import numpy as np
from common.additional_methods import AdditionalMethods

EPS = 1e-7   # tolerance when comparing numbers (rounding errors)
BIGM = float('inf')

class pareto_median_undirected_network:
    """
    Pareto median on an undirected network with Q >= 2 weight vectors w^1, ..., w^Q.

    Every weight vector q gives an objective function f^q(x) = sum_k w^q_k * d(v_k, x). A location (a vertex
    or a point on an edge) is Pareto optimal if no other location is at least as good in every objective
    function and better in at least one. On an edge every f^q is concave and piecewise linear in the
    position t (breakpoints, see AdditionalMethods._breakpoints). The algorithm follows the lecture
    "Pareto Locations in Networks":
      1. Shortest path lengths, the values f^q(v) of the vertices and the vertices that no other vertex
         dominates (pareto_vertices_determination).
      2. For every edge the part X_par(e) that its end vertices do not dominate (X_par_of_e_determination).
      3. Q = 2: the images of X_par(e) in the objective function space are walked from the median of f^2 to
         the median of f^1; the walked locations form the Pareto set (run_2_criteria).
         Q > 2: X_par(e) is split into linear subedges, all pieces are compared pairwise, and the
         dominated parts are removed (run_q_criteria).

    :param weights: the weight vectors w^1, ..., w^Q, one list per weight vector with one weight per vertex
    :param matrix: adjacency matrix with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        # Adjacency matrix as floats: no edge (None, "n", "inf" or empty) as infinity
        self.matrix = np.array([
            [
                np.inf if value is None or str(value).lower() in ("n", "inf", "")
                else float(value)
                for value in row
            ]
            for row in matrix
        ], dtype=float)

        np.fill_diagonal(self.matrix, 0.0)
        self.weights = np.asarray(weights, dtype=float)
        self.solution_path = ""
        self.pareto_points = []
        self.im = []
        self.col_sums = np.array([])
        self.distances = np.array([])
        self.sorted_breakpoints_per_edge = []


    def run(self):
        """
        Runs the algorithm.

        :return: (Pareto set, result text with the Pareto frontier and the objective function frontier, solution
                 path, None); the Pareto set contains vertex numbers and parts of edges ((i, j), (t1, t2)), the
                 points of the edge (i, j) from t1 to t2 (all 1-based); with fewer than two weight vectors or if
                 the customers are not connected: ([], "No result: ..." text, solution path, None)
        """
        nr_objectives = len(self.weights)
        n = len(self.matrix)
        # A Pareto median needs at least two weight vectors (objective functions)
        if self.weights.ndim != 2 or nr_objectives < 2:
            return [], "No result: the Pareto median needs at least two weight vectors.", "", None

        # Calculating the distance matrix of the network
        self.distances = AdditionalMethods.floyd_warshall(self.matrix)
        self.solution_path += f"The network has the distance matrix:\n{AdditionalMethods.format_matrix(self.distances)}"

        # Calculating the weighted distance matrices
        self.weighted_distances, self.col_sums, self.solution_path = pareto_median_undirected_network.multiple_weighted_distances_calculations(self.distances, self.weights, nr_objectives, self.solution_path)
        # The customers (vertices with a positive weight in at least one weight vector) must be connected
        customer_weights = [max(self.weights[q][k] for q in range(nr_objectives)) for k in range(n)]
        if not AdditionalMethods.location_exists(self.distances, customer_weights, "undirected"):
            return AdditionalMethods.no_location_result("Pareto locations", "undirected", self.solution_path)

        # Vertices that no other vertex dominates, and the dominance relation between the vertices
        pareto_vertices, dominance_relation, self.solution_path = pareto_median_undirected_network.pareto_vertices_determination(n, self.col_sums, self.solution_path)
        
        # X_par(e) for every edge
        edges = AdditionalMethods.get_edges(self.matrix, "undirected")
        pareto_points_per_edge = []
        for e in edges:
            pareto_points_edge = self.X_par_of_e_determination(n, e, dominance_relation, nr_objectives)
            pareto_points_per_edge.append(pareto_points_edge)
        
        # Pareto locations that the walk along the edges cannot find (all customers on one vertex, or none and no edges)
        trivial = AdditionalMethods.trivial_pareto_vertices(self.weights, edges)
        if nr_objectives == 2 and trivial is not None:
            self.pareto_points = trivial
            return self._results_bicriteria()
        
        # Q = 2: walk along the Pareto front; Q > 2: compare all pieces pairwise
        if nr_objectives == 2:
            return self.run_2_criteria(edges, pareto_points_per_edge, pareto_vertices)
        else:
            return self.run_q_criteria(edges, pareto_points_per_edge, pareto_vertices)

    def X_par_of_e_determination(self, n, e, dominance_relation, nr_objectives):
        """
        X_par(e): the points of the edge e = (a, b) that its end vertices do not dominate.
          - If one end vertex dominates the other, X_par(e) is this vertex.
          - If both end vertices have the same values: the complete edge if its midpoint has these values as
            well (then all objective functions are constant on the edge), otherwise only the two vertices.
          - Otherwise for every pair of objective functions (f, g), oriented so that f is smaller at b and g
            is smaller at a: since f and g are concave on the edge, the points before t1 (where f is still at
            least f(a)) are not better than a, and the points after t2 (from where g is at least g(b)) are
            not better than b. X_par(e) consists of the two vertices and the part [t1, t2], extended to the
            smallest t1 and the largest t2 of all pairs with t1 < t2.
        Also stores the sorted breakpoints of the edge in self.sorted_breakpoints_per_edge.

        :param n: number of vertices
        :param e: the edge (a, b), 0-based
        :param dominance_relation: the pairs (i, j) of vertices where i dominates j
        :param nr_objectives: number Q of objective functions
        :return: [a] or [b] (one vertex), [a, b] (both vertices), [a, b, [((a, b), 0), ((a, b), 1)]] (complete
                 edge with constant values) or [a, b, [[(a, b), t1], [(a, b), t2]]]
        """
        if (e[0], e[1]) in dominance_relation:
            # One end vertex dominates the other: X_par(e) is the dominating vertex
            pareto_points_edge = [e[0]]
            self.sorted_breakpoints_per_edge.append([])
            self.solution_path += f"\nVertex {e[0]+1} dominates vertex {e[1]+1}. Hence, X_par(e) is the vertex {e[0]+1}."
            return pareto_points_edge
        elif (e[1], e[0]) in dominance_relation:
            pareto_points_edge = [e[1]]
            self.sorted_breakpoints_per_edge.append([])
            self.solution_path += f"\nVertex {e[1]+1} dominates vertex {e[0]+1}. Hence, X_par(e) is the vertex {e[1]+1}."
            return pareto_points_edge
        elif np.all(abs(self.col_sums[:,e[0]] - self.col_sums[:,e[1]]) <= EPS):
            # Both end vertices have the same values: the complete edge if the midpoint has them as well
            objective_of_point = [AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), 0.5), self.distances, self.matrix, self.weights[i]) for i in range(nr_objectives)]
            if np.all(abs(objective_of_point - self.col_sums[:,e[0]]) <= EPS):
                pareto_points_edge = [e[0], e[1], [((e[0], e[1]), 0), ((e[0], e[1]), 1)]]
                self.solution_path += f"\nThe edge ({e[0]+1}, {e[1]+1}) has the same objective function at each point. Hence, X_par(e) is the complete edge."
            else:
                pareto_points_edge = [e[0], e[1]]
                self.solution_path += f"\nFor edge ({e[0]+1}, {e[1]+1}) we have the same objective function at both vertices but not on the edge. Hence, X_par(e) has only the two vertices."
            self.sorted_breakpoints_per_edge.append([])
            return pareto_points_edge
        else:
            pareto_points_edge = [e[0], e[1]]
            # Breakpoints of the edge: where the shortest path of a customer switches from a to b
            T, T_print = AdditionalMethods._breakpoints(e, n, self.distances, self.matrix)
            T = np.array(T)
            self.solution_path += f"\nFor edge ({e[0]+1}, {e[1]+1}) we have the breakpoints [{', '.join('–' if np.isnan(t) else f'{t:.4f}' for t in T_print)}] (sequence corresponds to the vertex indices)."
            indices = np.argsort(T)
            self.sorted_breakpoints_per_edge.append(np.sort(T))
            # Every pair of objective functions gives a part [t1, t2] that the end vertices do not dominate
            for i in range(nr_objectives - 1):
                for j in range(i+1,nr_objectives):
                    f_idx1 = i
                    f_idx2 = j
                    # Orientation: f^(f_idx1) should be smaller at b, f^(f_idx2) smaller at a
                    if self.col_sums[i, e[0]] <= self.col_sums[i, e[1]] and self.col_sums[j, e[0]] >= self.col_sums[j, e[1]]:
                        f_idx1 = j
                        f_idx2 = i
                        self.solution_path += f"\nf^{i+1}({e[0]+1}) <= f^{i+1}({e[1]+1}) and f^{j+1}({e[0]+1}) >= f^{j+1}({e[1]+1}). Switch the objective function indices for this edge."
                    # t1: up to t1, f^(f_idx1) is at least its value at a (t1 = 1 if it is not smaller at b)
                    signal = 0
                    for idx, k in enumerate(indices):
                        if T[k] > EPS:
                            objective_of_point = AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), T[k]), self.distances, self.matrix, self.weights[f_idx1])
                            if objective_of_point <= self.col_sums[f_idx1, e[0]] + EPS:
                                break
                            elif idx == len(indices) - 1:
                                signal = 1
                    prev_idx = indices[idx - 1]
                    if self.col_sums[f_idx1, e[0]] <= self.col_sums[f_idx1, e[1]]:
                        t1 = 1 # Not actually 1, but we can exclude it later
                    elif signal == 1:
                        t1 = 1
                    elif abs(objective_of_point - self.col_sums[f_idx1, e[0]]) <= EPS:
                        t1 = T[k]
                        # the objective can stay at the value of the vertex for a while (weights 0): the points up to
                        # the end of this constant part are dominated by the vertex, so t1 is the end of the constant part
                        for k_next in indices[idx + 1:]:
                            objective_next = AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), T[k_next]), self.distances, self.matrix, self.weights[f_idx1])
                            if abs(objective_next - self.col_sums[f_idx1, e[0]]) <= EPS:
                                t1 = T[k_next]
                            else:
                                break
                    else:
                        objective_previous_point = AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), T[prev_idx]), self.distances, self.matrix, self.weights[f_idx1])
                        m = (objective_of_point - objective_previous_point) / (T[k] - T[prev_idx])
                        inters = objective_of_point - m * T[k]
                        t1 = (self.col_sums[f_idx1, e[0]] - inters) / m
                        if t1 <= 0:  #rounding errors might turn it -0.0000
                            t1 = 0.0                 
                    # t2: from t2 on, f^(f_idx2) is at least its value at b (t2 = 0 if it is not smaller at a)
                    for idx, k in enumerate(indices):
                        if T[k] > EPS:
                            objective_of_point = AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), T[k]), self.distances, self.matrix, self.weights[f_idx2])
                            if objective_of_point >= self.col_sums[f_idx2, e[1]] - EPS:
                                break
                    signal = 0
                    if idx == 0:
                        signal = 1
                    prev_idx = indices[idx - 1]
                    if self.col_sums[f_idx2, e[0]] >= self.col_sums[f_idx2, e[1]]:
                        t2 = 0 # Not actually 0, but we can exclude it later
                    elif signal == 1:
                        m = (objective_of_point - self.col_sums[f_idx2, e[0]]) / (T[k] - 0)
                        t2 = (self.col_sums[f_idx2, e[1]] - self.col_sums[f_idx2, e[0]]) / m
                    elif abs(T[k] - 1) <= EPS:
                        t2 = 1
                    elif abs(objective_of_point - self.col_sums[f_idx2, e[1]]) <= EPS:
                        t2 = T[k]
                    else:
                        objective_previous_point = AdditionalMethods.calculate_weighted_distance_point(((e[0], e[1]), T[prev_idx]), self.distances, self.matrix, self.weights[f_idx2])
                        m = (objective_of_point - objective_previous_point) / (T[k] - T[prev_idx])
                        inters = objective_of_point - m * T[k]
                        t2 = (self.col_sums[f_idx2, e[1]] - inters) / m      
                        if t2 <= 0:      #rounding errors might turn it -0.0000
                            t2 = 0.0
                    # A non-empty part [t1, t2]: extend X_par(e) by it
                    if t1 < t2 - EPS:
                        if len(pareto_points_edge) == 2:
                            pareto_points_edge.append([[(e[0], e[1]), t1], [(e[0], e[1]), t2]])
                        else:
                            
                            if t1 < pareto_points_edge[2][0][1]:
                                pareto_points_edge[2][0][1] = t1
                            if t2 > pareto_points_edge[2][1][1]:
                                pareto_points_edge[2][1][1] = t2
                    # Solution path with 1-based vertices
                    pareto_print = pareto_median_undirected_network.deepcopy_list(pareto_points_edge)
                    for v in range(2):
                        pareto_print[v] += 1
                    if len(pareto_points_edge) > 2:
                        ed = (e[0] + 1, e[1] + 1)
                        pareto_print[2][0][0] = ed
                        pareto_print[2][1][0] = ed
                    self.solution_path += f"\nWe get t1={t1:.4f} and t2={t2:.4f} and hence, X_par(e) = {pareto_median_undirected_network.remove_numpy_types(pareto_print)}."
            return pareto_points_edge

    # ----------------------------------------------------------------------------------------------
    # Q-criteria case (more than two objective functions), as in the lecture
    # "Pareto Locations in Networks - Q-criteria Case". X_par(e) of every edge has already been
    # determined above (the same way for any number of objective functions); what remains is
    #   Step 2: compare all vertices and all edges on which every objective function is constant
    #   Step 3: split X_par(e) at the breakpoints into linear subedges, compare all pieces pairwise
    #           and remove the dominated parts
    # A piece of X_par is stored as a dictionary:
    #   "edge":   (a, b) for a part of the edge (a, b), None for a vertex
    #   "vertex": the vertex (only for a vertex)
    #   "lo", "hi": the part [lo, hi] of the edge (lo = hi = 0 for a vertex)
    #   "m", "b": f^q((edge, t)) = b[q] + m[q] * t for t in [lo, hi] (for a vertex: m = 0, b = f(vertex))
    # ----------------------------------------------------------------------------------------------

    def run_q_criteria(self, edges, pareto_points_per_edge, pareto_vertices):
        """
        Pareto locations for more than two objective functions (Q-criteria case of the lecture). Besides the
        parameters it uses self.sorted_breakpoints_per_edge (the sorted breakpoints of every edge), self.distances,
        self.col_sums (self.col_sums[q][v] = f^q(v), the objective function values of the vertices) and
        self.solution_path.

        :param edges: the edges of the network
        :param pareto_points_per_edge: X_par(e) of every edge, as determined in run()
        :param pareto_vertices: the vertices that no other vertex dominates (X_par(V))
        :return: (pareto_set, result_string, self.solution_path, None)
        """
        Q = len(self.weights)
        self.solution_path += f"\nQ-criteria case with Q = {Q} objective functions: X_par(e) is known for every edge; now we compare the vertices and the edges with constant objective functions, and then all linear subedges pairwise."

        # The pieces of X_par: the vertices not dominated by another vertex, ...
        pieces = []
        for v in pareto_vertices:
            pieces.append({"edge": None, "vertex": v, "lo": 0.0, "hi": 0.0,
                           "m": [0.0] * Q, "b": [float(self.col_sums[q][v]) for q in range(Q)]})
        # ... the edges with constant objective functions and the linear subedges of X_par(e)
        for idx, e in enumerate(edges):
            a = int(e[0])
            b = int(e[1])
            x_par = pareto_points_per_edge[idx]
            if len(x_par) < 3:
                continue                    # X_par(e) has only vertices
            if isinstance(x_par[2][0], tuple):
                # the complete edge, all objective functions are constant on it
                pieces.append({"edge": (a, b), "vertex": None, "lo": 0.0, "hi": 1.0,
                               "m": [0.0] * Q, "b": [float(self.col_sums[q][a]) for q in range(Q)], "constant": True})
                continue
            # X_par(e) contains ((a, b), (t1, t2)): split it at the breakpoints into linear subedges
            t1 = float(x_par[2][0][1])
            t2 = float(x_par[2][1][1])
            cuts = [t1]
            for t in self.sorted_breakpoints_per_edge[idx]:
                if cuts[-1] + EPS < t < t2 - EPS:      # the breakpoints inside (t1, t2), each one only once
                    cuts.append(float(t))
            cuts.append(t2)
            for i in range(len(cuts) - 1):
                lo = cuts[i]
                hi = cuts[i + 1]
                f_lo = self.objective_vector(a, b, lo)
                f_hi = self.objective_vector(a, b, hi)
                m = [(f_hi[q] - f_lo[q]) / (hi - lo) for q in range(Q)]
                pieces.append({"edge": (a, b), "vertex": None, "lo": lo, "hi": hi,
                               "m": m, "b": [f_lo[q] - m[q] * lo for q in range(Q)]})

        # ---------- Step 2: vertices and edges with constant objective functions ----------
        self.solution_path += f"\nWe compare all vertices and the edges with constant objective functions. The vertices not dominated by another vertex are {[v + 1 for v in pareto_vertices]}."
        kept = []
        for piece in pieces:
            if piece.get("constant") and piece["edge"][0] not in pareto_vertices:
                self.solution_path += f"\nThe edge ({piece['edge'][0]+1}, {piece['edge'][1]+1}) has the objective function values of vertex {piece['edge'][0]+1}, which is dominated by another vertex; remove the edge."
            else:
                kept.append(piece)
        pieces = kept

        # ---------- Step 3: compare all pieces pairwise ----------
        self.solution_path += f"\nWe compare all {len(pieces)} pieces pairwise: {', '.join(self.describe(p) for p in pieces)}."
        removed = [[] for p in pieces]
        for i in range(len(pieces)):
            for j in range(len(pieces)):
                if i == j:
                    continue
                part = self.dominated_part(pieces[i], pieces[j])
                if part is None:
                    continue
                removed[i].append(part)
                if pieces[i]["edge"] is None:
                    self.solution_path += f"\n{self.describe(pieces[i]).capitalize()} is dominated by {self.describe(pieces[j])}; remove it."
                else:
                    self.solution_path += f"\n{self.describe(pieces[i]).capitalize()} is dominated by {self.describe(pieces[j])} for t in [{part[0]:.4f}, {part[1]:.4f}]; remove this part."

        # Remaining vertices and parts of edges
        pareto_vertices_left = []
        parts_left = []
        for i, piece in enumerate(pieces):
            if piece["edge"] is None:
                if len(removed[i]) == 0:
                    pareto_vertices_left.append(piece["vertex"])
                continue
            parts = [(piece["lo"], piece["hi"])]
            for LB, UB in removed[i]:
                new_parts = []
                for lo, hi in parts:
                    if UB < lo - EPS or LB > hi + EPS:
                        new_parts.append((lo, hi))
                        continue
                    if LB > lo + EPS:
                        new_parts.append((lo, LB))
                    if UB < hi - EPS:
                        new_parts.append((UB, hi))
                parts = new_parts
            for lo, hi in parts:
                parts_left.append([piece["edge"], lo, hi])

        # Neighbouring parts of the same edge are joined, but not at a point that was removed
        removed_on_edge = {}
        for i, piece in enumerate(pieces):
            if piece["edge"] is not None:
                removed_on_edge.setdefault(piece["edge"], []).extend(removed[i])
        parts_left.sort()
        joined = []
        for edge, lo, hi in parts_left:
            meeting_point_removed = False
            for LB, UB in removed_on_edge.get(edge, []):
                if LB - EPS <= lo <= UB + EPS:
                    meeting_point_removed = True
            if len(joined) > 0 and joined[-1][0] == edge and lo <= joined[-1][2] + EPS and not meeting_point_removed:
                joined[-1][2] = max(joined[-1][2], hi)
            else:
                joined.append([edge, lo, hi])

        # Output
        pareto_set = []
        frontier = []
        for v in sorted(pareto_vertices_left):
            pareto_set.append(v + 1)
            frontier.append(tuple(float(self.col_sums[q][v]) for q in range(Q)))
        for (a, b), lo, hi in joined:
            pareto_set.append(((a + 1, b + 1), (lo, hi)))
            frontier.append([tuple(self.objective_vector(a, b, lo)), tuple(self.objective_vector(a, b, hi))])
        self.solution_path += "\nAll pieces have been compared; the remaining vertices and parts of edges are the Pareto locations."
        result_string = ("Pareto frontier {" + ", ".join(self.format_numbers(p) for p in pareto_set) + "}"
                         f"\nObjective function frontier: {self.format_numbers(frontier)}")
        return pareto_set, result_string, self.solution_path, None

    def objective_vector(self, a, b, t):
        """Values (f^1, ..., f^Q) at the point ((a, b), t); t = 0 is vertex a, t = 1 is vertex b."""
        l = self.matrix[a, b]
        values = []
        for q in range(len(self.weights)):
            total = 0.0
            for k in range(len(self.distances)):
                if self.weights[q][k] > 0:      # customers with weight 0 do not count (and may be unreachable)
                    total += self.weights[q][k] * min(self.distances[k, a] + t * l, self.distances[k, b] + (1 - t) * l)
            values.append(float(total))
        return values

    # ----------------------------------------------------------------------------------------------
    # 2-criteria case: X_par(e) of every edge is mapped into the objective function space, and the
    # Pareto front is walked from the median of f2 to the median of f1. self.im holds one image per edge:
    #   image:   {"edge": (a, b), "kind": ..., "entries": [...]}
    #            kind "points":            only single points (vertices, or an edge with the same values everywhere)
    #            kind "segments":          parts of the edge (a, b)
    #            kind "segments_reversed": the same, but stored for the edge (b, a), so that the image runs
    #                                      in the direction of the walk
    #   entries: {"type": "point", "objects": [...], "value": (f1, f2)}
    #                objects: the vertex, or both vertices of the edge (and the complete edge) with these values
    #            {"type": "segment", "edge": (a, b), "t": [t1, t2], "start": [f1, f2], "end": [f1, f2]}
    #                the part t in [t1, t2] of the edge; its image is the line from start to end
    # ----------------------------------------------------------------------------------------------

    def run_2_criteria(self, edges, pareto_points_per_edge, pareto_vertices):
        """
        Pareto locations for two objective functions (bicriteria case of the lecture). The images of X_par(e)
        in the objective function space (see the block comment above) are walked from the median of f^2 (the
        one with the smallest f^1) to the median of f^1. Each step goes from a Pareto point to the next one
        (_point_step) or along an image segment whose points are Pareto optimal (_segment_step); afterwards the
        chosen and the dominated parts of the images are removed.

        :return: see _results_bicriteria
        """
        self.solution_path += f"\n2-Criteria case; we get the following images, where a single tuple describes a point in the objective function space and tuples in brackets indicate a range of objective function values."
        self._image_generator(edges, pareto_points_per_edge, pareto_vertices)

        self.im = [im_e for im_e in self.im if im_e["kind"] is not None]  # edges without candidates have no image
        # Determining starting and end point(s)
        x1_median_value = min(self.col_sums[0])
        x2_median_value = min(self.col_sums[1])

        # Start: among the medians of f^2 the one with the smallest f^1
        x2_median_indizes = np.where(abs(self.col_sums[1] - x2_median_value) <= EPS)[0]
        x1_values = self.col_sums[0][x2_median_indizes]
        current_x1_value = np.min(x1_values)
        self.solution_path += f"\nWe start with the median for the second objective function. The values for (f1, f2) are ({current_x1_value:.4f}, {x2_median_value:.4f})."

        self.im = self.remove_numpy_types(self.im)

        Current, point_or_segment, Not_finished = self._start_point(current_x1_value, x1_median_value, x2_median_value)

        # Walk until the median of f^1 is reached: point steps and segment steps
        while Not_finished:
            if point_or_segment == 1:
                Current, point_or_segment, Not_finished = self._point_step(Current, x1_median_value)
            else:
                Current, point_or_segment, Not_finished = self._segment_step(Current, x1_median_value)

        return self._results_bicriteria()

    def _point_entry(self, objects, vertex):
        """Image entry of a single point: the objects (vertices, complete edge) with the objective function values of the vertex."""
        return {"type": "point", "objects": objects, "value": (self.col_sums[0][vertex], self.col_sums[1][vertex])}

    def _image_generator(self, edges, pareto_points_per_edge, pareto_vertices):
        """
        Builds self.im, the image of X_par(e) in the objective function space (f^1, f^2) for every edge (format
        in the block comment above): end vertices that no other vertex dominates as points, an edge with
        constant values as one point, and the part [t1, t2] as segments between consecutive breakpoints. Every
        image runs in the direction of the walk (from a smaller f^2 to a smaller f^1); if necessary it is stored
        for the reversed edge (b, a) ("segments_reversed").
        """
        for idx, e in enumerate(edges):
            if isinstance(e, np.ndarray):
                e = (e[0], e[1])
            im_of_edge = {"edge": e, "kind": None, "entries": []}

            if len(pareto_points_per_edge[idx]) == 1:
                # Only one point is still in the Pareto set
                if pareto_points_per_edge[idx][0] in pareto_vertices:
                    im_of_edge = {"edge": e, "kind": "points", "entries": [self._point_entry([pareto_points_per_edge[idx][0]], pareto_points_per_edge[idx][0])]}

            elif len(pareto_points_per_edge[idx]) == 2:
                # Both points are still in the Pareto set
                if abs(self.col_sums[0][e[0]] - self.col_sums[0][e[1]]) <= EPS:
                    # Both points have same objective values
                    if e[0] in pareto_vertices:
                        im_of_edge = {"edge": e, "kind": "points", "entries": [self._point_entry((e[0], e[1]), e[0])]}
                else:
                    if e[0] in pareto_vertices:
                        # if the first vertex is in the Pareto set
                        im_of_edge = {"edge": e, "kind": "points", "entries": [self._point_entry([e[0]], e[0])]}
                    if e[1] in pareto_vertices:
                        # if the second vertex is in the Pareto set
                        if im_of_edge["kind"] is None:
                            im_of_edge = {"edge": e, "kind": "points", "entries": [self._point_entry([e[1]], e[1])]}
                        else:
                            im_of_edge["entries"].append(self._point_entry([e[1]], e[1]))

            elif len(pareto_points_per_edge[idx]) == 3 and isinstance(pareto_points_per_edge[idx][2][0], tuple):
                # Vertices and the whole edge are in the Pareto set (with the same objective values)
                if e[0] in pareto_vertices:
                    im_of_edge = {"edge": e, "kind": "points", "entries": [self._point_entry((e[0], e[1], [[(e[0], e[1]), 0], [(e[0], e[1]), 1]]), e[0])]}

            elif len(pareto_points_per_edge[idx]) == 3:
                # Vertices and part of the edge are in the Pareto set; if f^1 is not larger and f^2 not smaller at
                # a, the image is stored for the reversed edge (b, a), with the positions counted from b
                if self.col_sums[0][e[0]] <= self.col_sums[0][e[1]] and self.col_sums[1][e[0]] >= self.col_sums[1][e[1]]:
                    im_of_edge = {"edge": (e[1], e[0]), "kind": "segments_reversed", "entries": [self._point_entry([e[1]], e[1])]}
                    t1 = 1 - pareto_points_per_edge[idx][2][1][1]
                    t2 = 1 - pareto_points_per_edge[idx][2][0][1]
                    im_of_edge = self._image_of_non_constant_edge(e, idx, im_of_edge, t1, t2, 1, 0)
                else:
                    im_of_edge = {"edge": e, "kind": "segments", "entries": [self._point_entry([e[0]], e[0])]}
                    t1 = pareto_points_per_edge[idx][2][0][1]
                    t2 = pareto_points_per_edge[idx][2][1][1]
                    im_of_edge = self._image_of_non_constant_edge(e, idx, im_of_edge, t1, t2, 0, 1)
            self.im.append(im_of_edge)

            im_print = []
            for entry in im_of_edge["entries"]:
                if entry["type"] == "point":
                    im_print.append(entry["value"])
                else:
                    im_print.append([tuple(entry["start"]), tuple(entry["end"])])
            if len(im_print) == 0:
                continue
            else:
                self.solution_path += f"\nEdge ({e[0]+1}, {e[1]+1}) has the image {pareto_median_undirected_network.remove_numpy_types(im_print)}."

    def _image_of_non_constant_edge(self, e, idx, im_of_edge, t1, t2, v0, v1):
        """
        Appends the image of the part [t1, t2] of the edge (e[v0], e[v1]): one segment between two consecutive
        breakpoints (all objective functions are linear there), followed by the point entry of the end vertex
        e[v1]. For the reversed edge (v0 = 1) the positions are counted from e[1].

        :return: the image of the edge
        """
        obj_0_start = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), t1), self.distances, self.matrix, self.weights[0])
        obj_1_start = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), t1), self.distances, self.matrix, self.weights[1])
        last_breakpoint = t1
        last_breakpoint_value = [obj_0_start, obj_1_start]
        if v0 == 1:
            self.sorted_breakpoints_per_edge[idx] = self.sorted_breakpoints_per_edge[idx][::-1]
        for breakpoint in self.sorted_breakpoints_per_edge[idx]:
            if v0 == 1:
                breakpoint = 1 - breakpoint
            if breakpoint <= t1 + EPS or abs(breakpoint - last_breakpoint) <= EPS:
                continue
            elif breakpoint >= t2 - EPS:
                break
            else:
                obj_0 = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), breakpoint), self.distances, self.matrix, self.weights[0])
                obj_1 = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), breakpoint), self.distances, self.matrix, self.weights[1])
                im_of_edge["entries"].append({"type": "segment", "edge": (e[v0], e[v1]), "t": [last_breakpoint, breakpoint], "start": last_breakpoint_value, "end": [obj_0, obj_1]})
                last_breakpoint = breakpoint
                last_breakpoint_value = [obj_0, obj_1]
        obj_0_end = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), t2), self.distances, self.matrix, self.weights[0])
        obj_1_end = AdditionalMethods.calculate_weighted_distance_point(((e[v0], e[v1]), t2), self.distances, self.matrix, self.weights[1])
        im_of_edge["entries"].append({"type": "segment", "edge": (e[v0], e[v1]), "t": [last_breakpoint, t2], "start": last_breakpoint_value, "end": [obj_0_end, obj_1_end]})
        im_of_edge["entries"].append(self._point_entry([e[v1]], e[v1]))
        return im_of_edge

    def _start_point(self, current_x1_value, x1_median_value, x2_median_value):
        """
        Start of the walk at the point (current_x1_value, x2_median_value), the median of f^2 with the smallest
        f^1: adds the locations with these values to the Pareto points, removes the image parts that this point
        dominates and chooses the first segment if the front continues along a segment.

        :return: (Current, point_or_segment, Not_finished): Current = [[f^1, f^2] of the current point, the
                 current object (a Pareto point, or [segment, segments with the same slope])];
                 point_or_segment = 1 if a point step follows, 2 if a segment step follows;
                 Not_finished = False if the median of f^1 is reached
        """
        potential_starting_edges = []
        to_remove = []
        for idx, im_e in enumerate(self.im):
            entries = im_e["entries"]
            if im_e["kind"] == "points":
                if len(entries) == 1:
                    if abs(entries[0]["value"][0] - current_x1_value) <= EPS and abs(entries[0]["value"][1] - x2_median_value) <= EPS:
                        for obj in entries[0]["objects"]:
                            if obj not in self.pareto_points:
                                self.pareto_points.append(obj)
                                if isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, np.int64):
                                    self.solution_path += f"\nVertex {obj + 1} is part of the Pareto front."
                                else:
                                    self.solution_path += f"\nEdge ({obj[0][0][0] + 1}, {obj[0][0][1] + 1}) is part of the Pareto front."
                    if entries[0]["value"][0] >= current_x1_value - EPS and entries[0]["value"][1] >= x2_median_value - EPS:
                        to_remove.append(idx)
                elif len(entries) == 2:
                    if abs(entries[0]["value"][0] - current_x1_value) <= EPS and abs(entries[0]["value"][1] - x2_median_value) <= EPS:
                        if entries[0]["objects"][0] not in self.pareto_points:
                            self.pareto_points.append(entries[0]["objects"][0])
                            self.solution_path += f"\nVertex {entries[0]['objects'][0] + 1} is part of the Pareto front."
                    elif abs(entries[1]["value"][0] - current_x1_value) <= EPS and abs(entries[1]["value"][1] - x2_median_value) <= EPS:
                        if entries[1]["objects"][0] not in self.pareto_points:
                            self.pareto_points.append(entries[1]["objects"][0])
                            self.solution_path += f"\nVertex {entries[1]['objects'][0] + 1} is part of the Pareto front."
                    if entries[1]["value"][0] >= current_x1_value - EPS and entries[1]["value"][1] >= x2_median_value - EPS:
                        entries.pop(1)
                    if entries[0]["value"][0] >= current_x1_value - EPS and entries[0]["value"][1] >= x2_median_value - EPS:
                        entries.pop(0)
                    if len(entries) == 0:
                        to_remove.append(idx)
            else:
                to_delete = []
                if abs(entries[0]["value"][0] - current_x1_value) <= EPS and abs(entries[0]["value"][1] - x2_median_value) <= EPS:
                    if entries[0]["objects"][0] not in self.pareto_points:
                        self.pareto_points.append(entries[0]["objects"][0])
                        self.solution_path += f"\nVertex {entries[0]['objects'][0] + 1} is part of the Pareto front."
                    if entries[1]["type"] == "segment" and abs(entries[1]["start"][1] - x2_median_value) <= EPS:
                        potential_starting_edges.append(entries[1])
                    to_delete.append(0)
                elif abs(entries[-1]["value"][0] - current_x1_value) <= EPS and abs(entries[-1]["value"][1] - x2_median_value) <= EPS:
                    if entries[-1]["objects"][0] not in self.pareto_points:
                        self.pareto_points.append(entries[-1]["objects"][0])
                        self.solution_path += f"\nVertex {entries[-1]['objects'][0] + 1} is part of the Pareto front."
                    if entries[-2]["type"] == "segment" and abs(entries[-2]["start"][1] - x2_median_value) <= EPS:
                        potential_starting_edges.append(entries[-2])
                    to_delete.append(len(entries) - 1)
                for idx2, entry in enumerate(entries):
                    if entry["type"] == "point":
                        if entry["value"][0] >= current_x1_value - EPS and entry["value"][1] >= x2_median_value - EPS:
                            to_delete.append(idx2)
                    else:
                        if entry["start"][0] > current_x1_value + EPS or (abs(entry["start"][0] - current_x1_value) <= EPS and entry["start"][1] > x2_median_value + EPS):
                            if entry["end"][0] > current_x1_value + EPS or (abs(entry["end"][0] - current_x1_value) <= EPS and entry["end"][1] > x2_median_value + EPS):
                                if idx2 not in to_delete:
                                    to_delete.append(idx2)
                to_delete = sorted(set(to_delete), reverse=True)
                for idx2 in to_delete:
                    entries.pop(idx2)
                if len(entries) == 0:
                    to_remove.append(idx)

        to_remove = sorted(set(to_remove), reverse=True)
        for idx in to_remove:
            self.im.pop(idx)

        Current = [[current_x1_value, x2_median_value], (self.pareto_points[0])]
        Not_finished = True
        point_or_segment = 1
        if abs(x1_median_value - current_x1_value) <= EPS:
            Not_finished = False
        else:
            if len(potential_starting_edges) >= 1:
                point_or_segment = 2
                Current[1] = self._determining_next_segment(potential_starting_edges)

                # the walked starting segment and those with the same slope (handled in segments_to_check) leave their image;
                # starting segments with another slope stay for later
                for seg in [Current[1][0]] + Current[1][1]:
                    for im_e in self.im:
                        if seg in im_e["entries"]:
                            im_e["entries"].remove(seg)
                self.im = [im_e for im_e in self.im if len(im_e["entries"]) > 0]

        return Current, point_or_segment, Not_finished

    def _point_step(self, Current, x1_median_value):
        """
        Point step from the current Pareto point: among the images with a smaller f^1, the next Pareto point
        is the one with the smallest f^2 (and among those the smallest f^1). It can be a vertex, an edge with
        constant values or the start of a segment, possibly cut at the current f^1 (_comparing_with_other_vertices,
        _comparing_with_other_segments). Then the new Pareto points are added, the next segment is chosen if the
        front continues along a segment, and the chosen and the dominated image parts are removed.

        :return: (Current, point_or_segment, Not_finished) as in _start_point
        """
        iteration_start_x1_value = Current[0][0]
        iteration_start_x2_value = Current[0][1]
        current_x1_value, current_x2_value = iteration_start_x1_value, iteration_start_x2_value
        next_obj = []
        maybe_to_remove = []
        # The next Pareto point: among all images with a smaller f^1 the point with the smallest f^2
        for idx, im_e in enumerate(self.im):
            if im_e["kind"] == "points":
                maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value = self._comparing_with_other_vertices(maybe_to_remove, next_obj, im_e, idx, iteration_start_x1_value, current_x1_value, current_x2_value)
            else:
                maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value = self._comparing_with_other_segments(maybe_to_remove, next_obj, im_e, idx, iteration_start_x1_value, iteration_start_x2_value, current_x1_value, current_x2_value)

        if abs(current_x1_value - iteration_start_x1_value) <= EPS and current_x2_value > iteration_start_x2_value + EPS:
            # the next segment starts directly above the last Pareto point: this start point is dominated
            self.solution_path += f"\nThe next edge segment starts at ({current_x1_value:.4f}, {current_x2_value:.4f}), directly above the last Pareto point; this start point is dominated, the points after it are not."
        else:
            self.solution_path += f"\nNext Pareto point of the objective function ({current_x1_value:.4f}, {current_x2_value:.4f})."

        # Adding Pareto points
        point_or_segment = 1
        potential_segments = self._adding_pareto_points(next_obj)

        # determining next segment if there is one
        if abs(current_x1_value - x1_median_value) <= EPS:
            return Current, point_or_segment, False
        else:
            Current[0] = [current_x1_value, current_x2_value]
            if len(potential_segments) >= 1:
                point_or_segment = 2
                Current[1] = self._determining_next_segment(potential_segments)
            else:
                Current[1] = [self.pareto_points[-1]]
        # Remove the new Pareto points/segments
        self._remove_chosen(maybe_to_remove, False)
        #remove dominated points/segments
        self._remove_dominated(current_x1_value, current_x2_value)

        return Current, point_or_segment, True

    def _comparing_with_other_vertices(self, maybe_to_remove, next_obj, im_e, idx, iteration_start_x1_value, current_x1_value, current_x2_value):
        """
        Point step: compares the points of an image of kind "points" that have a smaller f^1 than the current
        Pareto point with the best candidate so far (vertex_check).

        :return: (maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value): what to remove from the
                 images if the candidate is chosen, the candidate objects, the image and the values (f^1, f^2)
                 of the candidate
        """
        entries = im_e["entries"]
        if len(entries) == 1:
            if entries[0]["value"][0] < iteration_start_x1_value - EPS:
                maybe_to_remove, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.vertex_check(maybe_to_remove, next_obj, entries[0], current_x1_value, current_x2_value, idx, entries[0]["objects"])
        if len(entries) == 2:
            for i in [1, 0]:
                if entries[i]["value"][0] < iteration_start_x1_value - EPS:
                    maybe_to_remove, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.vertex_check(maybe_to_remove, next_obj, entries[i], current_x1_value, current_x2_value, (idx, entries[i]), [entries[i]["objects"][0]])
        return maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value

    def _comparing_with_other_segments(self, maybe_to_remove, next_obj, im_e, idx, iteration_start_x1_value, iteration_start_x2_value, current_x1_value, current_x2_value):
        """
        Point step: compares an image of segments with the best candidate so far: its end vertices with a
        smaller f^1 (vertex_check), segments that start at the current Pareto point, and segments that cross
        the vertical line f^1 = current f^1; such a segment is cut at this line, and its point on the line is a
        candidate. A segment that ends exactly at the current Pareto point adds its end to the Pareto points.

        :return: (maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value) as in
                 _comparing_with_other_vertices
        """
        entries = im_e["entries"]
        if len(entries) == 1:
            iterator = [0]
        elif len(entries) >= 2:
            iterator = [-1, 0]
        for i in iterator:
            if entries[i]["type"] == "point":
                if entries[i]["value"][0] < iteration_start_x1_value - EPS:
                    maybe_to_remove, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.vertex_check(maybe_to_remove, next_obj, entries[i], current_x1_value, current_x2_value, (idx, entries[i]), [entries[i]["objects"][0]])
        for segment in entries:
            if segment["type"] == "point":
                continue
            else:
                if abs(segment["start"][0] - iteration_start_x1_value) <= EPS and abs(segment["start"][1] - iteration_start_x2_value) <= EPS:
                    if len(next_obj) == 0:
                        next_obj.append(segment)
                        current_x1_value = iteration_start_x1_value
                        current_x2_value = iteration_start_x2_value
                        maybe_to_remove = [(segment, idx)]
                    else:
                        if abs(current_x1_value - iteration_start_x1_value) <= EPS and abs(current_x2_value - iteration_start_x2_value) <= EPS:
                            next_obj.append(segment)
                            maybe_to_remove.append((segment, idx))
                        else:
                            current_x1_value = iteration_start_x1_value
                            current_x2_value = iteration_start_x2_value
                            next_obj = [segment]
                            maybe_to_remove = [(segment, idx)]
                elif len(next_obj) > 0 and abs(segment["start"][0] - iteration_start_x1_value) <= EPS and abs(current_x1_value - iteration_start_x1_value) <= EPS and abs(segment["start"][1] - current_x2_value) <= EPS:
                    # starts at the same point as the segment chosen so far: keep both
                    next_obj.append(segment)
                    maybe_to_remove.append((segment, idx))
                elif abs(segment["start"][0] - iteration_start_x1_value) <= EPS and (segment["start"][1] < current_x2_value - EPS or len(next_obj) == 0):
                    current_x1_value = segment["start"][0]
                    current_x2_value = segment["start"][1]
                    next_obj = [segment]
                    maybe_to_remove = [(segment, idx)]
                elif segment["start"][0] >= iteration_start_x1_value - EPS:
                    if segment["end"][0] <= iteration_start_x1_value + EPS:
                        if abs(segment["end"][0] - iteration_start_x1_value) <= EPS and abs(segment["end"][1] - iteration_start_x2_value) <= EPS:
                            if EPS < segment["t"][1] < 1 - EPS:      # t = 0 or 1 is a vertex
                                self.pareto_points.append([(segment["edge"][0], segment["edge"][1]), [segment["t"][1], segment["t"][1]]])
                        elif segment["end"][0] < iteration_start_x1_value - EPS:
                            slope = (segment["end"][1] - segment["start"][1]) / (segment["end"][0] - segment["start"][0])
                            intersec = segment["end"][1] - slope * segment["end"][0]
                            x2_value_to_check = slope * iteration_start_x1_value + intersec
                            new_t_value = segment["t"][0] + (segment["t"][1] - segment["t"][0]) * (iteration_start_x1_value - segment["start"][0]) / (segment["end"][0] - segment["start"][0])
                            if len(next_obj) == 0:
                                segment["t"][0], segment["start"][0], segment["start"][1] = new_t_value, iteration_start_x1_value, x2_value_to_check
                                next_obj = [segment]
                                current_x1_value = iteration_start_x1_value
                                current_x2_value = x2_value_to_check
                                maybe_to_remove = [(segment, idx)]
                            elif abs(x2_value_to_check - current_x2_value) <= EPS and abs(current_x1_value - iteration_start_x1_value) <= EPS:
                                segment["t"][0], segment["start"][0], segment["start"][1] = new_t_value, iteration_start_x1_value, x2_value_to_check
                                next_obj.append(segment)
                                maybe_to_remove.append((segment, idx))
                            elif x2_value_to_check < current_x2_value - EPS:
                                segment["t"][0], segment["start"][0], segment["start"][1] = new_t_value, iteration_start_x1_value, x2_value_to_check
                                current_x1_value = iteration_start_x1_value
                                current_x2_value = x2_value_to_check
                                next_obj = [segment]
                                maybe_to_remove = [(segment, idx)]
        return maybe_to_remove, next_obj, im_e, current_x1_value, current_x2_value

    def _segment_step(self, Current, x1_median_value):
        """
        Segment step along the current segment (Current[1][0]) from the current Pareto point. The walk stops
        where another image gets below the line of the segment or reaches its end value
        (_determining_following_parts). The segment up to there is added to the Pareto points (_end_of_segment),
        and the objects noted on the line are checked (_check_later). Then the next Pareto point or segment is
        chosen, and the chosen and the dominated image parts are removed.

        :return: (Current, point_or_segment, Not_finished) as in _start_point
        """
        the_segment = Current[1][0].copy()
        iteration_start_x1_value = Current[0][0]
        iteration_start_x2_value = Current[0][1]
        next_obj = []
        maybe_to_remove = []
        later_to_check = [seg for seg in Current[1][1]]

        current_x1_value = the_segment["end"][0]
        current_x2_value = the_segment["end"][1]
        # Line x2 = the_slope * x1 + the_intersec of the walked segment in the objective function space
        the_slope = (current_x2_value - iteration_start_x2_value) / (current_x1_value - iteration_start_x1_value)
        the_intersec = iteration_start_x2_value - the_slope * iteration_start_x1_value

        # Where the walk along the segment stops: the first point at which another image gets below the line
        maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value = self._determining_following_parts(Current, the_segment, the_slope, the_intersec, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value)

        x1_end_of_the_segment = self._end_of_segment(the_segment, the_slope, the_intersec, current_x2_value)
        self.pareto_points.append([the_segment["edge"], list(the_segment["t"])])   # a copy: the segment in the image changes later
        self.solution_path += f"\nThe edge segment on edge ({the_segment['edge'][0] + 1}, {the_segment['edge'][1] + 1}) in the range t=[{the_segment['t'][0]:.4f}, {the_segment['t'][1]:.4f}] is added to the Pareto front. For the objective function Pareto front we get the range [({iteration_start_x1_value:.4f}, {iteration_start_x2_value:.4f}), ({x1_end_of_the_segment:.4f}, {current_x2_value:.4f})]."

        maybe_to_remove = self._check_later(later_to_check, maybe_to_remove, current_x1_value, current_x2_value, x1_end_of_the_segment)
        self.solution_path += f"\nNext Pareto point of the objective function ({current_x1_value:.4f}, {current_x2_value:.4f})."
        # Adding Pareto points
        point_or_segment = 1
        potential_segments = self._adding_pareto_points(next_obj)

        # determining next segment if there is one
        if abs(current_x1_value - x1_median_value) <= EPS:
            return Current, point_or_segment, False
        else:
            Current[0] = [current_x1_value, current_x2_value]
            if len(potential_segments) >= 1:
                point_or_segment = 2
                Current[1] = self._determining_next_segment(potential_segments)
                # the other candidate segments start at the end of the walked segment, a point of the front: their start locations are Pareto points too
                for seg in potential_segments:
                    if seg is not Current[1][0] and not any(seg is s for s in Current[1][1]) and EPS < seg["t"][0] < 1 - EPS:
                        self.pareto_points.append([seg["edge"], [seg["t"][0], seg["t"][0]]])
            else:
                Current[1] = [self.pareto_points[-1]]

            # Remove the new Pareto points/segments
            self._remove_chosen(maybe_to_remove, True)

            #remove dominated points/segments
            self._remove_dominated(current_x1_value, current_x2_value)

            return Current, point_or_segment, True

    def _determining_following_parts(self, Current, the_segment, the_slope, the_intersec, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value):
        """
        Segment step: checks every image against the walked segment (line x2 = the_slope * x1 + the_intersec):
        points (constant_objective_function_part) and segments (non_constant_objective_function_part) below the
        line determine where the walk along the segment stops and what comes next; objects exactly on the line
        are noted in later_to_check.

        :return: (maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value), where
                 current_x2_value is the value of f^2 at which the walk stops
        """
        for idx, im_e in enumerate(self.im):
            entries = im_e["entries"]
            if im_e["kind"] == "points":
                if len(entries) == 1:
                    maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.constant_objective_function_part(entries[0],
                        maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, the_slope, the_intersec, entries[0]["objects"], idx, [obj for obj in entries[0]["objects"]], (idx, im_e))
                elif len(entries) == 2:
                    for i in [1, 0]:
                        maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.constant_objective_function_part(entries[i],
                            maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, the_slope, the_intersec, [entries[i]["objects"][0]], (idx, entries[i]), [entries[i]["objects"][0]], (idx, im_e, entries[i]))
            else:
                if len(entries) == 1:
                    iterator = [0]
                elif len(entries) >= 2:
                    iterator = [-1, 0]
                for i in iterator:
                    if entries[i]["type"] == "point":
                        maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.constant_objective_function_part(entries[i],
                            maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, the_slope, the_intersec, [entries[i]["objects"][0]], (idx, entries[i]), [entries[i]["objects"][0]], (idx, im_e, entries[i]))
                for idx_seg, segment in enumerate(entries):
                    if segment["type"] == "point":
                        continue
                    elif segment is Current[1][0]:
                        continue        # the current segment itself
                    elif any(segment is s for s in Current[1][1]):
                        continue        # a segment with the same start and slope: it is checked in later_to_check
                    elif (segment["start"][1] + EPS <= current_x2_value) and (segment["start"][1] - EPS > the_slope * segment["start"][0] + the_intersec) and (abs((segment["end"][1] - segment["start"][1]) / (segment["end"][0] - segment["start"][0]) - the_slope) <= EPS):
                        # The segment starts above the line of the current segment; if it is parallel to it,
                        # it never gets below the line and cannot cut off a part of the current segment
                        continue
                    else:
                        segment, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value = pareto_median_undirected_network.non_constant_objective_function_part(im_e,
                        segment, the_segment, the_slope, the_intersec, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, idx, idx_seg)
        return maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value

    def _end_of_segment(self, the_segment, the_slope, the_intersec, current_x2_value):
        """
        Cuts the walked segment at the value current_x2_value of f^2 where the walk stops; if the walk stops
        inside the segment, the rest goes back into the image of its edge.

        :return: the value of f^1 at the new end of the segment
        """
        old_t2, old_end = the_segment["t"][1], list(the_segment["end"])
        x1_end_of_the_segment = (current_x2_value - the_intersec) / the_slope
        t2_end_of_the_segment = the_segment["t"][0] + (the_segment["t"][1] - the_segment["t"][0]) * (current_x2_value - the_segment["start"][1]) / (the_segment["end"][1] - the_segment["start"][1])
        the_segment["t"][1], the_segment["end"][0], the_segment["end"][1] = t2_end_of_the_segment, x1_end_of_the_segment, current_x2_value

        if t2_end_of_the_segment < old_t2 - EPS:
            # the walk stops inside the segment at a point below it: the rest of the segment goes back into the image of its edge
            rest = {"type": "segment", "edge": the_segment["edge"], "t": [t2_end_of_the_segment, old_t2], "start": [x1_end_of_the_segment, current_x2_value], "end": old_end}
            found = False
            for im_e in self.im:
                if im_e["kind"] != "points" and im_e["edge"] == the_segment["edge"]:
                    im_e["entries"].insert(0, rest)
                    found = True
                    break
            if not found:
                self.im.append({"edge": the_segment["edge"], "kind": "segments", "entries": [rest]})
        return x1_end_of_the_segment

    def _check_later(self, later_to_check, maybe_to_remove, current_x1_value, current_x2_value, x1_end_of_the_segment):
        """
        Checks the objects on the line of the walked segment (later_to_check), now that the stop of the walk
        (current_x1_value, current_x2_value) is known:
          - dicts: segments with the same start and slope as the walked segment,
          - tuples of 2: the single point of an image of kind "points",
          - tuples of 3: an end vertex of an image of segments,
          - tuples of 5: segments that start on the line and run along it (-2: they end before the stop,
            -3: they reach beyond it).
        The parts up to the stop are added to the Pareto points, and the segments are cut at the stop.

        :return: maybe_to_remove, extended by the objects that were added completely
        """
        for obj in later_to_check:
            if isinstance(obj, dict):
                # a segment with the same start and slope as the walked segment
                if obj["end"][1] <= current_x2_value + EPS:
                    self.pareto_points.append([obj["edge"], obj["t"]])
                    for idx, im_e in enumerate(self.im):
                        if im_e["kind"] != "points":
                            if im_e["edge"][0] == obj["edge"][0] and im_e["edge"][1] == obj["edge"][1]:
                                maybe_to_remove.append((obj, idx))
                                break
                else:
                    slope = (obj["end"][1] - obj["start"][1]) / (obj["end"][0] - obj["start"][0])
                    intersec = obj["end"][1] - slope * obj["end"][0]
                    new_x1_value = (current_x2_value - intersec) / slope
                    new_t_value = obj["t"][0] + (obj["t"][1] - obj["t"][0]) * (current_x2_value - obj["start"][1]) / (obj["end"][1] - obj["start"][1])
                    self.pareto_points.append([(obj["edge"][0], obj["edge"][1]),[obj["t"][0], new_t_value]])
                    self.solution_path += f"\nWe also add the edge segment on edge ({obj['edge'][0] + 1}, {obj['edge'][1] + 1}) in the range t=[{obj['t'][0]:.4f}, {new_t_value:.4f}] to the Pareto front."
                    for idx, im_e in enumerate(self.im):
                        if im_e["kind"] != "points":
                            if im_e["edge"][0] == obj["edge"][0] and im_e["edge"][1] == obj["edge"][1]:
                                for s in im_e["entries"]:
                                    if s["type"] == "segment":
                                        if abs(s["t"][0] - obj["t"][0]) <= EPS:
                                            s["t"][0], s["start"][0], s["start"][1] = new_t_value, new_x1_value, current_x2_value
            elif isinstance(obj, tuple) and len(obj) == 2:
                point = obj[1]["entries"][0]     # the single point of an image of kind "points"
                if point["value"][1] < current_x2_value or (abs(point["value"][1] - current_x2_value) <= EPS and abs(point["value"][0] - current_x1_value) <= EPS):
                    for p in point["objects"]:
                        if p not in self.pareto_points:
                            self.pareto_points.append(p)
                            if isinstance(p, int):
                                self.solution_path += f"\nWe also add the vertex {p + 1} to the Pareto front."
                            else:
                                self.solution_path += f"\nWe also add the edge ({p[0][0][0] + 1}, {p[0][0][1] + 1}) to the Pareto front."
                    maybe_to_remove.append(obj[0])
            elif isinstance(obj, tuple) and len(obj) == 3:
                vertex = obj[2]     # the vertex entry that lies on the line of the segment
                entries = obj[1]["entries"]
                if vertex in entries and (vertex["value"][1] < current_x2_value or (abs(vertex["value"][1] - current_x2_value) <= EPS and abs(vertex["value"][0] - current_x1_value) <= EPS)):
                    if vertex["objects"][0] not in self.pareto_points:
                        self.pareto_points.append(vertex["objects"][0])
                        self.solution_path += f"\nWe also add the vertex {vertex['objects'][0] + 1} to the Pareto front."
                    entries.remove(vertex)
                if len(entries) == 0:
                    maybe_to_remove.append(obj[0])
            else:
                seg = obj[3]    # a segment that starts on the line of the walked segment and runs along it
                if obj[4] == -2:
                    if seg["end"][1] < current_x2_value or (abs(seg["end"][1] - current_x2_value) <= EPS and seg["end"][0] <= current_x1_value):
                        self.pareto_points.append([seg["edge"], seg["t"]])
                        maybe_to_remove.append((seg, obj[0]))
                        self.solution_path += f"\nWe also add the edge segment on edge ({seg['edge'][0] + 1}, {seg['edge'][1] + 1}) in the range t=[{seg['t'][0]:.4f}, {seg['t'][1]:.4f}] to the Pareto front."
                    elif seg["start"][1] < current_x2_value and not (abs(seg["start"][1] - current_x2_value) <= EPS and abs(seg["start"][0] - current_x1_value) <= EPS):
                        new_t_value = seg["t"][0] + (seg["t"][1] - seg["t"][0]) * (current_x2_value - seg["start"][1]) / (seg["end"][1] - seg["start"][1])
                        self.pareto_points.append([(seg["edge"][0], seg["edge"][1]), [seg["t"][0], new_t_value]])
                        self.solution_path += f"\nWe also add the edge segment on edge ({seg['edge'][0] + 1}, {seg['edge'][1] + 1}) in the range t=[{seg['t'][0]:.4f}, {new_t_value:.4f}] to the Pareto front."
                        seg["t"][0], seg["start"][0], seg["start"][1] = new_t_value, x1_end_of_the_segment, current_x2_value
                elif obj[4] == -3:
                    if seg["start"][1] < current_x2_value and not (abs(seg["start"][1] - current_x2_value) <= EPS and abs(seg["start"][0] - current_x1_value) <= EPS):
                        new_t_value = seg["t"][0] + (seg["t"][1] - seg["t"][0]) * (current_x2_value - seg["start"][1]) / (seg["end"][1] - seg["start"][1])
                        self.pareto_points.append([(seg["edge"][0], seg["edge"][1]), [seg["t"][0], new_t_value]])
                        self.solution_path += f"\nWe also add the edge segment on edge ({seg['edge'][0] + 1}, {seg['edge'][1] + 1}) in the range t=[{seg['t'][0]:.4f}, {new_t_value:.4f}] to the Pareto front."
                        seg["t"][0], seg["start"][0], seg["start"][1] = new_t_value, x1_end_of_the_segment, current_x2_value
        return maybe_to_remove

    def _adding_pareto_points(self, next_obj):
        """
        Adds the chosen objects to the Pareto points: vertices and edges with constant values directly; the
        segments are returned so that the next segment can be chosen from them.

        :return: the segments among next_obj
        """
        potential_segments = []
        for obj in next_obj:
            if isinstance(obj, int) or isinstance(obj, float)  or isinstance(obj, np.int64):
                if obj not in self.pareto_points:
                    self.pareto_points.append(obj)
                    self.solution_path += f"\nVertex {obj + 1} is part of the Pareto front."
            elif isinstance(obj, dict):
                potential_segments.append(obj)
            elif isinstance(obj, list) and len(obj) == 2:   # the complete edge [[(a, b), 0], [(a, b), 1]]
                if len(obj[0]) == 2 and len(obj[1]) == 2:
                    if obj[0][1] == 0 and obj[1][1] == 1:
                        self.pareto_points.append(obj)
                        self.solution_path += f"\nEdge ({obj[0][0][0] + 1}, {obj[0][0][1] + 1}) is part of the Pareto front."
        return potential_segments

    def _determining_next_segment(self, potential_segments):
        """
        Chooses the segment to walk next among the segments that start at the current Pareto point: the one
        with the smallest increase of f^2 per decrease of f^1; of segments with the same slope the one that
        reaches furthest. The others with the same slope are checked after the step (_check_later).

        :return: [segment to walk, the other segments with the same slope]
        """
        segments_to_check = []
        best_slope = BIGM
        for seg in potential_segments:
            # Increase of f^2 per decrease of f^1
            slope = (seg["end"][1] - seg["start"][1]) / (seg["start"][0] - seg["end"][0])
            if slope <= best_slope + EPS:
                if slope < best_slope - EPS:
                    best_slope = slope
                    segments_to_check = []
                    segment = seg
                else:
                    segments_to_check.append(seg)
                    if seg["end"][0] < segment["end"][0]:
                        segments_to_check.append(segment)
                        segment = seg
                        segments_to_check.pop(-2)
        self.solution_path += f"\nWe continue examining the edge segment on edge ({segment['edge'][0] + 1}, {segment['edge'][1] + 1}) in the range t=[{segment['t'][0]:.4f}, {segment['t'][1]:.4f}]."
        return [segment, segments_to_check]

    def _remove_chosen(self, maybe_to_remove, it_is_segment):
        """
        Removes the parts chosen in this step from the images: whole images (index), point entries ((index,
        entry), found by the entry itself) and, after a segment step, segments ((segment, index), found by their
        start t). Images without entries are removed.
        """
        points_to_remove = []
        for rmv in maybe_to_remove:
            if isinstance(rmv, int):
                points_to_remove.append(rmv)
            elif len(rmv) == 2 and isinstance(rmv[0], int):
                # a point entry of an image: found by the entry itself, because the positions in the image
                # can change during a step (_check_later removes entries); it may already be gone
                entries = self.im[rmv[0]]["entries"]
                for k, entry in enumerate(entries):
                    if entry is rmv[1]:
                        entries.pop(k)
                        break
                if len(entries) == 0:
                    points_to_remove.append(rmv[0])
            else:
                if it_is_segment:
                    entries = self.im[rmv[1]]["entries"]
                    segm_to_remove = []
                    for idx3, segm in enumerate(entries):
                        if segm["type"] == "segment":
                            if abs(segm["t"][0] - rmv[0]["t"][0]) <= EPS:
                                segm_to_remove.append(idx3)
                    segm_to_remove.sort(reverse=True)
                    for idx in segm_to_remove:
                        entries.pop(idx)
                    if len(entries) == 0:
                        points_to_remove.append(rmv[1])

        points_to_remove = sorted(set(points_to_remove), reverse=True)
        for idx in points_to_remove:
            self.im.pop(idx)

    def _remove_dominated(self, current_x1_value, current_x2_value):
        """
        Removes the image parts that the walk has passed at the point (current_x1_value, current_x2_value):
        points with an f^1 of at least the current one, and segments that start to the right of or above this
        point; segments that cross the vertical line f^1 = current f^1 are cut there.
        """
        to_remove = []
        for idx, im_e in enumerate(self.im):
            entries = im_e["entries"]
            if im_e["kind"] == "points":
                if len(entries) == 1:
                    if entries[0]["value"][0] >= current_x1_value - EPS:
                        to_remove.append(idx)
                elif len(entries) == 2:
                    if entries[1]["value"][0] >= current_x1_value - EPS:
                        entries.pop(1)
                    if entries[0]["value"][0] >= current_x1_value - EPS:
                        entries.pop(0)
                    if len(entries) == 0:
                        to_remove.append(idx)
            else:
                to_delete = []
                if entries[0]["type"] == "point":
                    if entries[0]["value"][0] >= current_x1_value - EPS:
                        to_delete.append(0)
                if entries[-1]["type"] == "point":
                    if entries[-1]["value"][0] >= current_x1_value - EPS:
                        to_delete.append(len(entries) - 1)
                for idx2, segment in enumerate(entries):
                    if segment["type"] == "segment":
                        if segment["start"][0] > current_x1_value + EPS or (abs(segment["start"][0] - current_x1_value) <= EPS and segment["start"][1] > current_x2_value + EPS):
                            if segment["end"][0] >= current_x1_value - EPS:
                                if idx2 not in to_delete:
                                    to_delete.append(idx2)
                                    self.solution_path += f"\nEdge segment on edge ({segment['edge'][0] + 1}, {segment['edge'][1] + 1}) in the range t=[{segment['t'][0]:.4f}, {segment['t'][1]:.4f}] is dominated and hence not further considered."
                            else:
                                slope = (segment["end"][1] - segment["start"][1]) / (segment["end"][0] - segment["start"][0])
                                intersec = segment["end"][1] - slope * segment["end"][0]
                                new_x2_value = slope * current_x1_value + intersec
                                new_t1_value = segment["t"][0] + (segment["t"][1] - segment["t"][0]) * (current_x1_value - segment["start"][0]) / (segment["end"][0] - segment["start"][0])
                                segment["t"][0], segment["start"][0], segment["start"][1] = new_t1_value, current_x1_value, new_x2_value
                                self.solution_path += f"\nEdge segment on edge ({segment['edge'][0] + 1}, {segment['edge'][1] + 1}) in the range t=[{segment['t'][0]:.4f}, {segment['t'][1]:.4f}] is dominated."
                to_delete = sorted(set(to_delete), reverse=True)   # every index only once
                for idx2 in to_delete:
                    entries.pop(idx2)
                if len(entries) == 0:
                    to_remove.append(idx)
        to_remove = sorted(set(to_remove), reverse=True)
        for idx in to_remove:
            self.im.pop(idx)


    def _results_bicriteria(self):
        """
        Result of the bicriteria case: the Pareto points as vertex numbers, complete edges ((i, j), (0, 1)) and
        parts of edges ((i, j), (t1, t2)) (all 1-based), and the objective function frontier as points and line
        segments in the objective function space (a segment that lies inside another one is left out).

        :return: (Pareto set, result text, solution path, None)
        """
        self.solution_path += f"\nMedian for the first objective function is reached. Terminate the algorithm."
        print_string = []
        obj_string = []

        for p in self.pareto_points:
            if isinstance(p, int):
                print_string.append(p + 1)
                obj1 = self.col_sums[0, p]
                obj2 = self.col_sums[1, p]
                if (obj1, obj2) not in obj_string:
                    obj_string.append((obj1, obj2))
            elif isinstance(p[0], list):
                # the complete edge with constant objective function values
                a, b = int(p[0][0][0]), int(p[0][0][1])
                print_string.append(((a + 1, b + 1), (0, 1)))
                if (self.col_sums[0, a], self.col_sums[1, a]) not in obj_string:
                    obj_string.append((self.col_sums[0, a], self.col_sums[1, a]))
            else:
                obj1_p1 =  AdditionalMethods.calculate_weighted_distance_point(((p[0][0], p[0][1]), p[1][0]), self.distances, self.matrix, self.weights[0])
                obj2_p1 =  AdditionalMethods.calculate_weighted_distance_point(((p[0][0], p[0][1]), p[1][0]), self.distances, self.matrix, self.weights[1])
                obj1_p2 =  AdditionalMethods.calculate_weighted_distance_point(((p[0][0], p[0][1]), p[1][1]), self.distances, self.matrix, self.weights[0])
                obj2_p2 =  AdditionalMethods.calculate_weighted_distance_point(((p[0][0], p[0][1]), p[1][1]), self.distances, self.matrix, self.weights[1])
                changed = 0
                for idx, o in enumerate(obj_string):
                    if isinstance(o, list):
                        if obj1_p1 >= o[0][0] and obj1_p2 <= o[1][0]:
                            obj_string[idx] = [[obj1_p1, obj2_p1], [obj1_p2, obj2_p2]]
                            changed = 1
                        elif obj1_p1 <= o[0][0] and obj1_p2 >= o[1][0]:
                            changed = 1
                if changed == 0:
                    obj_string.append([[obj1_p1, obj2_p1], [obj1_p2, obj2_p2]])
                print_string.append(((p[0][0] + 1, p[0][1] + 1), (p[1][0], p[1][1])))
        set_string = set(print_string)
        obj_string = pareto_median_undirected_network.remove_numpy_types(obj_string)
        result_string = f'Pareto frontier {pareto_median_undirected_network.format_numbers(set_string)}\nObjective function frontier: {pareto_median_undirected_network.format_numbers(obj_string)}'

        return print_string, result_string, self.solution_path, None

    @staticmethod
    def equal_values(f_x, f_y):
        """True if f_x and f_y are equal in every objective."""
        return all(abs(f_x[q] - f_y[q]) <= EPS for q in range(len(f_x)))

    @staticmethod
    def value_of_piece(piece, t):
        """Values (f^1, ..., f^Q) of a piece at t."""
        return [piece["b"][q] + piece["m"][q] * t for q in range(len(piece["m"]))]

    @staticmethod
    def deepcopy_list(lst):
        """
        Copy of a nested list (the lists are copied, the other items are not).
        """
        if not isinstance(lst, list):
            return lst

        new_list = []
        for item in lst:
            if isinstance(item, list):
                new_list.append(pareto_median_undirected_network.deepcopy_list(item))
            else:
                new_list.append(item)

        return new_list

    @staticmethod
    def describe(piece):
        """Text of a piece: vertex, edge with constant objective functions or linear subedge."""
        if piece["edge"] is None:
            return f"vertex {piece['vertex'] + 1}"
        a, b = piece["edge"]
        if piece.get("constant"):
            return f"the edge ({a+1}, {b+1})"
        return f"the linear subedge (({a+1}, {b+1}), [{piece['lo']:.4f}, {piece['hi']:.4f}])"

    @staticmethod
    def format_numbers(value):
        """Text of a number, or of numbers in sets, tuples and lists, with 4 decimals for decimal numbers."""
        if isinstance(value, float):
            return f"{value:.4f}"
        if isinstance(value, (set, tuple, list)):
            inner = ", ".join(pareto_median_undirected_network.format_numbers(v) for v in value)
            return {set: "{" + inner + "}", tuple: "(" + inner + ")", list: "[" + inner + "]"}[type(value)]
        return str(value)

    @staticmethod
    def remove_numpy_types(obj):
        """
        The same structure with numpy numbers turned into Python int and float (for the texts).
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, (list, tuple)):
            return type(obj)(pareto_median_undirected_network.remove_numpy_types(item) for item in obj)
        elif isinstance(obj, dict):
            return {pareto_median_undirected_network.remove_numpy_types(key): pareto_median_undirected_network.remove_numpy_types(value) for key, value in obj.items()}
        else:
            return obj

    @staticmethod
    def multiple_weighted_distances_calculations(distances, weights, nr_objectives, sol_path):
        """
        Weighted distance matrices w^q_i * d(i, j) and their column sums f^q(j) for every weight vector q
        (also used by pareto_median_undirected_network_vertex_restricted).

        :return: (weighted matrices, array with one row of column sums per weight vector, solution path)
        """
        weighted_distances = []
        col_sums = []
        for i in range(nr_objectives):
            weighted_matrix = AdditionalMethods.calculate_weighted_in_distances(distances, weights[i])
            sol_path += f"\nFor weight vector {i+1}, the network has the weighted distance matrix:\n{AdditionalMethods.format_matrix(weighted_matrix)}"
            weighted_distances.append(weighted_matrix)
            col_sum = weighted_distances[i].sum(axis=0)
            col_sums.append(col_sum)
            sol_path += f"\nAnd we get the column sums:\n{AdditionalMethods.format_vector(col_sum)}"
        col_sums = np.array(col_sums)
        weighted_distances = np.array(weighted_distances)
        return weighted_distances, col_sums, sol_path

    @staticmethod
    def pareto_vertices_determination(n, col_sums, sol_path):
        """
        Compares all pairs of vertices: vertex i dominates vertex j if f^q(i) <= f^q(j) for all q and
        f^q(i) < f^q(j) for at least one q (with the tolerance EPS). Also used by the vertex Pareto algorithms.

        :param n: number of vertices
        :param col_sums: col_sums[q][v] = f^q(v)
        :param sol_path: solution path so far
        :return: (vertices that no other vertex dominates (0-based), the pairs (i, j) where i dominates j,
                 solution path)
        """
        pareto_vertices = [i for i in range(n)]
        dominance_relation = []
        for i in range(n):
            for j in range(i+1,n):
                if np.all(col_sums[:,i] <= col_sums[:,j] + EPS) and np.any(col_sums[:,i] < col_sums[:,j] - EPS):
                    dominance_relation.append((i, j))
                    sol_path += f"\nVertex {i+1} dominates vertex {j+1}."
                    if j in pareto_vertices:
                        pareto_vertices.remove(j)
                        sol_path += f"\nRemove vertex {j+1} from consideration."
                elif np.all(col_sums[:,j] <= col_sums[:,i] + EPS) and np.any(col_sums[:,j] < col_sums[:,i] - EPS):
                    dominance_relation.append((j, i))
                    sol_path += f"\nVertex {j+1} dominates vertex {i+1}."
                    if i in pareto_vertices:
                        pareto_vertices.remove(i)
                        sol_path += f"\nRemove vertex {i+1} from consideration."
        return pareto_vertices, dominance_relation, sol_path

    @staticmethod
    def vertex_check(maybe_to_remove, next_obj, point, current_x1_value, current_x2_value, mtr, no):
        """
        Point step: compares the point entry `point` with the best candidate so far (current values). The point
        becomes the candidate if there is none yet, if it has a smaller f^2, or the same f^2 and a smaller
        f^1; with the same values it is added to the candidates.

        :param mtr: what to remove from the images if this point is chosen
        :param no: the locations of the point (vertex, or vertices and complete edge)
        :return: (maybe_to_remove, next_obj, current_x1_value, current_x2_value)
        """
        if len(next_obj) == 0:
            for obj in no:
                if obj not in next_obj:
                    next_obj.append(obj)
            current_x1_value = point["value"][0]
            current_x2_value = point["value"][1]
            maybe_to_remove = [mtr]
        elif abs(current_x1_value - point["value"][0]) <= EPS and abs(current_x2_value - point["value"][1]) <= EPS:
            for obj in no:
                if obj not in next_obj:
                    next_obj.append(obj)
            maybe_to_remove.append(mtr)
        elif current_x2_value > point["value"][1] + EPS:
            next_obj = [obj for obj in no]
            current_x1_value = point["value"][0]
            current_x2_value = point["value"][1]
            maybe_to_remove = [mtr]
        elif current_x1_value > point["value"][0] + EPS and current_x2_value >= point["value"][1] - EPS:
            next_obj = [obj for obj in no]
            current_x1_value = point["value"][0]
            current_x2_value = point["value"][1]
            maybe_to_remove = [mtr]
        return maybe_to_remove, next_obj, current_x1_value, current_x2_value

    @staticmethod
    def constant_objective_function_part(point, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, the_slope, the_intersec, sub_iterator, mtr, no, ltc):
        """
        Segment step: compares a point entry with the walked segment (line x2 = the_slope * x1 + the_intersec)
        and the stop of the walk so far (current values). A point with the same values as the stop is added to
        the candidates; a point with the same f^2 and a smaller f^1, or a point with a smaller f^2 below the
        line, becomes the new stop; a point with a smaller f^2 exactly on the line is noted in later_to_check.

        :param sub_iterator: the locations to add if the point has the same values as the stop
        :param mtr: what to remove from the images if this point is chosen
        :param no: the locations of the point
        :param ltc: the entry for later_to_check
        :return: (maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value)
        """
        if abs(point["value"][1] - current_x2_value) <= EPS and abs(point["value"][0] - current_x1_value) <= EPS:
            for obj in sub_iterator:
                if obj not in next_obj:
                    next_obj.append(obj)
            maybe_to_remove.append(mtr)
        elif abs(point["value"][1] - current_x2_value) <= EPS and point["value"][0] < current_x1_value:
            next_obj = no
            maybe_to_remove = [mtr]
            current_x1_value = point["value"][0]
        elif point["value"][1] < current_x2_value - EPS:
            if abs(point["value"][1] - (the_slope * point["value"][0] + the_intersec)) <= EPS:
                later_to_check.append(ltc)   # the vertex entry itself: the indices in the image can change
            elif point["value"][1] < the_slope * point["value"][0] + the_intersec:
                next_obj = no
                maybe_to_remove = [mtr]
                current_x1_value = point["value"][0]
                current_x2_value = point["value"][1]
        return maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value

    @staticmethod
    def non_constant_objective_function_part(im_e, segment, the_segment, the_slope, the_intersec, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value, idx, idx_seg):
        """
        Segment step: compares another segment with the walked segment (line x2 = the_slope * x1 + the_intersec)
        and the stop of the walk so far (current values). The other segment
          - starts at the stop: it is added to the candidates (with the same f^2 and a smaller f^1 its start
            becomes the new stop);
          - starts below the line with a smaller f^2: its start becomes the new stop;
          - starts on the line: if it runs below the line, its start becomes the new stop; if it runs along
            the line, it is noted in later_to_check (-2: it ends before the stop, -3: it reaches beyond it;
            then the part after the stop is a candidate if the stop is the end of the walked segment);
          - starts above the line: if it crosses the line before the stop, it is cut at the intersection,
            which becomes the new stop (or a further candidate at the stop).

        :return: (segment, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value)
        """
        if abs(segment["start"][1] - current_x2_value) <= EPS:
            if abs(segment["start"][0] - current_x1_value) <= EPS:
                next_obj.append(segment)
            elif segment["start"][0] < current_x1_value:
                next_obj = [segment]
                maybe_to_remove = [(segment, idx)]
                current_x1_value = segment["start"][0]
        elif segment["start"][1] < current_x2_value:
            if segment["start"][1] < the_slope * segment["start"][0] + the_intersec - EPS:
                next_obj = [segment]
                maybe_to_remove = [(segment, idx)]
                current_x2_value = segment["start"][1]
                current_x1_value = segment["start"][0]
            elif abs(segment["start"][1] - (the_slope * segment["start"][0] + the_intersec)) <= EPS:
                slope = (segment["end"][1] - segment["start"][1]) / (segment["end"][0] - segment["start"][0])
                intersec = segment["end"][1] - slope * segment["end"][0]
                end_on_line = the_slope * segment["end"][0] + the_intersec   # the line of the current segment at the end of this segment
                if segment["end"][1] > end_on_line + EPS:
                    pass
                elif abs(segment["end"][1] - end_on_line) <= EPS:     # on the line: collinear
                    if segment["end"][1] <= current_x2_value + EPS:
                        later_to_check.append((idx, im_e, idx_seg, segment, -2))
                    else:
                        t_split = segment["t"][0] + (segment["t"][1] - segment["t"][0]) * (current_x2_value - segment["start"][1]) / (segment["end"][1] - segment["start"][1])
                        obj_split = (current_x2_value - intersec) / slope
                        if abs(the_segment["end"][0] - current_x1_value) <= EPS and abs(the_segment["end"][1] - current_x2_value) <= EPS:
                            later_to_check.append((idx, im_e, idx_seg, segment, -3))
                            segment1 = {"type": "segment", "edge": (segment["edge"][0], segment["edge"][1]), "t": [t_split, segment["t"][1]], "start": [obj_split, current_x2_value], "end": [segment["end"][0], segment["end"][1]]}
                            next_obj.append(segment1)
                        else:
                            later_to_check.append((idx, im_e, idx_seg, segment, -3))
                else:
                    next_obj = [segment]
                    maybe_to_remove = [(segment, idx)]
                    current_x2_value = segment["start"][1]
                    current_x1_value = segment["start"][0]
            else:
                slope = (segment["end"][1] - segment["start"][1]) / (segment["end"][0] - segment["start"][0])
                intersec = segment["end"][1] - slope * segment["end"][0]
                x2_intersection = (intersec - slope * the_intersec / the_slope) / (1 - slope / the_slope)
                x1_intersection = (x2_intersection - intersec) / slope
                t_intersection = segment["t"][0] + (segment["t"][1] - segment["t"][0]) * (x2_intersection - segment["start"][1]) / (segment["end"][1] - segment["start"][1])
                if x2_intersection >= segment["start"][1] - EPS and x2_intersection < segment["end"][1] - EPS and x2_intersection <= current_x2_value + EPS:
                    if abs(x2_intersection - current_x2_value) <= EPS and abs(x1_intersection - current_x1_value) <= EPS:
                        segment["t"][0], segment["start"][0], segment["start"][1] = t_intersection, x1_intersection, x2_intersection
                        next_obj.append(segment)
                    elif x2_intersection < current_x2_value:
                        segment["t"][0], segment["start"][0], segment["start"][1] = t_intersection, x1_intersection, x2_intersection
                        next_obj = [segment]
                        maybe_to_remove = [(segment, idx)]
                        current_x2_value = x2_intersection
                        current_x1_value = x1_intersection
        return segment, maybe_to_remove, later_to_check, next_obj, current_x1_value, current_x2_value

    @staticmethod
    def dominated_part(A, B):
        """
        Part [LB, UB] of piece A whose points are dominated by points of piece B, None if there is none.
        As in the lecture: F is the set of all (s, t) with s in [B.lo, B.hi], t in [A.lo, A.hi] and
        f^q((B, s)) <= f^q((A, t)) for all q; LB = min{t | (s, t) in F}, UB = max{t | (s, t) in F}.
        If the images of A and B are equal at LB and at UB, no point of A is dominated by B.
        """
        Q = len(A["m"])
        value_of = pareto_median_undirected_network.value_of_piece

        # Quick test: B can only dominate a point of A if, in every objective, the smallest value of B
        # is not larger than the largest value of A
        for q in range(Q):
            smallest_B = min(value_of(B, B["lo"])[q], value_of(B, B["hi"])[q])
            largest_A = max(value_of(A, A["lo"])[q], value_of(A, A["hi"])[q])
            if smallest_B > largest_A + EPS:
                return None

        # Border lines of F in the form alpha * s + beta * t = gamma
        lines = []
        for q in range(Q):
            # B at s is not larger than A at t:  B.b + B.m * s <= A.b + A.m * t
            lines.append((-B["m"][q], A["m"][q], B["b"][q] - A["b"][q]))
        lines += [(1.0, 0.0, B["lo"]), (1.0, 0.0, B["hi"]), (0.0, 1.0, A["lo"]), (0.0, 1.0, A["hi"])]

        def in_F(s, t):
            if s < B["lo"] - EPS or s > B["hi"] + EPS or t < A["lo"] - EPS or t > A["hi"] + EPS:
                return False
            f_B = value_of(B, s)
            f_A = value_of(A, t)
            return all(f_B[q] <= f_A[q] + EPS for q in range(Q))

        # Corners of F: the intersections of two border lines that lie in F
        corners = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                alpha1, beta1, gamma1 = lines[i]
                alpha2, beta2, gamma2 = lines[j]
                determinant = alpha1 * beta2 - alpha2 * beta1
                if abs(determinant) < 1e-12:      # parallel lines
                    continue
                s = (gamma1 * beta2 - gamma2 * beta1) / determinant
                t = (alpha1 * gamma2 - alpha2 * gamma1) / determinant
                if in_F(s, t):
                    corners.append((s, t))
        if len(corners) == 0:
            return None

        LB = max(min(t for s, t in corners), A["lo"])
        UB = min(max(t for s, t in corners), A["hi"])
        equal_at_LB = all(pareto_median_undirected_network.equal_values(value_of(B, s), value_of(A, t))
                          for s, t in corners if abs(t - LB) <= EPS)
        equal_at_UB = all(pareto_median_undirected_network.equal_values(value_of(B, s), value_of(A, t))
                          for s, t in corners if abs(t - UB) <= EPS)
        if equal_at_LB and equal_at_UB:
            return None
        return (LB, UB)