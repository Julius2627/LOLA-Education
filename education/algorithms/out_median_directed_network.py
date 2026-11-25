import numpy as np
from common.additional_methods import AdditionalMethods

class out_median_directed_network:
    """
    Out-median on a directed network: the location serves the customers.

    Minimises the sum of the weighted shortest path lengths from the location x to the customers:
        f(x) = sum_k w_k * d(x, v_k)
    A point inside an arc (u, v) reaches the customers only via v and is therefore never better than v,
    so it suffices to compare the vertices. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. Weighted distance matrix d(i, j) * w_j (column = customer); its row sums are the values f(i).
      3. The vertices with the smallest row sum are optimal.

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
        # A location must reach every customer
        if not AdditionalMethods.location_exists(distances, self.weights, "out"):
            return AdditionalMethods.no_location_result("out median", "out", solution_path)

        # Calculating the weighted distance matrices
        weighted_out_distances = AdditionalMethods.calculate_weighted_out_distances(distances, self.weights)

        solution_path += f"\nThe network has the weighted out distance matrix:\n{AdditionalMethods.format_matrix(weighted_out_distances)}"

        # Calculating the row sums and subsequently determining the median
        row_sums = weighted_out_distances.sum(axis=1)

        solution_path += f"\nWe get the row sums:\n{AdditionalMethods.format_vector(row_sums)}"

        median_index = np.argmin(row_sums)
        median_value = row_sums[median_index]

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, solution_path, result_string = AdditionalMethods.output_vertices(row_sums, median_value, median_index, solution_path)

        return list(i+1 for i in indices), result_string, solution_path, None