import numpy as np
from common.additional_methods import AdditionalMethods

class center_undirected_network_absolute:
    """
    Absolute center on an undirected network: the point (vertex or point on an edge) that minimises the
    largest weighted shortest path length to a customer,
        f(x) = max_k w_k * d(v_k, x).

    Customer k reaches the point x(t) on the edge (i, j) at the fraction t of its length l via i or via j:
        w_k * d(v_k, x(t)) = w_k * min(d(k, i) + t l, d(k, j) + (1 - t) l).
    This function increases with slope w_k l up to its breakpoint
        T_k = (d(k, j) - d(k, i) + l) / (2 l)
    and decreases with slope -w_k l afterwards. On every edge the algorithm follows the upper envelope
    g(t) = max_k w_k * d(v_k, x(t)) from t = 0 to t = 1. Its local minima lie at t = 0, at t = 1 and where
    a decreasing piece meets an increasing one. The smallest of these values over all edges is the optimal
    value, and all points that reach it are returned.

    :param weights: weight w_k of every vertex (customers have w_k > 0; vertices with w_k = 0 need not be
                    reached)
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

    
    def run(self):
        """
        Runs the algorithm.

        :return: (optimal points, result text, solution path, None); the optimal points are ((i, j), t) for a
                 point inside the edge (i, j) at the fraction t of its length from i, followed by the optimal
                 vertices as vertex numbers (1-based);
                 if the customers are not connected: ([], "No result: ..." text, solution path, None)
        """
        n = len(self.matrix)
        relevant_vertices = [v for v in range(n) if self.weights[v] != 0]  # the customers

        # Calculating the distance matrix of the network
        distances = AdditionalMethods.floyd_warshall(self.matrix)
        self.solution_path += f"The network has the distance matrix:\n{AdditionalMethods.format_matrix(distances)}"

        # If the customers are not connected, no point has a finite objective function value
        if not AdditionalMethods.location_exists(distances, self.weights, "undirected"):
            return AdditionalMethods.no_location_result("center", "undirected", self.solution_path)

        # Only one customer: its vertex is the center, with value 0
        if len(relevant_vertices) == 1:
            self.solution_path = f"The network has only one (weighted) vertex so the result is trivial."
            result_string = f'Optimal point: {", ".join(f"on vertex {v+1}" for v in relevant_vertices)}\nObjective function value: {0:.4f}'
            return [relevant_vertices[0] + 1], result_string, self.solution_path, None

        # No customer (every weight is 0): every point has the value 0; the vertices are given as optimal
        if not relevant_vertices:
            self.solution_path += "\nNo vertex has a weight greater than 0 (no customer): every point of the network has the objective function value 0, so every vertex is optimal."
            places = f'Multiple optimal points: {", ".join(f"on vertex {v}" for v in range(1, n + 1))}' if n > 1 else "Optimal point: on vertex 1"
            return list(range(1, n + 1)), f"{places}\nObjective function value: {0:.4f}", self.solution_path, None

        # Calculating the weighted distance matrix
        weighted_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)
        self.solution_path += f"\nThe network has the weighted distance matrix:\n{AdditionalMethods.format_matrix(weighted_distances)}"

        # For each edge, we calculate the breakpoints and subsequently, the local minima
        edges = AdditionalMethods.get_edges(self.matrix, "undirected")

        center_vertices = []
        center_value = np.inf
        center_position = []
        for e in edges:
            # Breakpoints T[k]: up to T[k] customer k reaches the point via e[0], afterwards via e[1]
            T, T_print = AdditionalMethods._breakpoints(e, n, distances, self.matrix)
            self.solution_path += f"\nEdge ({e[0]+1}, {e[1]+1}) has the breakpoints [{', '.join('–' if np.isnan(t) else f'{t:.4f}' for t in T_print)}]. We calculate the upper envelope:"   

            # Determine the first upper envelope vertex (if there are multiple at vertex e[0], we take the one with
            # the steepest ascent)
            start, sign = self._first_envelope_vertex(e, weighted_distances)

            # Setting starting values 
            min_max = weighted_distances[start, e[0]]
            t_min = [0]  # positions of the smallest value found on this edge
            g_min = min_max  # smallest value of g found on this edge

            self.solution_path += f"\nAt point (({e[0]+1}, {e[1]+1}), {0}) we have an objective function value g(x) = {g_min:.4f}."

            vertex = start
            not_finished = True
            current_t = 0

            while not_finished:
                # For increasing line segment
                if sign == 1:
                    # Next event: the breakpoint of `vertex` (the envelope starts to decrease) or a steeper
                    # increasing function that crosses it
                    inters, not_switched, next_vertex = self._next_on_increasing(e, vertex, current_t, T, relevant_vertices, weighted_distances)

                    # Determining next steps
                    if inters == 1:  # end of the edge reached
                        not_finished = False
                        self.solution_path += f"\nNo more relevant intersection on edge ({e[0]+1}, {e[1]+1}). Go to evaluation at vertex {e[1]+1}."
                        break
                    current_t = inters
                    if not_switched:
                        sign = -1
                        self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), upper envelope reaches breakpoint from vertex {vertex+1} at t = {inters:.4f}."
                    else:
                        if self.weights[vertex] == self.weights[next_vertex] and np.isclose(weighted_distances[vertex, e[0]], weighted_distances[next_vertex, e[0]]) and T[vertex] < T[next_vertex]:
                            self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), we switch from considering vertex {vertex+1} to vertex {next_vertex+1} as it has later breakpoint t = {inters:.4f}."
                        else:
                            self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), intersection from increasing distance function of vertex {vertex+1} and steeper increasing distance function of vertex {next_vertex+1} at t = {inters:.4f}."
                        vertex = next_vertex
                    
                # Case of decreasing distance function
                elif sign == -1:
                    # Next event: a less steeply decreasing function (the envelope keeps decreasing) or an
                    # increasing function (a local minimum of the envelope)
                    inters, not_switched, next_vertex = self._next_on_decreasing(e, vertex, current_t, T, relevant_vertices, weighted_distances)
                    
                    # Determining next steps
                    if inters == 1:  # end of the edge reached
                        not_finished = False
                        self.solution_path += f"\nNo more relevant intersection on edge ({e[0]+1}, {e[1]+1}). Go to evaluation at vertex {e[1]+1}."
                        break
                    current_t = inters
                    old_vertex = vertex
                    vertex = next_vertex
                    if not_switched:
                        self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), intersection from decreasing distance function of vertex {old_vertex+1} and steeper decreasing distance function of vertex {next_vertex+1} at t = {inters:.4f}."
                        sign = -1
                    else:  # local minimum: compare it with the best value of this edge
                        sign = 1
                        g = weighted_distances[vertex, e[0]] + current_t * self.weights[vertex] * self.matrix[e[0], e[1]]
                        self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), intersection from decreasing distance function of vertex {old_vertex+1} and increasing distance function of vertex {next_vertex+1} at t = {inters:.4f}."
                        if np.isclose(g, g_min):
                            self.solution_path += f"\nFurther minima of upper envelope on edge ({e[0]+1}, {e[1]+1}) found with objective function value g(x) = {g_min:.4f}."
                            t_min.append(current_t)
                        elif g < g_min:
                            g_min = g
                            t_min = [current_t]
                            self.solution_path += f"\nNew minima of upper envelope on edge ({e[0]+1}, {e[1]+1}) found with objective function value g(x) = {g_min:.4f}."
                        
            # Evaluating functions at end vertex of the edge
            last_g = np.max(weighted_distances[:, e[1]])
            self.solution_path += f"\nAt point (({e[0]+1}, {e[1]+1}), {1}) we have an objective function value g(x) = {last_g:.4f}."
            if np.isclose(last_g, g_min):
                t_min.append(1)
            elif last_g < g_min:
                g_min = last_g
                t_min = [1]
            self.solution_path += f"\nMinima of upper envelope of edge ({e[0]+1}, {e[1]+1}) at point(s) [{', '.join(f'{i}' for i in t_min)}] with objective function value g(x) = {g_min:.4f}."

            # Comparing with other edges
            if np.isclose(center_value, g_min):
                center_position.append((e, t_min))
                not_vertex, center_vertices = self._record_edge(e, t_min, center_vertices, center_value, 0)
            elif center_value > g_min:
                center_value = g_min
                center_position = [(e, t_min)]
                center_vertices = []
                not_vertex, center_vertices = self._record_edge(e, t_min, center_vertices, center_value, 1)            

        self.solution_path += f"\nAll edges have been examined."

        # Determining print
        center_position_print, result_string = self._result_text(center_position, center_vertices, center_value)

        return center_position_print, result_string, self.solution_path, None



    def _first_envelope_vertex(self, e, weighted_distances):
        """
        The function that forms the upper envelope directly after t = 0: among the customers with the largest
        weighted distance at e[0], the one whose function increases most steeply, or, if all of them
        decrease, the one that decreases the least.

        :return: (customer, sign): sign 1 if its function increases, -1 if it decreases
        """
        start_indices = np.where(np.isclose(weighted_distances[:, e[0]], np.max(weighted_distances[:, e[0]])))[0]
        weights_start_indices = []
        for v in start_indices:
            if np.isclose(weighted_distances[v, e[0]], weighted_distances[v, e[1]] + self.weights[v] * self.matrix[e[0], e[1]]):
                weights_start_indices.append(- self.weights[v])
            else: 
                weights_start_indices.append(self.weights[v])
        vert_max = np.argmax(weights_start_indices)
        start = start_indices[vert_max]
        if weights_start_indices[vert_max] < 0:
            sign = -1
        else: 
            sign = 1
        return start, sign

    def _next_on_increasing(self, e, vertex, t, T, relevant_vertices, weighted_distances):
        """
        Next event while the envelope follows the increasing function of `vertex` from position t: the
        breakpoint T[vertex] (the function starts to decrease) or the first intersection with a steeper
        increasing function of another customer, which then forms the envelope. Of two functions with the
        same slope and the same values, the one with the later breakpoint is taken at once.

        :return: (position of the event, not_switched: True if the event is the breakpoint of `vertex`,
                 customer whose function forms the envelope after the event)
        """
        inters = T[vertex]
        not_switched = True
        w = 0
        next_vertex = vertex
        
        # Check all vertices
        for v in relevant_vertices:
            if v == vertex: continue

            # Case that two overlapping distance functions have the same slope -> Take the one with later breakpoint
            if self.weights[vertex] == self.weights[v] and np.isclose(weighted_distances[vertex, e[0]], weighted_distances[v, e[0]]) and T[vertex] < T[v]:
                inters = t
                not_switched = False
                next_vertex = v
                self.solution_path += f"\nOn edge ({e[0]+1}, {e[1]+1}), switch from increasing distance function of vertex {vertex+1} to increasing distance function of vertex {v+1} at t = {inters:.4f}. (Same slope but later breakpoint.)"
                break

            # Intersection with other increasing distance functions
            if (t < T[v] and self.weights[vertex] < self.weights[v]):
                # Intersection of w_vertex * (d(vertex, e[0]) + t l) and w_v * (d(v, e[0]) + t l)
                the_intersection = (weighted_distances[vertex, e[0]] - weighted_distances[v, e[0]]) / (self.matrix[e[0], e[1]] * (self.weights[v] - self.weights[vertex]))
                if the_intersection < T[v] and (t < the_intersection or np.isclose(t, the_intersection)):
                    if the_intersection < inters:
                        w = self.weights[v]
                        inters = the_intersection
                        not_switched = False
                        next_vertex = v
                    elif np.isclose(the_intersection, inters) and self.weights[v] > w:
                        w = self.weights[v]
                        inters = the_intersection
                        not_switched = False
                        next_vertex = v
        return inters, not_switched, next_vertex

    def _next_on_decreasing(self, e, vertex, t, T, relevant_vertices, weighted_distances):
        """
        Next event while the envelope follows the decreasing function of `vertex` from position t: the first
        intersection with the function of another customer that lies above it afterwards, either a less
        steeply decreasing function (the envelope keeps decreasing) or an increasing function (a local
        minimum of the envelope).

        :return: (position of the event (1 = end of the edge, no event), not_switched: True if the envelope
                 keeps decreasing, False if it increases afterwards, customer whose function forms the
                 envelope after the event)
        """
        inters = 1
        not_switched = True
        w = 0
        next_vertex = vertex

        # Check all vertices
        for v in relevant_vertices:
            if v == vertex: continue

            # Intersection with other decreasing lines
            if ((t > T[v] or np.isclose(t, T[v])) and self.weights[vertex] > self.weights[v]):
                # Intersection of the two decreasing functions w * (d(., e[1]) + (1 - t) l)
                the_intersection = (weighted_distances[vertex, e[1]] - weighted_distances[v, e[1]] + self.weights[vertex] * self.matrix[e[0], e[1]] - self.weights[v] * self.matrix[e[0], e[1]]) / (self.matrix[e[0], e[1]] * (self.weights[vertex] - self.weights[v]))
                if t < the_intersection or np.isclose(t, the_intersection):
                    if the_intersection < inters:
                        w, inters, not_switched, next_vertex = self.weights[v], the_intersection, True, v
                    elif np.isclose(the_intersection, inters) and self.weights[v] < w and not_switched:
                        w, not_switched, next_vertex = self.weights[v], True, v

            # Intersection with increasing lines
            elif (t < T[v]):
                # Intersection of the decreasing function of `vertex` and the increasing function of v
                the_intersection = (weighted_distances[vertex, e[1]] - weighted_distances[v, e[0]] + self.weights[vertex] * self.matrix[e[0], e[1]]) / (self.matrix[e[0], e[1]] * (self.weights[vertex] + self.weights[v]))
                if (the_intersection < T[v] or np.isclose(the_intersection, T[v])) and (t < the_intersection or np.isclose(t, the_intersection)):
                    if the_intersection < inters:
                        if the_intersection < T[v]:
                            w, inters, not_switched, next_vertex = self.weights[v], the_intersection, False, v
                        elif self.weights[vertex] > self.weights[v]:
                            w, inters,  not_switched, next_vertex = self.weights[v], the_intersection, True, v
                    elif np.isclose(the_intersection, inters):
                        if not_switched:
                            if the_intersection < T[v]:
                                w, not_switched, next_vertex = self.weights[v], False, v
                            elif self.weights[next_vertex] > self.weights[v]:
                                w, not_switched, next_vertex = self.weights[v], True, v
                        elif the_intersection < T[v]:
                            if self.weights[v] == w:
                                if T[next_vertex] < T[v]:
                                    w, not_switched, next_vertex = self.weights[v], False, v
                            elif self.weights[v] > w:
                                w, not_switched, next_vertex = self.weights[v], False, v
                elif self.weights[vertex] > self.weights[v]:
                    # v reaches its breakpoint before the intersection: intersection with the decreasing part of v
                    the_intersection = (weighted_distances[vertex, e[1]] - weighted_distances[v, e[1]] + self.weights[vertex] * self.matrix[e[0], e[1]] - self.weights[v] * self.matrix[e[0], e[1]]) / (self.matrix[e[0], e[1]] * (self.weights[vertex] - self.weights[v]))
                    if t < the_intersection or np.isclose(t, the_intersection):
                        if the_intersection < inters:
                            w, inters, not_switched, next_vertex = self.weights[v], the_intersection, True, v
                        elif np.isclose(the_intersection, inters) and self.weights[v] < w and not_switched:
                            w, not_switched, next_vertex = self.weights[v], True, v
        return inters, not_switched, next_vertex

    def _record_edge(self, e, t_min, center_vertices, center_value, new):
        """
        Adds the end vertices of the edge e that are among its minima (t = 0 or t = 1) to the optimal vertices
        and writes the solution path.

        :param t_min: positions of the minima on e
        :param new: 1 if e has a new best value, 0 if it has the same value as the best one so far
        :return: (True if a minimum lies inside the edge, the optimal vertices (0-based))
        """
        not_vertex = False
        for p in t_min:
            if np.isclose(p, 0):
                if e[0] not in center_vertices:
                    center_vertices.append(e[0])
                    if new:
                        self.solution_path += f"\nNew best point found on vertex {e[0]+1} with objective function value g(x) = {center_value:.4f}."
                    else:
                        self.solution_path += f"\nFurther best point found on vertex {e[0]+1} with objective function value g(x) = {center_value:.4f}."
            elif np.isclose(p, 1):
                if e[1] not in center_vertices:
                    center_vertices.append(e[1])
                    if new:
                        self.solution_path += f"\nNew best point found on vertex {e[1]+1} with objective function value g(x) = {center_value:.4f}."
                    else:
                        self.solution_path += f"\nFurther best point found on vertex {e[1]+1} with objective function value g(x) = {center_value:.4f}."
            else:
                not_vertex = True
        if not_vertex:
            if new:
                self.solution_path += f"\nNew best point(s) found on edge ({e[0]+1}, {e[1]+1}) with objective function value g(x) = {center_value:.4f}."
            else:
                self.solution_path += f"\nFurther best point(s) found on edge ({e[0]+1}, {e[1]+1}) with objective function value g(x) = {center_value:.4f}."
        return not_vertex, center_vertices

    @staticmethod
    def _result_text(center_position, center_vertices, center_value):
        """
        Output list and result text: the points inside edges as ((i, j), t) (t rounded to 4 decimals),
        followed by the optimal vertices as vertex numbers (both 1-based).

        :return: (optimal points, result text)
        """
        center_position_print = []
        
        for p in center_position:
            v1 = int(p[0][0]) + 1
            v2 = int(p[0][1]) + 1
            for i in p[1]:
                if not (np.isclose(i, 0) or np.isclose(i, 1)):
                    position = round(float(i), 4)
                    center_position_print.append(((v1, v2), position))

        # Output
        if len(center_position_print) + len(center_vertices) >= 2:
            if len(center_vertices) == 0:
                result_string = f'Multiple optimal points: {", ".join(f"on edge ({e[0]}, {e[1]}) at t = {t:.4f}" for e, t in center_position_print)}\nObjective function value: {center_value:.4f}'
            elif len(center_position_print) == 0:
                result_string = f'Multiple optimal points: {", ".join(f"on vertex {v+1}" for v in center_vertices)}\nObjective function value: {center_value:.4f}'
            else:
                result_string = f'Multiple optimal points: {", ".join(f"on edge ({e[0]}, {e[1]}) at t = {t:.4f}" for e, t in center_position_print)} and {", ".join(f"on vertex {v+1}" for v in center_vertices)}\nObjective function value: {center_value:.4f}'
        else:
            if len(center_vertices) == 0:
                result_string = f'Optimal point: {", ".join(f"on edge ({e[0]}, {e[1]}) at t = {t:.4f}" for e, t in center_position_print)}\nObjective function value: {center_value:.4f}'
            else:
                result_string = f'Optimal point: {", ".join(f"on vertex {v+1}" for v in center_vertices)}\nObjective function value: {center_value:.4f}'

        for p in center_vertices:
            center_position_print.append(p+1)

        return center_position_print, result_string