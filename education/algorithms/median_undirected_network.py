import numpy as np
from common.additional_methods import AdditionalMethods

class median_undirected_network:
    """
    Median on an undirected network.

    Minimises the sum of the weighted shortest path lengths from the customers to the location x:
        f(x) = sum_k w_k * d(v_k, x)
    On a network there is always an optimal vertex (vertex optimality), so it suffices to compare the
    vertices. Steps:
      1. Shortest path lengths d(i, j) between all vertices (Floyd-Warshall).
      2. Weighted distance matrix w_i * d(i, j); its column sums are the values f(j) of the vertices.
      3. The vertices with the smallest column sum are optimal. If two of them are adjacent and the
         midpoint of their edge is optimal as well, the whole edge is optimal (see _optimal_edges).

    :param weights: weight w_k of every vertex (customers have w_k > 0; vertices with w_k = 0 need not be reached)
    :param matrix: adjacency matrix with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        self.matrix = np.array(matrix)
        self.weights = np.array(weights)
        self.solution_path = ""

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal vertices as 1-based vertex numbers, followed by the completely optimal edges as tuples
                 (i, j); result text; solution path; None);
                 if the customers are not connected: ([], "No result: ..." text, solution path, None)
        """
        # Calculating the distance matrix of the network
        distances = AdditionalMethods.floyd_warshall(self.matrix)
        self.solution_path += f"The network has the distance matrix:\n{AdditionalMethods.format_matrix(distances)}"
        # If the customers are not connected, no vertex has a finite objective function value
        if not AdditionalMethods.location_exists(distances, self.weights, "undirected"):
            return AdditionalMethods.no_location_result("median", "undirected", self.solution_path)

        # Calculating the weighted distance matrix
        weighted_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)
        self.solution_path += f"\nThe network has the weighted distance matrix:\n{AdditionalMethods.format_matrix(weighted_distances)}"

        # Calculating the column sums and subsequently determining the median
        col_sums = weighted_distances.sum(axis=0)
        median_index = np.argmin(col_sums)
        median_value = col_sums[median_index]

        self.solution_path += f"\nWe get the column sums:\n{AdditionalMethods.format_vector(col_sums)}"

        # All vertices with the smallest value are optimal (with a tolerance for rounding errors)
        indices = np.flatnonzero(np.isclose(col_sums, median_value))
        result_objects = list(i+1 for i in indices)
        
        # Calculating all optimal points for the case that there are multiple optimal points.
        if len(indices) >= 2:
            self.solution_path += f"\nWe have multiple optimal points because multiple vertices have the lowest objective function value."
            result_string = f'Multiple optimal points on vertices {", ".join(str(i + 1) for i in indices)}\nObjective function value: {median_value:.4f}'
            optimal_edges, result_objects = self._optimal_edges(indices, distances, median_value, result_objects)
            if len(optimal_edges) >= 1:
                result_string += f'\nAlso the edges {", ".join(f"[{a}, {b}]" for a, b in optimal_edges)} are optimal.'
        else:
            result_string = f"Optimal point at vertex {median_index+1}\nObjective function value: {median_value:.4f}"

        return result_objects, result_string, self.solution_path, None



    def _optimal_edges(self, indices, distances, median_value, result_objects):
        """
        Edges between two optimal vertices on which every point is optimal. Along an edge the objective
        function is concave; if it has the optimal value at both end vertices and at the midpoint of the
        edge, it is therefore constant on the whole edge.

        :param indices: the optimal vertices (0-based)
        :param distances: matrix of the shortest path lengths
        :param median_value: the optimal objective function value
        :param result_objects: the optimal vertices (1-based); the optimal edges are appended as tuples (i, j)
        :return: (optimal edges as lists [i, j], 1-based; result_objects with the edges appended)
        """
        optimal_edges = []
        for idx, i in enumerate(indices[:-1]):
            for j in indices[idx+1:]:
                if self.matrix[i,j] is not None:
                    # Objective function value at the midpoint of the edge; customer k reaches it via i or via j
                    middle_point_distance = 0
                    for k in range(len(self.weights)):
                        if self.weights[k] > 0:
                            middle_point_distance += self.weights[k] * (self.matrix[i,j]/2 + min(distances[i,k], distances[j,k]))
                    if np.isclose(middle_point_distance, median_value):
                        self.solution_path += f"\nSince vertices {i+1} and {j+1} are optimal as well as the middle of the connecting edge, the complete edge ({i+1}, {j+1}) is optimal."
                        optimal_edges.append([i+1, j+1])
                        result_objects.append((i+1, j+1))
        return optimal_edges, result_objects