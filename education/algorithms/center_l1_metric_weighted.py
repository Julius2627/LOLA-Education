import numpy as np
from common.additional_methods import AdditionalMethods
from education.algorithms.center_linf_metric_weighted import center_linf_metric_weighted

class center_l1_metric_weighted:
    """
    Weighted center with Manhattan distances (l1 metric).

    Minimises f(x) = max_k w_k (|x1 - a_k1| + |x2 - a_k2|). With the transformation T = [1 1; -1 1],
        |x1| + |x2| = max(|x1 + x2|, |-x1 + x2|) = ||T x||_inf,
    so the problem becomes the weighted l∞ center of the transformed points T a_k. It is solved with the
    delta method (center_linf_metric_weighted.calculate_linf_center_weighted), and its optimal points (one
    point or a line segment) are transformed back with the inverse of T.

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
        # Transform the points with T = [1 1; -1 1]: l1 distances become l∞ distances of the transformed points
        x_transformed, y_transformed = AdditionalMethods.transform_points(self.x_coords, self.y_coords)
        output_string = ", ".join(f"({x_transformed[i]}, {y_transformed[i]})" for i in range(len(x_transformed)))
        solution_path = "Transformed points:\n[" + output_string + "]\nThe next solution outputs refer to the transformed points."

        # Weighted l∞ center of the transformed points: optimal coordinates x*, y* and the optimal values
        # max_delta_x, max_delta_y of the two dimensions
        x_star, y_star, max_delta_x, max_delta_y, solution_path = center_linf_metric_weighted.calculate_linf_center_weighted(x_transformed, y_transformed, self.weights, solution_path)

        # Transform point
        x1_optSingle, x2_optSingle = AdditionalMethods.inverse_transform(x_star, y_star)
        solution_value = np.max(self.weights*(abs(x1_optSingle - self.x_coords) + abs(x2_optSingle - self.y_coords)))

        # One optimal point if both dimensions have the same optimal value; otherwise the coordinate of the
        # dimension with the smaller value can vary
        if np.isclose(max_delta_x, max_delta_y):
            solution_path += f"\nSince the maximum deltas for x1 and x2 (transformed) are the same, we have one optimal point."
            solution_path += f"\nCenter of transformed points: ({x_star:.4f}, {y_star:.4f})"
            result_string = f"Optimal point: ({x1_optSingle:.4f} | {x2_optSingle:.4f})\nObjective function value: {solution_value:.4f}"
            optimal_point = [0, (x1_optSingle, x2_optSingle)]
        elif max_delta_x < max_delta_y:
            optimal_point, result_string, solution_path = self._output_calculation(x_transformed, max_delta_y, y_star, 1, 2, solution_value, solution_path)
        else:
            optimal_point, result_string, solution_path = self._output_calculation(y_transformed, max_delta_x, x_star, 2, 1, solution_value, solution_path)
        
        return optimal_point, result_string, solution_path, None



    def _output_calculation(self, coords, max_delta_other, other_star, own, other, solution_value, solution_path):
            """
            Optimal points if the dimension `own` has a smaller optimal value than the dimension `other`: the other
            coordinate stays at its optimum, and the coordinate t of `own` may take every value with
            w_k |t - a_k| <= max_delta_other for all customers k, i.e.
                t in [A-, A+] = [max_k (a_k - max_delta_other / w_k), min_k (a_k + max_delta_other / w_k)].

            The values are transformed coordinates; the end points of the line segment are transformed back.

            :param coords: transformed coordinates of the customers in the dimension `own`
            :param max_delta_other: optimal value of the dimension `other` (= optimal value of the problem)
            :param other_star: optimal transformed coordinate in the dimension `other`
            :param own: number of the dimension with the smaller optimal value (1 or 2)
            :param other: number of the other dimension
            :param solution_value: objective function value for the result text
            :return: ([1, p, q] with the end points p, q of the optimal line segment, result text, solution path)
            """
            aMinus = np.max(coords - max_delta_other/self.weights)
            aPlus = np.min(coords + max_delta_other/self.weights)
            solution_path += f"\nSince the maximum delta for x{own} is smaller than the maximum delta for x{other} (transformed), we have multiple optimal points."
            if own == 1:
                solution_path += f"\nA- = {aMinus:.4f}, A+ = {aPlus:.4f}.\nRange of optimal transformed points: ([{aMinus:.4f}, {aPlus:.4f}] x {other_star:.4f})\nThe corresponding points have to be transformed back into the original space."
                x1_opt1, x2_opt1 = AdditionalMethods.inverse_transform(aMinus, other_star)
                x1_opt2, x2_opt2 = AdditionalMethods.inverse_transform(aPlus, other_star)
            else:
                solution_path += f"\nA- = {aMinus:.4f}, A+ = {aPlus:.4f}.\nRange of optimal transformed points: ({other_star:.4f} x [{aMinus:.4f}, {aPlus:.4f}])\nThe corresponding points have to be transformed back into the original space."
                x1_opt1, x2_opt1 = AdditionalMethods.inverse_transform(other_star, aMinus)
                x1_opt2, x2_opt2 = AdditionalMethods.inverse_transform(other_star, aPlus)
            result_string = f'Multiple optimal points on line segment: (({x1_opt1:.4f}, {x2_opt1:.4f}) - ({x1_opt2:.4f}, {x2_opt2:.4f}))\nObjective function value: {solution_value:.4f}'
            optimal_point = [1, (x1_opt1, x2_opt1), (x1_opt2, x2_opt2)]
            return optimal_point, result_string, solution_path