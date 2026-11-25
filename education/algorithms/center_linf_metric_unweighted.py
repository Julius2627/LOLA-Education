import numpy as np

class center_linf_metric_unweighted:
    """
    Unweighted center with the maximum distance (l∞ metric): the smallest axis-parallel square that
    covers all customers.

    Minimises f(x) = max_k max(|x1 - a_k1|, |x2 - a_k2|) = max(max_k |x1 - a_k1|, max_k |x2 - a_k2|).
    Each coordinate is best at the midpoint of the bounding rectangle of the customers, with half of the
    side length as value, so the optimal value is half of the longer side. If the bounding rectangle is a
    square, its midpoint is the only optimal point. Otherwise the coordinate along the shorter side can
    vary: the optimal points form the line segment between the midpoints of the two squares that extend
    the rectangle along its shorter side, once in each direction.

    :param coordinates: the customers as lists [x1, x2, ...]; only the first two entries are used
    """

    def __init__(self, coordinates):
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
        solution_path = ""

        # Midpoints m1, m2 of the two candidate squares (m1 = m2 if the bounding rectangle is a square)
        m1, m2, min_x, max_x, min_y, max_y, solution_value, solution_path = self.calculate_linf_center_unweighted(self.x_coords, self.y_coords, solution_path)

        if np.allclose(m1, m2):
            result_string = f"Optimal point: ({m1[0]:.4f} | {m1[1]:.4f})\nObjective function value: {solution_value:.4f}"
            optimal_point = [0, (m1[0], m1[1])]
        elif (max_x - min_x) > (max_y - min_y):  # wider than high: x1 fixed, x2 varies
            result_string = f'Multiple optimal points in range: ({m1[0]:.4f} x [{m1[1]:.4f}, {m2[1]:.4f}])\nObjective function value: {solution_value:.4f}'
            optimal_point = [1, (m1[0], m1[1]), (m1[0], m2[1])]
        else:  # higher than wide: x2 fixed, x1 varies
            result_string = f'Multiple optimal points in range: ([{m1[0]:.4f}, {m2[0]:.4f}] x {m1[1]:.4f})\nObjective function value: {solution_value:.4f}'
            optimal_point = [1, (m1[0], m1[1]), (m2[0], m1[1])]

        # Return a list of optimal points, the result string, and the solution path.
        return optimal_point, result_string, solution_path, None



    @staticmethod
    def calculate_linf_center_unweighted(x_coordinates, y_coordinates, solution_path):
        """
        Unweighted l∞ center of the given points (also used by center_l1_metric_unweighted for the transformed
        points).

        :param x_coordinates: first coordinates of the customers
        :param y_coordinates: second coordinates of the customers
        :param solution_path: solution path so far
        :return: (m1, m2, min_x, max_x, min_y, max_y, optimal value, solution path) with the midpoints m1, m2
                 of the two candidate squares (m1 = m2 if the bounding rectangle is a square)
        """
        # Compute the bounding rectangle
        min_x, max_x = np.min(x_coordinates), np.max(x_coordinates)
        min_y, max_y = np.min(y_coordinates), np.max(y_coordinates)
        solution_path += f"\nBounding rectangle: X1min={min_x:.4f}, X2min={min_y:.4f}, X1max={max_x:.4f}, X2max={max_y:.4f}"

        solution_point_x1 = (max_x + min_x) / 2
        solution_point_x2 = (max_y + min_y) / 2
        solution_value = max((max_x - min_x) / 2, (max_y - min_y) / 2)

        # Check if the rectangle is already a square
        if np.isclose((max_x - min_x), (max_y - min_y)):
            midpoint = (solution_point_x1, solution_point_x2)
            solution_path += f"\nBounding rectangle is a square (X1max - X1min = X2max - X2min), so the midpoint is the only optimal solution."
            return midpoint, midpoint, min_x, max_x, min_y, max_y, solution_value, solution_path

        # Stretch the rectangle into two candidate squares
        solution_path += f"\nBounding rectangle is not a square. Consequently, there are multiple optimal solutions."
        if (max_x - min_x) > (max_y - min_y):
            diff = (max_x - min_x) - (max_y - min_y)
            # Extend upward and downward.
            q1 = ((min_x, min_y), (max_x, max_y + diff))
            q2 = ((min_x, min_y - diff), (max_x, max_y))
            solution_path += f"\n\nLength of bounding rectangle in x1-direction is larger than in x2-direction. Extend bounding rectangle in x2-direction."
        else:
            diff = (max_y - min_y) - (max_x - min_x)
            # Extend to the right and left.
            q1 = ((min_x, min_y), (max_x + diff, max_y))
            q2 = ((min_x - diff, min_y), (max_x, max_y))
            solution_path += f"\n\nLength of bounding rectangle in x2-direction is larger than in x1-direction. Extend bounding rectangle in x1-direction."
        solution_path += f"\nCandidate square Q1: (({q1[0][0]:.4f}, {q1[0][1]:.4f}), ({q1[1][0]:.4f}, {q1[1][1]:.4f}))\nCandidate square Q2: (({q2[0][0]:.4f}, {q2[0][1]:.4f}), ({q2[1][0]:.4f}, {q2[1][1]:.4f}))"

        # Compute the midpoints of the two candidate squares
        m1 = ((q1[0][0] + q1[1][0]) / 2, (q1[0][1] + q1[1][1]) / 2)
        m2 = ((q2[0][0] + q2[1][0]) / 2, (q2[0][1] + q2[1][1]) / 2)
        solution_path += f"\nCandidate midpoint Q1: ({m1[0]:.4f}, {m1[1]:.4f})\nCandidate midpoint Q2: ({m2[0]:.4f}, {m2[1]:.4f})"

        return m1, m2, min_x, max_x, min_y, max_y, solution_value, solution_path