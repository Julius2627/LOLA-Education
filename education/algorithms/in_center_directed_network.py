import numpy as np
from common.additional_methods import AdditionalMethods

class in_center_directed_network:
    """
    In-center on a directed network: the customers travel to the location.

    Minimises the largest weighted shortest path length from a customer to the location x:
        f(x) = max_k w_k * d(v_k, x)
    A point inside an arc (u, v) is reached only via u and is therefore never better than u, so an
    optimal vertex always exists and it suffices to compare the vertices. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. Weighted distance matrix w_i * d(i, j) (row = customer); its column maxima are the values f(j).
      3. The vertices with the smallest column maximum are optimal.

    :param weights: weight w_k of every vertex (customers have w_k > 0; vertices with w_k = 0 need not be reached)
    :param matrix: adjacency matrix with the arc lengths, None where there is no arc
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
        # A location must be reachable from every customer
        if not AdditionalMethods.location_exists(distances, self.weights, "in"):
            return AdditionalMethods.no_location_result("in center", "in", solution_path)

        # Calculating the weighted distance matrices
        weighted_in_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)

        solution_path += f"\nThe network has the weighted in distance matrix:\n{AdditionalMethods.format_matrix(weighted_in_distances)}"

        # Calculating the column maxima and subsequently determining the center
        col_maxima = weighted_in_distances.max(axis=0)

        solution_path += f"\nWe get the column maxima:\n{AdditionalMethods.format_vector(col_maxima)}"
        
        center_index = np.argmin(col_maxima)
        solution_value = col_maxima[center_index]

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, solution_path, result_string = AdditionalMethods.output_vertices(col_maxima, solution_value, center_index, solution_path)

        return list(i+1 for i in indices), result_string, solution_path, None