import numpy as np
from common.additional_methods import AdditionalMethods

class center_undirected_tree_absolute_unweighted:
    """
    Absolute center of an undirected tree, unweighted: the point (vertex or point on an edge) whose largest
    distance to a vertex is smallest, f(x) = max_k d(v_k, x).

    On a tree the farthest vertex from any vertex is an end vertex of a longest path, and the farthest
    vertex from this end vertex is the other end. The center is the midpoint of this longest path, and the
    optimal value is half of its length. Steps (see calculate_absolute_tree_center):
      1. Farthest vertex u from vertex 1 (tree Dijkstra).
      2. Farthest vertex v from u, with the path from u to v.
      3. Walk from u along the path to the edge that contains the midpoint.

    :param weights: weights of the vertices (not used: unweighted problem)
    :param matrix: adjacency matrix of the tree with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        self.matrix = AdditionalMethods.tree_matrix(matrix)
        self.weights = np.asarray(weights, dtype=float)

    def run(self):
        """
        Runs the algorithm.

        :return: (center, result text, solution path, None); the center is a vertex number (1-based) or ((i, j), t)
                 for the point on the edge (i, j) at the fraction t of its length from i
        """
        n = len(self.matrix)
        solution_path = ""

        solution_value, dist, paths, path_center_index, center, outside_vertex_2, i, solution_path = self.calculate_absolute_tree_center(n, self.matrix, solution_path)
        # Longest path of the tree, from u to v
        path = paths[outside_vertex_2]

        # Three cases: only one vertex; the midpoint is the end vertex path[i + 1] of the edge on which the walk
        # stopped; otherwise it lies inside this edge at t = (half length - walked) / edge length
        if isinstance(center, int):
            result_string = f"Optimal point at vertex 1\nObjective function value: 0"
        
        elif np.isclose(dist + self.matrix[path[i], path[i + 1]], solution_value):
            center = path[i + 1] + 1
            result_string = f"Optimal point at vertex {center}\nObjective function value: {solution_value:.4f}"
        else:
            t = (solution_value - dist) / self.matrix[path[path_center_index], path[path_center_index + 1]]
            result_string = f"Optimal point: on edge ({path[path_center_index] + 1}, {path[path_center_index + 1] + 1}) at t = {t:.4f}\nObjective function value: {solution_value:.4f}"
            center = ((path[path_center_index] + 1, path[path_center_index + 1] + 1), t)

        return center, result_string, solution_path, None



    @staticmethod
    def calculate_absolute_tree_center(n, matrix, solution_path):
        """
        Absolute center of an unweighted tree (also used by center_undirected_tree_vertex_restricted_unweighted).

        :param n: number of vertices
        :param matrix: adjacency matrix of the tree (np.inf where there is no edge, see AdditionalMethods.tree_matrix)
        :param solution_path: solution path so far
        :return: (optimal value = half the length of the longest path,
                  walked = length of the longest path from u to the start vertex of the edge with the midpoint,
                  paths = paths from u to all vertices,
                  index of the edge with the midpoint on the longest path,
                  center (1 if the tree has only one vertex, otherwise nan),
                  v = the other end vertex of the longest path,
                  loop index i (= index of the edge with the midpoint),
                  solution path)
        """
        path_center_index, center, outside_vertex_2, i = float("nan"), float("nan"), float("nan"), float("nan")
        if n == 1:
            center = 1
            solution_value = 0
            solution_path += f"Only one vertex and hence, the center is on vertex 1."
            walked, paths, outside_vertex_2 = 0, [[0]], 0

        else:
            # Farthest vertex u from vertex 1: one end of a longest path
            dist, _ = AdditionalMethods.tree_dijkstra(matrix, 0, n)
            
            outside_vertex_1 = np.argmax(dist)

            solution_path += f"Start at vertex 1. Vertex with longest distance to vertex 1 is vertex {outside_vertex_1+1}."

            # Determine distance of next vertex to each vertex (dijkstra for trees) and save the paths
            dist, paths = AdditionalMethods.tree_dijkstra(matrix, outside_vertex_1, n)

            # Farthest vertex v from u: the path from u to v is a longest path of the tree
            outside_vertex_2 = np.argmax(dist)

            solution_value = dist[outside_vertex_2] / 2

            solution_path += f"\nVertex with longest distance to vertex {outside_vertex_1+1} is vertex {outside_vertex_2+1} with a distance of {dist[outside_vertex_2]:.4f}."

            walked = 0
            path = paths[outside_vertex_2]
            # Determine the position of the center: walk along the longest path to the first edge that reaches half
            # of its length
            
            for i in range(len(path) - 1):
                if walked + matrix[path[i], path[i + 1]] < solution_value:
                    walked += matrix[path[i], path[i + 1]]
                else:
                    path_center_index = i
                    break

        return solution_value, walked, paths, path_center_index, center, outside_vertex_2, i, solution_path