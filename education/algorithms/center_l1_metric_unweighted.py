import numpy as np
from common.additional_methods import AdditionalMethods
from education.algorithms.center_linf_metric_unweighted import center_linf_metric_unweighted

class center_l1_metric_unweighted:
    """
    Unweighted center with Manhattan distances (l1 metric).

    Minimises f(x) = max_k (|x1 - a_k1| + |x2 - a_k2|). With the transformation T = [1 1; -1 1],
        |x1| + |x2| = max(|x1 + x2|, |-x1 + x2|) = ||T x||_inf,
    so the problem becomes the unweighted l∞ center of the transformed points T a_k. It is solved by
    center_linf_metric_unweighted.calculate_linf_center_unweighted, and its optimal points (one point or a
    line segment) are transformed back with the inverse of T.

    :param coordinates: the customers as lists [x1, x2, ...]; only the first two entries are used
    """

    def __init__(self, coordinates):
        # Use only the first two elements (x and y) from each point.
        numeric_coords = [point[:2] for point in coordinates]
        self.coordinates = np.array(numeric_coords, dtype=float)
        self.x_coords = self.coordinates[:, 0]
        self.y_coords = self.coordinates[:, 1]

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

        # Unweighted l∞ center of the transformed points: midpoints m1, m2 of the two candidate squares
        m1, m2, _, _, _, _, _, solution_path = center_linf_metric_unweighted.calculate_linf_center_unweighted(x_transformed, y_transformed, solution_path)

        # m1 = m2: one optimal point, transformed back
        if np.allclose(m1, m2):
            solution_path += f"\nMidpoint of transformed points: ({m1[0]:.4f}, {m1[1]:.4f})"
            midpoint_originalx1, midpoint_originalx2 = AdditionalMethods.inverse_transform(m1[0], m1[1])
            solution_value = np.max(np.abs(midpoint_originalx1 - self.x_coords) + np.abs(midpoint_originalx2 - self.y_coords))
            result_string = f"Optimal point: ({midpoint_originalx1:.4f} | {midpoint_originalx2:.4f})\nObjective function value: {solution_value:.4f}"
            optimal_point = [0, (midpoint_originalx1, midpoint_originalx2)]
            return optimal_point, result_string, solution_path, None


        # Otherwise all points of the line segment from m1 to m2 are optimal; transform both end points back
        midpoint_originalx1_1, midpoint_originalx2_1 = AdditionalMethods.inverse_transform(m1[0],m1[1])
        midpoint_originalx1_2, midpoint_originalx2_2 = AdditionalMethods.inverse_transform(m2[0],m2[1])
        solution_path += f"\nMidpoint 1 of original points: ({midpoint_originalx1_1:.4f}, {midpoint_originalx2_1:.4f})"
        solution_path += f"\nMidpoint 2 of original points: ({midpoint_originalx1_2:.4f}, {midpoint_originalx2_2:.4f})"
        solution_value = np.max(np.abs(midpoint_originalx1_1 - self.x_coords) + np.abs(midpoint_originalx2_1 - self.y_coords))
        result_string = f'Multiple optimal points on line segment: (({midpoint_originalx1_1:.4f}, {midpoint_originalx2_1:.4f}) - ({midpoint_originalx1_2:.4f}, {midpoint_originalx2_2:.4f}))\nObjective function value: {solution_value:.4f}'
        optimal_point = [1, (midpoint_originalx1_1, midpoint_originalx2_1), (midpoint_originalx1_2, midpoint_originalx2_2)]

        # Return a list of optimal points, the result string, and the solution path.
        return optimal_point, result_string, solution_path, None
