import numpy as np
from common.additional_methods import AdditionalMethods

class in_median_directed_network:
    """
    In-median on a directed network: the customers travel to the location.

    Minimises the sum of the weighted shortest path lengths from the customers to the location x:
        f(x) = sum_k w_k * d(v_k, x)
    A point inside an arc (u, v) is reached only via u and is therefore never better than u, so it
    suffices to compare the vertices. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. Weighted distance matrix w_i * d(i, j) (row = customer); its column sums are the values f(j).
      3. The vertices with the smallest column sum are optimal.

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
            return AdditionalMethods.no_location_result("in median", "in", solution_path)

        # Calculating the weighted distance matrices
        weighted_in_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)

        solution_path += f"\nThe network has the weighted in distance matrix:\n{AdditionalMethods.format_matrix(weighted_in_distances)}"

        # Calculating the column sums and subsequently determining the median
        col_sums = weighted_in_distances.sum(axis=0)

        solution_path += f"\nWe get the column sums:\n{AdditionalMethods.format_vector(col_sums)}"
        
        median_index = np.argmin(col_sums)
        median_value = col_sums[median_index]

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, solution_path, result_string = AdditionalMethods.output_vertices(col_sums, median_value, median_index, solution_path)

        return list(i+1 for i in indices), result_string, solution_path, None