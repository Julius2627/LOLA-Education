import numpy as np
from common.additional_methods import AdditionalMethods

class center_linf_metric_weighted:
    """
    Weighted center with the maximum distance (l∞ metric), solved with the delta method.

    Minimises f(x) = max_k w_k max(|x1 - a_k1|, |x2 - a_k2|) = max(g1(x1), g2(x2)), where each dimension
    has the one-dimensional problem g(t) = max_k w_k |t - a_k|. For two customers p, q the best value of
    max(w_p |t - a_p|, w_q |t - a_q|) is
        delta_pq = w_p w_q / (w_p + w_q) * |a_q - a_p|,   reached at t = (w_p a_p + w_q a_q) / (w_p + w_q).
    The optimal value of g is the largest delta_pq, and the optimal t is that of this pair. The optimal
    value of the problem is z = max(z1, z2). If z1 = z2, the point (x1*, x2*) is the only optimal point;
    otherwise the coordinate of the dimension with the smaller value can vary as long as its value stays at
    most z, which gives a line segment (see _output_calculation).

    :param coordinates: the customers as lists [x1, x2, w, ...] with the weight w > 0; only the first three
                        entries are used
    """

    def __init__(self, coordinates):
        numeric_coords = [point[:3] for point in coordinates]
        self.coordinates = np.array(numeric_coords, dtype=float)
        self.x_coords = self.coordinates[:, 0]
        self.y_coords = self.coordinates[:, 1]
        self.weights = self.coordinates[:, 2]

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal points, result text, solution path, None); the optimal points are
                 [0, p] for the single optimal point p,
                 or [1, p, q] if all points on the line segment from p to q are optimal
                 (points as tuples (x1, x2))
        """
        solution_path = ""
        
        x_star, y_star, max_delta_x, max_delta_y, solution_path = center_linf_metric_weighted.calculate_linf_center_weighted(self.x_coords, self.y_coords, self.weights, solution_path)

        # One optimal point if both dimensions have the same optimal value; otherwise the coordinate of the
        # dimension with the smaller value can vary
        if np.isclose(max_delta_x, max_delta_y):
            result_string = f"Optimal point: ({x_star:.4f} | {y_star:.4f})\nObjective function value: {max_delta_x:.4f}"
            optimal_point = [0, (x_star, y_star)]
            solution_path += f"\nSince the maximum deltas for x1 and x2 are the same, we have one optimal point."
        elif max_delta_x < max_delta_y:
            optimal_point, result_string, solution_path = self._output_calculation(self.x_coords, max_delta_y, y_star, 1, 2, solution_path)
        else:
            optimal_point, result_string, solution_path = self._output_calculation(self.y_coords, max_delta_x, x_star, 2, 1, solution_path)

        return optimal_point, result_string, solution_path, None



    def _output_calculation(self, coords, max_delta_other, other_star, own, other, solution_path):
        """
        Optimal points if the dimension `own` has a smaller optimal value than the dimension `other`: the other
        coordinate stays at its optimum, and the coordinate t of `own` may take every value with
        w_k |t - a_k| <= max_delta_other for all customers k, i.e.
            t in [A-, A+] = [max_k (a_k - max_delta_other / w_k), min_k (a_k + max_delta_other / w_k)].

        :param coords: coordinates of the customers in the dimension `own`
        :param max_delta_other: optimal value of the dimension `other` (= optimal value of the problem)
        :param other_star: optimal coordinate in the dimension `other`
        :param own: number of the dimension with the smaller optimal value (1 or 2)
        :param other: number of the other dimension
        :return: ([1, p, q] with the end points p, q of the optimal line segment, result text, solution path)
        """
        aMinus = np.max(coords - max_delta_other/self.weights)
        aPlus = np.min(coords + max_delta_other/self.weights)
        solution_value = max_delta_other
        solution_path += f"\nSince the maximum delta for x{own} is smaller than the maximum delta for x{other}, we have multiple optimal points."
        solution_path += f"\nA- = {aMinus:.4f}, A+ = {aPlus:.4f}."
        if own == 1:
            result_string = f'Multiple optimal points in range: ([{aMinus:.4f}, {aPlus:.4f}] x {other_star:.4f})\nObjective function value: {solution_value:.4f}'
            optimal_point = [1, (aMinus, other_star), (aPlus, other_star)]
        else:
            result_string = f'Multiple optimal points in range: ({other_star:.4f} x [{aMinus:.4f}, {aPlus:.4f}])\nObjective function value: {solution_value:.4f}'
            optimal_point = [1, (other_star, aMinus), (other_star, aPlus)]
        return optimal_point, result_string, solution_path

    @staticmethod
    def _compute_deltas(values, weights):
        """
        Delta matrix of one dimension: delta_ij = w_i w_j / (w_i + w_j) * (a_j - a_i), the best value of
        max(w_i |t - a_i|, w_j |t - a_j|) with a sign (the matrix is antisymmetric).
        """
        n = len(values)
        deltas = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                delta = (weights[i] * weights[j]) / (weights[i] + weights[j]) * (values[j] - values[i])
                deltas[i, j] = delta
                deltas[j, i] = -delta  # Ensure symmetry
        return deltas

    @staticmethod
    def _find_max_delta(deltas):
        """
        Position (p, q) and value of the largest entry of the delta matrix (since the matrix is
        antisymmetric, this is also the largest absolute value).
        """
        deltaArray = np.array(deltas)
        index = np.argmax(deltaArray)
        p, q = np.unravel_index(index, deltaArray.shape)
        max_delta = deltas[p][q]
        return p, q, max_delta

    @staticmethod
    def _compute_optimal_point(p, q, values, weights):
        """
        Optimal coordinate t* = (w_p a_p + w_q a_q) / (w_p + w_q) of the pair (p, q): the point where
        w_p |t - a_p| = w_q |t - a_q|.
        """
        return ((weights[p] * values[p]) + (weights[q] * values[q])) / (weights[p] + weights[q])

    @staticmethod
    def calculate_linf_center_weighted(x_coordinates, y_coordinates, weights, solution_path):
        """
        Delta method for both dimensions (also used by center_l1_metric_weighted for the transformed points).

        :param x_coordinates: first coordinates of the customers
        :param y_coordinates: second coordinates of the customers
        :param weights: weights of the customers
        :param solution_path: solution path so far
        :return: (x*, y*, max_delta_x, max_delta_y, solution path): the optimal coordinate and the optimal
                 value of each dimension
        """
        # Compute delta matrices for x and y
        delta_x = center_linf_metric_weighted._compute_deltas(x_coordinates, weights)
        delta_y = center_linf_metric_weighted._compute_deltas(y_coordinates, weights)

        # Find the maximum delta values
        p_x, q_x, max_delta_x = center_linf_metric_weighted._find_max_delta(delta_x)
        p_y, q_y, max_delta_y = center_linf_metric_weighted._find_max_delta(delta_y)

        # Compute optimal x* and y*
        x_star = center_linf_metric_weighted._compute_optimal_point(p_x, q_x, x_coordinates, weights)
        y_star = center_linf_metric_weighted._compute_optimal_point(p_y, q_y, y_coordinates, weights)

        # Format solution path
        solution_path += (
            f"\nDeltas x1:\n{AdditionalMethods.format_matrix(delta_x)}"
            f"\nIndex p: {p_x+1} and q: {q_x+1} for x1-direction,"
            f"\nObjective function value z for x1-direction: {max_delta_x:.4f} | x1 = {x_star:.4f},"
            f"\nDeltas x2:\n{AdditionalMethods.format_matrix(delta_y)}"
            f"\nIndex p: {p_y+1} and q: {q_y+1} for x2-direction,"
            f"\nObjective function value z for x2-direction: {max_delta_y:.4f} | x2 = {y_star:.4f}."
        )

        return x_star, y_star, max_delta_x, max_delta_y, solution_path