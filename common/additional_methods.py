# common/additional_methods.py
import math

import numpy as np

class AdditionalMethods:
    """
    A utility class providing methods that can be used by all algorithms.
    """

    @staticmethod
    def distance_calculation_lp(point1, point2, coordinates, dimensions, p):
        """
        Distance calculation of two points with lp distance.
        Points can be in coordinate form or can be indexes if the 
        coordinates of all points are given
        """
        if type(point1)==int:
            point1=coordinates[point1].copy()
        if type(point2)==int:
            point2=coordinates[point2].copy()
        distance=pow(sum([pow(point1[i] - point2[i],p) for i in range(dimensions)]),1/p)
        return distance

    @staticmethod
    def floyd_warshall(matrix):
        """
        Floyd-Warshall algorithm for determining the distance matrix of a network.

        For every intermediate vertex k, numpy updates all pairs (i, j) at once:
            d(i, j) = min(d(i, j), d(i, k) + d(k, j)).
        This gives exactly the values of the three nested loops: row and column k do not change in step k,
        since d(k, k) = 0 and all lengths are positive.

        :param matrix: n x n adjacency matrix (list of lists or numpy array) with the edge lengths, None or np.inf
                       where there is no edge; the diagonal is ignored (it may hold "n")
        :return: numpy array of the shortest path lengths, np.inf where there is no path
        """
        n = len(matrix)
        lengths = np.array(matrix, dtype=object).reshape(n, n)
        np.fill_diagonal(lengths, None)
        edge = lengths != None              # elementwise for an object array
        dist = np.full((n, n), np.inf)
        dist[edge] = lengths[edge].astype(float)
        np.fill_diagonal(dist, 0)
        for k in range(n):
            np.minimum(dist, dist[:, k, None] + dist[None, k, :], out=dist)
        return dist

    @staticmethod
    def calculate_weighted_in_distances(matrix, weights):
        """
        Calculating the weighted distance matrix (in-median for directed networks so we have w*d, i.e., the distance from i to j is multiplied with the weight of i (w_i * d_ij))
        """
        with np.errstate(invalid="ignore"):   # 0 * inf: a customer with weight 0 need not be reached
            return np.where(weights[:, None] == 0, 0.0, weights[:, None] * matrix)

    @staticmethod
    def calculate_weighted_out_distances(matrix, weights):
        """
        Calculating the weighted distance matrix (out-median for directed networks so we have d*w, i.e., the distance from i to j is multiplied with the weight of j (w_j * d_ij))
        """
        with np.errstate(invalid="ignore"):   # 0 * inf: a customer with weight 0 need not be reached
            return np.where(weights[None, :] == 0, 0.0, matrix * weights[None, :])

    @staticmethod
    def location_exists(distances, weights, direction):
        """
        Checks whether a median or center can be determined, i.e. whether at least one vertex has a finite
        objective function value: it must reach every customer (vertex with a positive weight) and/or be
        reached by every customer. Customers with weight 0 do not have to be reached.

        :param distances: matrix of the shortest path lengths (np.inf if there is no path from i to j)
        :param weights: weights of the vertices
        :param direction: "in" (paths from the customers to the facility), "out" (paths from the facility
                          to the customers), "in_out" (both) or "undirected"
        :return: True if at least one vertex has a finite objective function value
        """
        customers = np.asarray(weights, dtype=float) > 0
        reaches_all = np.all(np.isfinite(distances[:, customers]), axis=1)      # vertex -> every customer
        reached_by_all = np.all(np.isfinite(distances[customers, :]), axis=0)   # every customer -> vertex
        if direction == "in":
            candidates = reached_by_all
        elif direction == "in_out":
            candidates = reaches_all & reached_by_all
        else:
            candidates = reaches_all
        return bool(np.any(candidates))

    @staticmethod
    def trivial_pareto_vertices(weights, edges):
        """
        The Pareto locations of a median with several weight vectors in two cases that need no search along the edges
        (the walk of the bicriteria approach only looks at edges and would find nothing):
          - all customers (vertices with a positive weight in at least one vector) are the same vertex v: v alone (all
            its values are 0, every other point has a positive value in an objective function where v has a weight);
          - there are no customers and no edges: every vertex (all values are 0).

        :return: the Pareto vertices (0-based), or None in every other case
        """
        weights = np.asarray(weights, dtype=float)
        customers = np.flatnonzero((weights > 0).any(axis=0))
        if len(customers) == 1:
            return [int(customers[0])]
        if len(customers) == 0 and len(edges) == 0:
            return list(range(weights.shape[1]))
        return None

    @staticmethod
    def no_location_result(location, direction, solution_path):
        """
        Result that a network algorithm returns instead of its solution if location_exists is False:
        nothing to mark, the reason as result string, the solution path so far and None (no CSV output).
        """
        reason = {
            "in": "no vertex is reached by all customers (vertices with a positive weight)",
            "out": "no vertex reaches all customers (vertices with a positive weight)",
            "in_out": "no vertex reaches all customers (vertices with a positive weight) and is reached by all of them",
            "undirected": "the customers (vertices with a positive weight) are not all connected with each other",
        }[direction]
        result_string = f"No result: the {location} cannot be determined, because {reason}."
        solution_path += f"\n{result_string}"
        return [], result_string, solution_path, None

    @staticmethod
    def no_location_result_applied(location, direction):
        """
        Result that a network algorithm returns instead of its solution if location_exists is False:
        nothing to mark, the reason as result string, the solution path so far and None (no CSV output).
        """
        reason = {
            "in": "no vertex is reached by all customers (vertices with a positive weight)",
            "out": "no vertex reaches all customers (vertices with a positive weight)",
            "in_out": "no vertex reaches all customers (vertices with a positive weight) and is reached by all of them",
            "undirected": "the customers (vertices with a positive weight) are not all connected with each other",
        }[direction]
        result_string = f"No result: the {location} cannot be determined, because {reason}."
        return [], result_string, None

    @staticmethod
    def get_edges(arr, netw_type):
        """
        Determining all edges of a network by given adjacency matrix
        """
        arr = np.array(arr, dtype=float)      # work on a copy: the caller's matrix must not change
        if netw_type == "undirected":
            for i in range(len(arr) - 1):
                for j in range(i, len(arr)):
                    arr[(j,i)] = 0
        mask = (arr != 0) & (~np.isinf(arr))
        return np.argwhere(mask)

    @staticmethod
    def calculate_weighted_distance_point(point, distance_matrix, matrix, weights):
        """
        Calculating the total weighted distance from a point to all vertices of the network, input is the point in form ((e[0], e[1]), t), the distance matrix (determined by Floyd-Warshall for example), the adjacency matrix and the weights.
        numpy computes the terms w_i * min(d(i, a) + t l, d(i, b) + (1 - t) l) of all vertices at once (min as in Python:
        the first value unless the second is smaller); they are added one after the other as before (not with sum(),
        which adds floats with a correction since Python 3.12), so the result is the same to the last digit.
        """
        (a, b), t = point
        k = len(weights)
        via_a = distance_matrix[:k, a] + t * matrix[a, b]
        via_b = distance_matrix[:k, b] + (1 - t) * matrix[a, b]
        weighted_distance = 0.0
        for term in (np.asarray(weights) * np.where(via_b < via_a, via_b, via_a)).tolist():
            weighted_distance += term
        return np.float64(weighted_distance)

    @staticmethod
    def network_direction(name):
        """How a network algorithm (file or dropdown name, e.g. "in_median_directed_network", "Pareto Out Median Directed
        Network") counts the distances: "in" (customers to the location), "out" (location to the customers), "in_out"
        (there and back) or "undirected"."""
        key = "_" + name.lower().replace(" ", "_")         # "_in_" also at the start of the name
        if "undirected" in key:
            return "undirected"
        return "in" if "_in_" in key else "out" if "_out_" in key else "in_out"

    @staticmethod
    def pareto_front(pareto_set, matrix, weights, direction="undirected", positions=False):
        """
        The Pareto front of a Pareto median: the images (f1, f2, ...) of its locations in the objective function space,
        for the plot (two weight vectors) and the export. f^q(x) = sum_k w^q_k d(v_k, x) for the directions
        "undirected" and "in", sum_k w^q_k d(x, v_k) for "out" and the sum of both for "in_out"; customers with weight
        0 do not count.

        :param pareto_set: the Pareto set an algorithm returned: vertices and parts ((a, b), (t1, t2)) of edges or arcs
                           (1-based; t is the share of the length from a)
        :param matrix: the lengths (None, "n", "inf" or "": no edge)
        :param weights: the weight vectors (two for the plot)
        :param positions: True: every point of a part as (t, (f1, f2, ...))
        :return: (vertices, parts, others), all 1-based: the Pareto optimal vertices [(k, (f1, f2, ...))]; the parts
                 [((a, b), [(f1, f2, ...), ...])], each as the points at t1, at every kink of an f^q inside and at t2
                 (the front is linear between them; the ends are open), one point if all f^q are constant on the part;
                 the other vertices that reach all customers [(k, (f1, f2, ...))]
        """
        n = len(matrix)
        lengths = np.array([[np.inf if value is None or str(value).lower() in ("n", "inf", "") else float(value)
                             for value in row] for row in matrix])
        np.fill_diagonal(lengths, 0.0)
        d = AdditionalMethods.floyd_warshall(lengths)
        to_x = d.T if direction == "out" else d + d.T if direction == "in_out" else d      # to_x[k, x]
        w = np.asarray(weights, dtype=float)
        objectives = range(len(w))
        customers = [[k for k in range(n) if w[q][k] > 0] for q in objectives]

        def vertex(x):
            return tuple(float(sum(w[q][k] * to_x[k, x] for k in customers[q])) for q in objectives)

        def on_edge(a, b, t):           # undirected: the shorter way over a or over b
            length = lengths[a, b]
            return tuple(float(sum(w[q][k] * min(d[k, a] + t * length, d[k, b] + (1 - t) * length) for k in customers[q]))
                         for q in objectives)

        vertices, parts, pareto_vertices = [], [], set()
        for location in pareto_set:
            if isinstance(location, tuple):
                (a, b), (t1, t2) = location
                a, b = a - 1, b - 1
                if direction != "undirected":       # a whole arc: its values are those of its start vertex
                    parts.append(((a + 1, b + 1), [(t1, vertex(a)) if positions else vertex(a)]))
                    continue
                length = lengths[a, b]
                kinks = {(d[k, b] - d[k, a] + length) / (2 * length) for q in objectives for k in customers[q]}
                ts = [t1] + sorted(t for t in kinks if t1 + 1e-9 < t < t2 - 1e-9) + [t2]     # not at the ends (rounding)
                points = [(t, on_edge(a, b, t)) for t in ts]
                points = [p for i, p in enumerate(points) if i == 0 or not np.allclose(p[1], points[i - 1][1])]
                parts.append(((a + 1, b + 1), points if positions else [p for _, p in points]))   # constant: one point
            else:
                pareto_vertices.add(location)
                vertices.append((location, vertex(location - 1)))
        others = [(x + 1, vertex(x)) for x in range(n) if x + 1 not in pareto_vertices and all(np.isfinite(vertex(x)))]
        return vertices, parts, others

    @staticmethod
    def haversine(points1, points2):
        """
        Great-circle distances in km (Haversine formula, earth radius 6371 km).

        :param points1: n points (latitude, longitude) in degrees
        :param points2: m points (latitude, longitude) in degrees
        :return: n x m matrix of the distances
        """
        (lat1, lon1), (lat2, lon2) = np.radians(points1).T[:, :, None], np.radians(points2).T[:, None, :]
        return 2 * 6371 * np.arcsin(np.sqrt(np.sin((lat2 - lat1) / 2) ** 2
                                            + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2))

    @staticmethod
    def transform_points(x, y):
        """
        Transforms points using the matrix [1 1; -1 1].

        :param x: x-coordinate (or array of x-coordinates)
        :param y: y-coordinate (or array of y-coordinates)
        :return: Tuple (x_transformed, y_transformed)
        """
        x_transformed = x + y
        y_transformed = -x + y
        return x_transformed, y_transformed

    @staticmethod
    def inverse_transform(x_t, y_t):
        """
        Inversely transforms points back to the original coordinate system.

        :param x_t: Transformed x-coordinate (or array)
        :param y_t: Transformed y-coordinate (or array)
        :return: Tuple (x_original, y_original)
        """
        x_original = (x_t - y_t) / 2
        y_original = (x_t + y_t) / 2
        return x_original, y_original
    
    @staticmethod
    def assignment_customers(c, n, X):
        """
        Assigns customers to its closest facilities.
        """
        X_print = [x + 1 for x in X]
        Assignment = []
        for i in range(n):
            ci_copy = [c[i,j] for j in X]
            ci_min = min(ci_copy)
            j_as = X[ci_copy.index(ci_min)]
            Assignment.append(j_as)

        return Assignment, X_print

    @staticmethod
    def format_matrix(matrix):
        """
        Formats a matrix into a readable string.

        :param matrix: Numpy matrix
        :return: Formatted string
        """
        return "\n".join(["| " + " ".join(f"{val:8.2f}" for val in row) + " |" for row in matrix])

    @staticmethod
    def format_vector(vector, decimals=4):
        """
        Formats a vector into a readable string, e.g. [194.0000, 152.0000, 103.0000].
        Whole numbers of an integer type (e.g. vertex numbers) are shown without decimals,
        nan (e.g. an already opened facility) as "–".

        :param vector: list or numpy array of numbers
        :param decimals: number of decimals for the other numbers
        :return: Formatted string
        """
        parts = []
        for value in vector:
            if isinstance(value, (int, np.integer)):
                parts.append(str(value))
            elif np.isnan(value):
                parts.append("–")
            else:
                parts.append(f"{value:.{decimals}f}")
        return "[" + ", ".join(parts) + "]"

    @staticmethod
    def output_vertices(interesting_values, obj_value, obj_index, solution_path):
        indices = np.flatnonzero(np.isclose(interesting_values, obj_value))
                
        # Calculating all optimal points for the case that there are multiple optimal points.
        if len(indices) >= 2:
            solution_path += f"\nWe have multiple optimal points because multiple vertices have the lowest objective function value."
            result_string = f'Multiple optimal points on vertices {", ".join(str(i + 1) for i in indices)}\nObjective function value: {obj_value:.4f}'
        else:
            result_string = f"Optimal point at vertex {obj_index+1}\nObjective function value: {obj_value:.4f}"

        return indices, solution_path, result_string

    @staticmethod
    def output_vertices_applied(interesting_values, obj_value, obj_index):
        indices = np.flatnonzero(np.isclose(interesting_values, obj_value))
                
        # Calculating all optimal points for the case that there are multiple optimal points.
        if len(indices) >= 2:
            result_string = f'Multiple optimal points on vertices {", ".join(str(i + 1) for i in indices)}\nObjective function value: {obj_value:.4f}'
        else:
            result_string = f"Optimal point at vertex {obj_index+1}\nObjective function value: {obj_value:.4f}"

        return indices, result_string

    @staticmethod
    def tree_dijkstra(matrix, vert, nr_vertices):
        """
        Calculates all distances of a tree to a given vertex (Dijkstra for trees)

        :param matrix: Numpy matrix, vert: int (vertex ID), nrVertices: int
        :return: distance Numpy array
        """
        distances = np.full(nr_vertices, np.inf)
        paths = [[] for i in range(nr_vertices)]

        distances[vert] = 0
        paths[vert] = [vert]
        stack = [(vert, 0)]
        
        while stack:
            vertex, distance = stack.pop()
            neighbours = np.where((matrix[vertex] != 0) & (~np.isinf(matrix[vertex])))[0]   # np.inf: no edge
            for nb in neighbours:
                if distances[nb] == np.inf:
                    distances[nb] = distance + matrix[vertex, nb]
                    paths[nb] = paths[vertex] + [nb]
                    stack.append((nb, distances[nb]))

        return distances, paths

    @staticmethod
    def tree_matrix(matrix):
        """
        Adjacency matrix of a tree as floats: np.inf where there is no edge (None, "", "n" or "inf"), 0 on the
        diagonal.
        """
        matrix = np.array([
            [
                np.inf
                if value is None or str(value).strip().lower() in ("", "n", "inf")
                else float(value)
                for value in row
            ]
            for row in matrix
        ], dtype=float)
        np.fill_diagonal(matrix, 0.0)
        
        return matrix

    @staticmethod
    def close(a, b):
        """
        np.isclose(a, b) for two numbers, about 30 times faster: |a - b| <= 1e-8 + 1e-5 |b| (the same operations);
        an infinite value is only close to itself, nan to nothing.
        """
        return a == b or (math.isfinite(a) and math.isfinite(b) and abs(a - b) <= 1e-8 + 1e-5 * abs(b))

    @staticmethod
    def _breakpoints(e, n, distances, matrix):
        """
        The breakpoints on the edge e = (a, b) of length l: for every vertex k the share t_k = (d(b, k) - d(a, k) + l) / 2l
        of the edge from a at which the distance from k to the point stops increasing (numpy computes all vertices at
        once, with the same operations as one by one).

        :return: (T: the t_k as numpy numbers, T_print: the same with nan where t_k is (close to) 0 or 1)
        """
        length = matrix[e[0], e[1]]
        T = list((distances[e[1], :n] - distances[e[0], :n] + length) / (2 * length))
        at_end = np.isclose(T, 1) | np.isclose(T, 0)
        T_print = [float('nan') if end else t for t, end in zip(T, at_end)]
        return T, T_print