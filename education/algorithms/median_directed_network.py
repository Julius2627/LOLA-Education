import numpy as np
from common.additional_methods import AdditionalMethods

class median_directed_network:
    """
    Median on a directed network with the way to and back: the customers travel to the location and back.

    Minimises the sum of the weighted round trips between the customers and the location x:
        f(x) = sum_k w_k * (d(v_k, x) + d(x, v_k))
    Along an arc (u, v) every round trip has a constant length that is at least the round trip to u,
    so an optimal vertex always exists; the points of an arc are either all optimal or none. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. Weighted in distances w_i * d(i, j) (column sums: way to j) and out distances d(i, j) * w_j
         (row sums: way from i).
      3. f(v) = column sum + row sum of v; the vertices with the smallest value are optimal.
      4. Arcs between optimal vertices whose (constant) value is optimal as well (see _median_arcs). With a
         positive weight of u this is impossible (customer u's round trip is 0 at u), so it needs w_u = 0.

    :param weights: weight w_k of every vertex (customers have w_k > 0; vertices with w_k = 0 need not be reached)
    :param matrix: adjacency matrix with the arc lengths, None where there is no arc
    """

    def __init__(self, weights, matrix):
        self.matrix = np.array(matrix)
        self.weights = np.array(weights)
        self.solution_path = ""

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal vertices as 1-based vertex numbers, followed by the completely optimal arcs as
                 ((u, v), (0, 1)); result text; solution path; None); if no vertex has a finite objective function
                 value:
                 ([], "No result: ..." text, solution path, None)
        """
        # Calculating the distance matrix of the network
        distances = AdditionalMethods.floyd_warshall(self.matrix)
        self.solution_path += f"The network has the distance matrix:\n{AdditionalMethods.format_matrix(distances)}"
        # A location must reach every customer and be reachable from every customer
        if not AdditionalMethods.location_exists(distances, self.weights, "in_out"):
            return AdditionalMethods.no_location_result("median", "in_out", self.solution_path)

        # Calculating the weighted distance matrices
        weighted_in_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)
        weighted_out_distances = AdditionalMethods.calculate_weighted_out_distances(distances, self.weights)

        self.solution_path += f"\nThe network has the weighted in distance matrix:\n{AdditionalMethods.format_matrix(weighted_in_distances)}"
        self.solution_path += f"\nThe network has the weighted out distance matrix:\n{AdditionalMethods.format_matrix(weighted_out_distances)}"

        # Calculating the column and row sums and subsequently determining the median
        col_sums = weighted_in_distances.sum(axis=0)
        row_sums = weighted_out_distances.sum(axis=1)

        self.solution_path += f"\nWe get the column sums:\n{AdditionalMethods.format_vector(col_sums)}"
        self.solution_path += f"\nWe get the row sums:\n{AdditionalMethods.format_vector(row_sums)}"

        # Objective function value of every vertex: way to it plus way back
        vertices_sums = col_sums + row_sums
        
        median_index = np.argmin(vertices_sums)
        median_value = vertices_sums[median_index]

        self.solution_path += f"\nIn total we get the sums:\n{AdditionalMethods.format_vector(vertices_sums)}"

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, self.solution_path, result_string = AdditionalMethods.output_vertices(vertices_sums, median_value, median_index, self.solution_path)
        median_set = list(i+1 for i in indices)
        # Complete arcs can be optimal as well, but only between optimal vertices: the values on an arc are at
        # least those of both its end vertices
        if len(indices) > 1:
            median_arcs = self._median_arcs(indices, median_value, len(self.weights), distances)
            if len(median_arcs) > 0:
                for u, v in median_arcs:
                    median_set.append(((u + 1, v + 1), (0, 1)))
                result_string = f'Multiple optimal points on vertices {", ".join(str(i + 1) for i in indices)}, and the complete arcs {", ".join(f"({u + 1}, {v + 1})" for u, v in median_arcs)} are also optimal.\nObjective function value: {median_value:.4f}'

        return median_set, result_string, self.solution_path, None

    def _median_arcs(self, median_vertices, median_value, n, distances):
        """
        Arcs whose points are all optimal. On an arc (u, v) every round trip is constant: a point x of the arc is
        reached only via u and reaches the customers only via v, so its round trip with customer k is
            d(k, u) + l(u, v) + d(v, k),
        which is at least the round trip of k to u and to v. The arc is therefore optimal exactly if the sum of
        these weighted round trips equals the optimal value.

        :param median_vertices: the optimal vertices (0-based)
        :param median_value: the optimal objective function value
        :param n: number of vertices
        :param distances: matrix of the shortest path lengths
        :return: list of the optimal arcs (u, v), 0-based
        """
        self.solution_path += "\nChecking if there are optimal arcs, i.e., arcs where the objective function is constant: a point of the arc is reached only via u and reaches the customers only via v. These values are at least those of vertex u, so the arc is optimal exactly if it has the same values as the optimal vertex u."
        median_arcs = []
        for u in sorted(median_vertices):
            for v in range(n):
                if u == v or self.matrix[u, v] is None:
                    continue
                arc_value = sum(self.weights[k] * (distances[k, u] + self.matrix[u, v] + distances[v, k])
                                    for k in range(n) if self.weights[k] > 0)
                if np.isclose(arc_value, median_value):
                    median_arcs.append((u, v))
                    self.solution_path += f"\nThe arc ({u + 1}, {v + 1}) has the same objective function value as vertex {u + 1} which is optimal; hence, the complete arc is optimal."
        return median_arcs