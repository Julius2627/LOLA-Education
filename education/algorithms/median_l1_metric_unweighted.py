import numpy as np
from common.additional_methods import AdditionalMethods

class median_l1_metric_unweighted:
    """
    Unweighted median with Manhattan distances (l1 metric).

    Minimises f(x) = sum_k (|x1 - a_k1| + |x2 - a_k2|). The objective function separates into the two
    coordinates, and each coordinate is optimal at a median of the customers' coordinates:
      - odd number n of customers: the middle coordinate, so there is exactly one optimal point;
      - even n: every value between the (n/2)-th and the (n/2+1)-th smallest coordinate, so all points
        of the rectangle spanned by these values are optimal.

    :param coordinates: the customers as lists [x1, x2, ...]; only the first two entries are used
    """

    def __init__(self, coordinates):

        numeric_coords = [point[:2] for point in coordinates]
        self.points = np.array(numeric_coords, dtype=float)
        self.x_coords = self.points[:, 0]
        self.y_coords = self.points[:, 1]

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal points, result text, solution path, None); the optimal points are
                 [0, p] for the single optimal point p,
                 or [2, p, q] if all points of the axis-parallel rectangle with the corners p and q are optimal
                 (points as tuples (x1, x2))
        """
        # Median of each coordinate (for an even number of customers np.median returns the mean of the two middle
        # values)
        x_median = np.median(self.x_coords)
        y_median = np.median(self.y_coords)
        solution_value = np.sum(np.abs(x_median - self.x_coords)) + np.sum(np.abs(y_median - self.y_coords))
        
        # Odd number of customers: unique medians, one optimal point
        if (len(self.x_coords) % 2 != 0):
            result_string = f'Optimal point: ({x_median:.4f} | {y_median:.4f})\nObjective function value: {solution_value:.4f}'
            optimal_point = [0, (x_median, y_median)]
            solution_string = f"\nx1 coordinates: {AdditionalMethods.format_vector(self.x_coords)}\nx1 median: {x_median:.4f}"
            solution_string +=f"\nx2 coordinates: {AdditionalMethods.format_vector(self.y_coords)}\nx2 median: {y_median:.4f}"
        else:
            # Even number of customers: the rectangle between the (n/2)-th and the (n/2+1)-th smallest coordinates
            sorted_x_coords = np.sort(self.x_coords)
            sorted_y_coords = np.sort(self.y_coords)
            n = len(self.x_coords);
            lower, upper = int(n / 2 - 1), int(n / 2)
            x_low, x_high = sorted_x_coords[lower], sorted_x_coords[upper]
            y_low, y_high = sorted_y_coords[lower], sorted_y_coords[upper]
            result_string = f'Multiple optimal points in range: ([{x_low:.4f}, {x_high:.4f}] x [{y_low:.4f}, {y_high:.4f}])\nObjective function value: {solution_value:.4f}'
            optimal_point = [2, (x_low, y_low), (x_high, y_high)]
            solution_string = f"\nx1 coordinates: {AdditionalMethods.format_vector(self.x_coords)}\nx1 coordinate of point at position n/2: {x_low:.4f}\nx1 coordinate of point at position n/2+1: {x_high:.4f}"
            solution_string +=f"\nx2 coordinates: {AdditionalMethods.format_vector(self.y_coords)}\nx2 coordinate of point at position n/2: {y_low:.4f}\nx2 coordinate of point at position n/2+1: {y_high:.4f}"
        
        return optimal_point, result_string, solution_string, None
