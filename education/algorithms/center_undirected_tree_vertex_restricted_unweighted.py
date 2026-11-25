import numpy as np
from common.additional_methods import AdditionalMethods
from education.algorithms.center_undirected_tree_absolute_unweighted import center_undirected_tree_absolute_unweighted

class center_undirected_tree_vertex_restricted_unweighted:
    """
    Vertex-restricted center of an undirected tree, unweighted: the vertex whose largest distance to a
    vertex is smallest.

    First the absolute center is determined (see center_undirected_tree_absolute_unweighted). If it is a
    vertex, this vertex is optimal. Otherwise it lies inside an edge (a, b) of a longest path. On a tree the
    largest distance from a vertex is its distance to the absolute center plus the optimal value of the
    absolute center, so the best vertex is a or b, whichever has the smaller largest distance (both if they
    are equal).

    :param weights: weights of the vertices (not used: unweighted problem)
    :param matrix: adjacency matrix of the tree with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        self.matrix = AdditionalMethods.tree_matrix(matrix)
        self.weights = np.asarray(weights, dtype=float)

    def run(self):
        """
        Runs the algorithm.

        :return: (center, result text, solution path, None); the center is a vertex number (1-based) or the list
                 [a, b] if both end vertices of the edge with the absolute center are optimal
        """
        n = len(self.matrix)
        solution_path = ""

        # Absolute center: half the length of a longest path and the edge on this path that contains its midpoint
        solution_value_absolute, dist, paths, path_center_index, center, outside_vertex_2, i, solution_path = center_undirected_tree_absolute_unweighted.calculate_absolute_tree_center(n, self.matrix, solution_path)
        
        if isinstance(center, int):  # only one vertex
            result_string = f"Optimal point at vertex 1\nObjective function value: 0"

        else:
            # End vertices a, b of the edge with the absolute center and its position t on this edge
            a, b = paths[outside_vertex_2][path_center_index], paths[outside_vertex_2][path_center_index + 1]
            t = (solution_value_absolute - dist) / self.matrix[a, b]

            if np.isclose(t, 1):  # the absolute center is the vertex b
                result_string = f"Optimal point at vertex {b + 1}\nObjective function value: {solution_value_absolute:.4f}"
                center = b + 1
                solution_value = solution_value_absolute
                solution_path += f"\nThe absolute center is already on a vertex, namely {b + 1}."
            else:
                solution_path += f"\nThe absolute center is between vertex {a + 1} and vertex {b + 1} (at t = {t:.4f})."

                # Largest distances from a and from b: the vertex with the smaller one is optimal (both if they are
                # equal)
                dist1, _ = AdditionalMethods.tree_dijkstra(self.matrix, a, n)
                dist2, _ = AdditionalMethods.tree_dijkstra(self.matrix, b, n)

                if np.isclose(max(dist1), max(dist2)):
                    solution_value = max(dist1)
                    result_string = f'Multiple optimal points on vertices {a + 1}, {b + 1}\nObjective function value: {solution_value:.4f}'
                    center = [a + 1, b + 1]
                elif max(dist1) < max(dist2):
                    solution_value = max(dist1)
                    result_string = f"Optimal point at vertex {a + 1}\nObjective function value: {solution_value:.4f}"
                    center = a + 1
                else:
                    solution_value = max(dist2)
                    result_string = f"Optimal point at vertex {b + 1}\nObjective function value: {solution_value:.4f}"
                    center = b + 1

        return center, result_string, solution_path, None