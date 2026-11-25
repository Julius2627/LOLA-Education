import numpy as np
from common.additional_methods import AdditionalMethods

class median_undirected_tree:
    """
    Median of an undirected tree, solved with Goldman's algorithm.

    Minimises f(x) = sum_k w_k * d(v_k, x). Let W be the total weight. A leaf whose (cumulative) weight is at
    least W/2 is a median: moving from it into the tree does not decrease f. Otherwise moving towards its
    neighbour decreases f, so the leaf is folded into its neighbour: the neighbour gets the leaf's weight,
    and the leaf is removed. This is repeated until a leaf has a cumulative weight of at least W/2 or only
    one vertex is left. If the cumulative weight of the median is exactly W/2, f is constant on the edge to
    its neighbour, so the neighbour and the whole edge are optimal as well.

    :param weights: weights w_k of the vertices
    :param matrix: adjacency matrix of the tree with the edge lengths, None where there is no edge
    """

    def __init__(self, weights, matrix):
        self.matrix = AdditionalMethods.tree_matrix(matrix)
        self.weights = np.asarray(weights, dtype=float)

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal vertices as 1-based vertex numbers, followed by the tuple (i, j) if the whole edge
                 (i, j) is optimal; result text; solution path; None)
        """
        HW = np.sum(self.weights) / 2

        solution_path = f"Half of the total weight is {HW:.4f}."

        n = len(self.weights)

        w_copy = self.weights.copy()
        adj_matrix = self.matrix.copy()
        vertices = [i for i in range(n)]

        # Determine the median with Goldman's algorithm (folding the leaves)
        while True:
            if len(vertices) == 1:
                # If there is one vertex left, it is the median
                rows_one = vertices
                leaf = vertices[0]
                solution_path += f"\nOnly vertex {leaf+1} is left; terminate algorithm."
                break
            # Leaves: vertices with exactly one remaining edge
            nonzero_per_row = np.sum((adj_matrix != 0) & (~np.isinf(adj_matrix)), axis=1)
            rows_one = np.where(nonzero_per_row == 1)[0]
            leaf = rows_one[0]
            if w_copy[leaf] >= HW:
                solution_path += f"\nVertex {leaf+1} now has the (cumulated) weight {w_copy[leaf]:.4f} >= {HW:.4f}; terminate algorithm."
                # If the vertex has a cumulative weight of at least half of the total weight, it is the median
                break
            else:
                neighbour = np.argmax((adj_matrix[leaf] != 0) & (~np.isinf(adj_matrix[leaf])))
                # Add leaf to its neighbour
                w_copy[neighbour] += w_copy[leaf]
                solution_path += f"\nChoose leaf vertex {leaf+1} with (cumulated) weight {w_copy[leaf]:.4f} < {HW:.4f}.\nFold (delete) vertex {leaf+1} to vertex {neighbour+1}, so vertex {neighbour+1} has cumulated weight {w_copy[neighbour]:.4f}."
                w_copy[leaf] = 0
                adj_matrix[leaf, neighbour], adj_matrix[neighbour, leaf] = np.inf, np.inf
                vertices.remove(leaf)
        
        # Determine solution value: First determine distance of median to each vertex (dijkstra for trees), then multiply with weights
        dist, _ = AdditionalMethods.tree_dijkstra(self.matrix, leaf, n)

        sol_value = np.dot(self.weights, dist)

        # Cumulative weight exactly W/2: f is constant on the edge to the neighbour, so the neighbour and the whole
        # edge are optimal as well
        if len(rows_one) >= 2 and np.isclose(w_copy[leaf], HW):
            neighbour = np.argmax((adj_matrix[leaf] != 0) & (~np.isinf(adj_matrix[leaf])))
            solution_path +=f"\nSince vertex {leaf+1} has a (cumulated) weight of exactly W/2, we have multiple optimal solutions."
            optimal_vertices = [leaf, neighbour]
            optimal_edges = [(leaf, neighbour)]
            # If the neighbour has weight 0, the optimal points can continue behind it
            if self.weights[neighbour] == 0:
                further_vertices, further_edges = self._optimal_points_behind(leaf, neighbour, HW)
                if len(further_vertices) > 0:
                    solution_path += f"\nVertex {neighbour+1} has weight 0, and behind it the optimal points continue along branches with a weight of exactly W/2 (all other branches have weight 0): the vertices {', '.join(str(v+1) for v in further_vertices)} and the edges {', '.join(f'({i+1}, {j+1})' for i, j in further_edges)} are optimal as well."
                optimal_vertices += further_vertices
                optimal_edges += further_edges
                result_string = (f'Multiple optimal points on vertices {", ".join(str(v+1) for v in optimal_vertices)} and on the complete '
                             f'edge{"s" if len(optimal_edges) > 1 else ""} {", ".join(f"({i+1}, {j+1})" for i, j in optimal_edges)}'
                             f'\nObjective function value: {sol_value:.4f}')
                optimal_solution = [v+1 for v in optimal_vertices] + [(i+1, j+1) for i, j in optimal_edges]
            else:
                result_string = f'Multiple optimal points on vertices {leaf+1}, {neighbour+1} and on the complete edge ({leaf+1}, {neighbour+1})\nObjective function value: {sol_value:.4f}'
                optimal_solution = [leaf+1, neighbour+1, (leaf+1, neighbour+1)]
        else:
            result_string = f"Optimal point at vertex {leaf+1}\nObjective function value: {sol_value:.4f}"
            optimal_solution = [leaf+1]

        return optimal_solution, result_string, solution_path, None

    def _optimal_points_behind(self, leaf, neighbour, HW):
        """
        Optimal vertices and edges behind the neighbour of a leaf with a cumulative weight of exactly W/2 (the leaf,
        its neighbour and the edge between them are optimal already). For each further vertex v, the side towards
        the leaf has the weight W/2. Moving from v into one of its other branches does not change f exactly if
        this branch also has the weight W/2, i.e. if v has weight 0 and all other branches of v have weight 0.
        Then the first vertex of this branch and the edge to it are optimal as well, and the check continues there.
        (If all weights are 0, every branch has the weight W/2 = 0, and the whole tree is optimal.)

        :param leaf: the leaf with a cumulative weight of exactly W/2 (0-based)
        :param neighbour: its neighbour (0-based)
        :param HW: half of the total weight
        :return: (further optimal vertices, further optimal edges (v, u)), 0-based
        """
        vertices, edges = [], []
        to_check = [(leaf, neighbour)]       # (vertex we came from, vertex to check)
        while len(to_check) > 0:
            previous, v = to_check.pop()
            # The optimal points can only continue behind a vertex with weight 0
            if self.weights[v] != 0:
                continue
            branches = [u for u in np.flatnonzero((self.matrix[v] != 0) & (~np.isinf(self.matrix[v]))) if u != previous]
            # Branches with a positive weight. If there is exactly one, all other branches have weight 0, so it has
            # the weight W/2 and f stays constant in it. If there is none, all weights are 0 (W = 0), f is 0
            # everywhere and every branch is optimal. If there are several, the optimal points end at v.
            positive = [u for u in branches if not self._branch_zero_test(u, v)]
            if len(positive) == 1:
                next_vertices = positive
            elif len(positive) == 0:
                next_vertices = branches
            else:
                next_vertices = []
            for u in next_vertices:
                vertices.append(int(u))
                edges.append((int(v), int(u)))
                to_check.append((v, u))
        return vertices, edges

    def _branch_zero_test(self, start, came_from):
        """
        True if every vertex of the branch of the tree that begins at the vertex `start` when coming from the vertex
        `came_from` (all vertices that can be reached from `start` without passing `came_from`) has weight 0.
        """
        to_visit = [(start, came_from)]
        while len(to_visit) > 0:
            v, parent = to_visit.pop()
            if self.weights[v] > 0:
                return False
            for u in np.flatnonzero((self.matrix[v] != 0) & (~np.isinf(self.matrix[v]))):
                if u != parent:
                    to_visit.append((u, v))
        return True