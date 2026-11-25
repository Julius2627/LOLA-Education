import numpy as np
from common.additional_methods import AdditionalMethods

class center_undirected_network_vertex_restricted:
    """
    Vertex-restricted center on an undirected network.

    Minimises the largest weighted shortest path length from a customer to the location, where only the
    vertices are allowed as locations:
        f(v) = max_k w_k * d(v_k, v)
    Steps:
      1. Shortest path lengths d(i, j) between all vertices (Floyd-Warshall).
      2. Weighted distance matrix w_i * d(i, j); its column maxima are the values f(j) of the vertices.
      3. The vertices with the smallest column maximum are optimal.
    (On an edge the center can be better than on any vertex, see center_undirected_network_absolute.)

    :param weights: weight w_k of every vertex (customers have w_k > 0; vertices with w_k = 0 need not be reached)
    :param matrix: adjacency matrix with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        self.matrix = np.array(matrix)
        self.weights = np.array(weights)

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal vertices as a list of 1-based vertex numbers, result text, solution path, None);
                 if no vertex has a finite objective function value:
                 ([], "No result: ..." text, solution path, None)
        """
        # Calculating the distance matrix of the network
        distances = AdditionalMethods.floyd_warshall(self.matrix)
        solution_path = f"The network has the distance matrix:\n{AdditionalMethods.format_matrix(distances)}"
        # If the customers are not connected, no vertex has a finite objective function value
        if not AdditionalMethods.location_exists(distances, self.weights, "undirected"):
            return AdditionalMethods.no_location_result("center", "undirected", solution_path)

        # Calculating the weighted distance matrix
        weighted_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)
        solution_path += f"\nThe network has the weighted distance matrix:\n{AdditionalMethods.format_matrix(weighted_distances)}"

        # Calculating the column maxima and subsequently determining the center
        col_max = weighted_distances.max(axis=0)
        center_index = np.argmin(col_max)
        center_value = col_max[center_index]

        solution_path += f"\nWe get the maximum column entries:\n{AdditionalMethods.format_vector(col_max)}"

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, solution_path, result_string = AdditionalMethods.output_vertices(col_max, center_value, center_index, solution_path)

        return list(i+1 for i in indices), result_string, solution_path, None