import numpy as np
from common.additional_methods import AdditionalMethods
from education.algorithms.pareto_median_undirected_network import pareto_median_undirected_network
EPS = 1e-7   # tolerance when comparing numbers (rounding errors)

class pareto_median_directed_network:
    """
    Pareto median on a directed network with the way to and back, with Q >= 2 weight vectors: the customers
    travel to the location and back.

    Every weight vector q gives an objective function f^q(x) = sum_k w^q_k * (d(v_k, x) + d(x, v_k)): the column
    sums of its weighted in distance matrix plus the row sums of its weighted out distance matrix. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. f^q(v) for every weight vector q and every vertex v.
      3. The vertices whose vectors (f^1(v), ..., f^Q(v)) are not dominated are Pareto optimal.
      4. On an arc (u, v) all objective functions are constant and at least as large as at u, so the points
         of an arc are Pareto optimal exactly if its values equal those of a Pareto optimal vertex u
         (see _pareto_arcs).

    A location is Pareto optimal if no other location is at least as good in every objective function and better in
    at least one.

    :param weights: the weight vectors w^1, ..., w^Q, one list per weight vector with one weight per vertex
    :param matrix: adjacency matrix with the arc lengths, None where there is no arc
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
        self.col_sums = np.array([])
        self.row_sums = np.array([])
        self.vertices_sums = np.array([])
        self.distances = np.array([])


    def run(self):
        """
        Runs the algorithm.

        :return: (Pareto optimal vertices as 1-based vertex numbers, followed by the Pareto optimal arcs as
                 ((u, v), (0, 1)), i.e. all points of the arc from t = 0 to t = 1; result text with the Pareto
                 frontier and the objective function frontier; solution path; None);
                 with fewer than two weight vectors or without a vertex with finite objective function values:
                 ([], "No result: ..." text, solution path, None)
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
        _, self.col_sums, self.solution_path = pareto_median_directed_network.multiple_weighted_in_distances_calculations(self.distances, self.weights, nr_objectives, self.solution_path)
        _, self.row_sums, self.solution_path = pareto_median_directed_network.multiple_weighted_out_distances_calculations(self.distances, self.weights, nr_objectives, self.solution_path)

        # Objective function values of the vertices: way to the vertex plus way back (one row per weight vector)
        self.vertices_sums = self.col_sums + self.row_sums
        self.solution_path += f"\nIn total we get the sums for the vertices(one row per weight vector):\n{AdditionalMethods.format_matrix(self.vertices_sums)}"

        # The customers (vertices with a positive weight in at least one weight vector) must be reachable
        customer_weights = [max(self.weights[q][k] for q in range(nr_objectives)) for k in range(n)]
        if not AdditionalMethods.location_exists(self.distances, customer_weights, "in_out"):
            return AdditionalMethods.no_location_result("Pareto locations", "in_out", self.solution_path)
        # Vertices whose vectors of objective function values (one column per vertex) are not dominated
        pareto_vertices, _, self.solution_path = pareto_median_undirected_network.pareto_vertices_determination(n, self.vertices_sums, self.solution_path)
        # a vertex that does not reach every customer (or is not reached by every customer) is no location
        pareto_vertices = [v for v in pareto_vertices if np.all(np.isfinite(self.vertices_sums[:, v]))]
        pareto_arcs = self._pareto_arcs(pareto_vertices, n, nr_objectives)
        # Output: the Pareto optimal vertices with their objective function values, then the Pareto optimal arcs
        pareto_set = []
        frontier = []
        for v in sorted(pareto_vertices):
            pareto_set.append(v + 1)
            frontier.append(tuple(float(self.vertices_sums[q][v]) for q in range(nr_objectives)))
        for u, v in pareto_arcs:
            pareto_set.append(((u + 1, v + 1), (0, 1)))     # the complete arc; its values are those of vertex u
        result_string = ("Pareto frontier {" + ", ".join(pareto_median_undirected_network.format_numbers(p) for p in pareto_set) + "}"
                            f"\nObjective function frontier: {pareto_median_undirected_network.format_numbers(frontier)}")
        return pareto_set, result_string, self.solution_path, None

    def _pareto_arcs(self, pareto_vertices, n, nr_objectives):
        """
        Arcs whose points are Pareto optimal. On an arc (u, v) every objective function is constant: a point x
        on the arc is reached only via u and reaches the customers only via v, so
            f^q(x) = sum_k w^q_k (d(k, u) + l(u, v) + d(v, k)) >= sum_k w^q_k (d(k, u) + d(u, k)) = f^q(u).
        The points of the arc are therefore Pareto optimal exactly if these values are equal to those of a
        Pareto optimal vertex u (then v has the same values as well).

        :return: list of the arcs (u, v), 0-based
        """
        self.solution_path += "\nChecking if there are Pareto optimal arcs, i.e., arcs where the objective functions are constant: a point of the arc is reached only via u and reaches the customers only via v. These values are at least those of vertex u, so the arc is Pareto optimal exactly if it has the same values as the Pareto optimal vertex u."
        pareto_arcs = []
        for u in sorted(pareto_vertices):
            for v in range(n):
                if u == v or not np.isfinite(self.matrix[u, v]):
                    continue
                arc_values = [sum(self.weights[q][k] * (self.distances[k, u] + self.matrix[u, v] + self.distances[v, k])
                                  for k in range(n) if self.weights[q][k] > 0) for q in range(nr_objectives)]
                if all(abs(arc_values[q] - self.vertices_sums[q][u]) <= EPS for q in range(nr_objectives)):
                    pareto_arcs.append((u, v))
                    self.solution_path += f"\nThe arc ({u + 1}, {v + 1}) has the same objective function values as vertex {u + 1} which is Pareto optimal; hence, the complete arc is Pareto optimal."
        return pareto_arcs

    @staticmethod
    def multiple_weighted_in_distances_calculations(distances, weights, nr_objectives, sol_path):
        """
        Weighted in distance matrices w^q_i * d(i, j) and their column sums f^q(j) (way to j) for every weight
        vector q (also used by pareto_in_median_directed_network).

        :return: (weighted matrices, array with one row of column sums per weight vector, solution path)
        """
        weighted_distances = []
        col_sums = []
        for i in range(nr_objectives):
            weighted_matrix = AdditionalMethods.calculate_weighted_in_distances(distances, weights[i])
            sol_path += f"\nFor weight vector {i+1}, the network has the weighted in distance matrix:\n{AdditionalMethods.format_matrix(weighted_matrix)}"
            weighted_distances.append(weighted_matrix)
            col_sum = weighted_distances[i].sum(axis=0)
            col_sums.append(col_sum)
            sol_path += f"\nAnd we get the column sums:\n{AdditionalMethods.format_vector(col_sum)}"
        col_sums = np.array(col_sums)
        weighted_distances = np.array(weighted_distances)
        return weighted_distances, col_sums, sol_path

    @staticmethod
    def multiple_weighted_out_distances_calculations(distances, weights, nr_objectives, sol_path):
        """
        Weighted out distance matrices d(i, j) * w^q_j and their row sums f^q(i) (way from i) for every weight
        vector q (also used by pareto_out_median_directed_network).

        :return: (weighted matrices, array with one row of row sums per weight vector, solution path)
        """
        weighted_distances = []
        row_sums = []
        for i in range(nr_objectives):
            weighted_matrix = AdditionalMethods.calculate_weighted_out_distances(distances, weights[i])
            sol_path += f"\nFor weight vector {i+1}, the network has the weighted out distance matrix:\n{AdditionalMethods.format_matrix(weighted_matrix)}"
            weighted_distances.append(weighted_matrix)
            row_sum = weighted_matrix.sum(axis=1)
            row_sums.append(row_sum)
            sol_path += f"\nAnd we get the row sums:\n{AdditionalMethods.format_vector(row_sum)}"
        row_sums = np.array(row_sums)
        weighted_distances = np.array(weighted_distances)
        return weighted_distances, row_sums, sol_path