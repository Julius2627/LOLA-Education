import numpy as np
from common.additional_methods import AdditionalMethods

class center_directed_network:
    """
    Center on a directed network with the way to and back: the customers travel to the location and back.

    Minimises the largest weighted round trip between a customer and the location x:
        f(x) = max_k w_k * (d(v_k, x) + d(x, v_k))
    Along an arc (u, v) every round trip has a constant length that is at least the round trip to u,
    so an optimal vertex always exists; the points of an arc are either all optimal or none. Steps:
      1. Shortest path lengths d(i, j) along the arcs (Floyd-Warshall).
      2. Weighted round trips w_i * (d(i, j) + d(j, i)) (row = customer i, column = location j).
      3. The column maxima are the values f(j); the vertices with the smallest maximum are optimal.
      4. Arcs between optimal vertices whose (constant) value is optimal as well (see _center_arcs).

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
            return AdditionalMethods.no_location_result("center", "in_out", self.solution_path)

        # Calculating the weighted distance matrices
        weighted_in_distances = AdditionalMethods.calculate_weighted_in_distances(distances, self.weights)
        weighted_out_distances = AdditionalMethods.calculate_weighted_out_distances(distances, self.weights)

        self.solution_path += f"\nThe network has the weighted in distance matrix:\n{AdditionalMethods.format_matrix(weighted_in_distances)}"
        self.solution_path += f"\nThe network has the weighted out distance matrix:\n{AdditionalMethods.format_matrix(weighted_out_distances)}"

        # Entry (i, j): weighted round trip of customer i to location j (the out matrix is transposed for this)
        weighted_distances = weighted_in_distances + weighted_out_distances.T

        self.solution_path += f"\nThe network has the weighted total distance matrix:\n{AdditionalMethods.format_matrix(weighted_distances)}"

        # Calculating the column maxima and subsequently determining the center
        col_maxima = weighted_distances.max(axis=0)

        self.solution_path += f"\nWe get the column maxima:\n{AdditionalMethods.format_vector(col_maxima)}"
        
        center_index = np.argmin(col_maxima)
        center_value = col_maxima[center_index]

        # All vertices with the smallest value are optimal; output_vertices also writes the result text
        indices, self.solution_path, result_string = AdditionalMethods.output_vertices(col_maxima, center_value, center_index, self.solution_path)
        center_set = list(i+1 for i in indices)
        # Complete arcs can be optimal as well, but only between optimal vertices: the values on an arc are at
        # least those of both its end vertices
        if len(indices) > 1:
            center_arcs = self._center_arcs(indices, center_value, len(self.weights), distances)
            if len(center_arcs) > 0:
                for u, v in center_arcs:
                    center_set.append(((u + 1, v + 1), (0, 1)))
                result_string = f'Multiple optimal points on vertices {", ".join(str(i + 1) for i in indices)}, and the complete arcs {", ".join(f"({u + 1}, {v + 1})" for u, v in center_arcs)} are also optimal.\nObjective function value: {center_value:.4f}'
            
        return center_set, result_string, self.solution_path, None

    def _center_arcs(self, center_vertices, center_value, n, distances):
        """
        Arcs whose points are all optimal. On an arc (u, v) every round trip is constant: a point x of the arc is
        reached only via u and reaches the customers only via v, so its round trip with customer k is
            d(k, u) + l(u, v) + d(v, k),
        which is at least the round trip of k to u and to v. The arc is therefore optimal exactly if the largest of
        these weighted round trips equals the optimal value.

        :param center_vertices: the optimal vertices (0-based)
        :param center_value: the optimal objective function value
        :param n: number of vertices
        :param distances: matrix of the shortest path lengths
        :return: list of the optimal arcs (u, v), 0-based
        """
        self.solution_path += "\nChecking if there are optimal arcs, i.e., arcs where the objective function is constant: a point of the arc is reached only via u and reaches the customers only via v. These values are at least those of vertex u, so the arc is optimal exactly if it has the same values as the optimal vertex u."
        center_arcs = []
        for u in sorted(center_vertices):
            for v in range(n):
                if u == v or self.matrix[u, v] is None:
                    continue
                arc_value = max((self.weights[k] * (distances[k, u] + self.matrix[u, v] + distances[v, k])
                                  for k in range(n) if self.weights[k] > 0), default=0)
                if np.isclose(arc_value, center_value):
                    center_arcs.append((u, v))
                    self.solution_path += f"\nThe arc ({u + 1}, {v + 1}) has the same objective function value as vertex {u + 1} which is optimal; hence, the complete arc is optimal."
        return center_arcs