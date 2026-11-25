import numpy as np
from common.additional_methods import AdditionalMethods
from education.algorithms.pareto_median_undirected_network import pareto_median_undirected_network


class pareto_median_undirected_network_vertex_restricted:
    """
    Vertex-restricted Pareto median on an undirected network with Q >= 2 weight vectors.

    Every weight vector q gives an objective function f^q(v) = sum_k w^q_k * d(v_k, v), the column sums of its
    weighted distance matrix. Only the vertices are allowed as locations (for the points on the edges see
    pareto_median_undirected_network). Steps:
      1. Shortest path lengths d(i, j) between all vertices (Floyd-Warshall).
      2. f^q(v) for every weight vector q and every vertex v.
      3. The vertices whose vectors (f^1(v), ..., f^Q(v)) are not dominated are Pareto optimal.

    A location is Pareto optimal if no other location is at least as good in every objective function and better in
    at least one.

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
        self.col_sums = np.array([])
        self.distances = np.array([])


    def run(self):
        """
        Runs the algorithm.

        :return: (Pareto optimal vertices as 1-based vertex numbers, result text with the Pareto frontier and the
                 objective function frontier, solution path, None);
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
        self.weighted_distances, self.col_sums, self.solution_path = pareto_median_undirected_network.multiple_weighted_distances_calculations(self.distances, self.weights, nr_objectives, self.solution_path)
        # The customers (vertices with a positive weight in at least one weight vector) must be reachable
        customer_weights = [max(self.weights[q][k] for q in range(nr_objectives)) for k in range(n)]
        if not AdditionalMethods.location_exists(self.distances, customer_weights, "undirected"):
            return AdditionalMethods.no_location_result("Pareto locations", "undirected", self.solution_path)
        # Vertices whose vectors of objective function values (one column per vertex) are not dominated
        pareto_vertices, _, self.solution_path = pareto_median_undirected_network.pareto_vertices_determination(n, self.col_sums, self.solution_path)
        # a vertex that does not reach every customer (or is not reached by every customer) is no location
        pareto_vertices = [v for v in pareto_vertices if np.all(np.isfinite(self.col_sums[:, v]))]
        # Output: the Pareto optimal vertices with their objective function values
        pareto_set = []
        frontier = []
        for v in sorted(pareto_vertices):
            pareto_set.append(v + 1)
            frontier.append(tuple(float(self.col_sums[q][v]) for q in range(nr_objectives)))
        result_string = ("Pareto frontier {" + ", ".join(pareto_median_undirected_network.format_numbers(p) for p in pareto_set) + "}"
                            f"\nObjective function frontier: {pareto_median_undirected_network.format_numbers(frontier)}")
        return pareto_set, result_string, self.solution_path, None