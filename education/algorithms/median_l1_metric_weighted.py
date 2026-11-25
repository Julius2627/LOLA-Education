import numpy as np
from common.additional_methods import AdditionalMethods

class median_l1_metric_weighted:
    """
    Weighted median with Manhattan distances (l1 metric).

    Minimises f(x) = sum_k w_k (|x1 - a_k1| + |x2 - a_k2|). First the dominance criterion is checked: a
    customer with more than half of the total weight W is the only optimal point. Otherwise the objective
    function separates into the two coordinates, and each coordinate is optimal at a weighted median: the
    first coordinate (sorted ascending) at which the cumulative weight reaches W/2. If the cumulative
    weight there is exactly W/2, every value up to the next larger coordinate is optimal as well. The
    optimal points therefore form a point, a line segment or a rectangle.

    :param coordinates: the customers as lists [x1, x2, w, ...] with the weight w > 0; only the first three
                        entries are used
    """

    def __init__(self, coordinates):
        numeric_coords = [point[:3] for point in coordinates]
        self.coordinates = np.array(numeric_coords, dtype=float)
        self.x_coords = self.coordinates[:, 0]
        self.y_coords = self.coordinates[:, 1]
        self.weights = self.coordinates[:, 2]
        self.solution_path = ""

    def run(self):
        """
        Runs the algorithm.

        :return: (optimal points, result text, solution path, None); the optimal points are
                 [0, p] for the single optimal point p,
                 [1, p, q] if all points on the line segment from p to q are optimal,
                 or [2, p, q] if all points of the axis-parallel rectangle with the corners p and q are optimal
                 (points as tuples (x1, x2))
        """
        # Dominance criterion: a customer with more than half of the total weight W is the only optimal point
        half_weight = np.sum(self.weights) / 2
        self.solution_path += f"W/2 = {half_weight:.4f}"
        half_weight_reached = False

        for i, weight in enumerate(self.weights):
            if weight > half_weight and not np.isclose(weight, half_weight):
                optimal_point = [0, (self.x_coords[i], self.y_coords[i])]
                solution_value = self._objective_function_value((self.x_coords[i], self.y_coords[i]))
                result_string = f"Optimal point: ({self.x_coords[i]:.4f} | {self.y_coords[i]:.4f})\nObjective function value: {solution_value:.4f}"
                self.solution_path +=f"\nDominance criterion met at customer {i+1}, who has weight {weight:.4f}."
                return optimal_point, result_string, self.solution_path, None

            elif np.isclose(weight, half_weight):  # exactly W/2: optimal, but maybe not the only optimal point
                self.solution_path +=f"\nDominance criterion met at customer {i+1}, who has weight {weight:.4f}.\nHowever, as it is exactly half the total weight, we need to check if there are multiple optimal points."
                half_weight_reached = True
        if half_weight_reached == False:
            self.solution_path +=f"\nDominance criterion is not met at any point."

        # Otherwise each coordinate is optimal at a weighted median of the customers' coordinates
        x_median = self.weighted_median(self.x_coords, half_weight, 1)
        y_median = self.weighted_median(self.y_coords, half_weight, 2)

        solution_value = self._objective_function_value((x_median[0], y_median[0]))
        
        # One optimal coordinate in both dimensions: a point; an interval in one dimension: a line segment; in
        # both: a rectangle
        if len(x_median) == 1:
            if len(y_median) == 1:
                result_string = f"Optimal point: ({x_median[0]:.4f} | {y_median[0]:.4f})\nObjective function value: {solution_value:.4f}"
                optimal_point = [0, (x_median[0], y_median[0])]
            else:
                result_string = f'Multiple optimal points in range: ({x_median[0]:.4f} x [{y_median[0]:.4f}, {y_median[1]:.4f}])\nObjective function value: {solution_value:.4f}'
                optimal_point = [1, (x_median[0], y_median[0]), (x_median[0], y_median[1])]
        else:
            if len(y_median) == 1:
                result_string = f'Multiple optimal points in range: ([{x_median[0]:.4f}, {x_median[1]:.4f}] x {y_median[0]:.4f})\nObjective function value: {solution_value:.4f}'
                optimal_point = [1, (x_median[0], y_median[0]), (x_median[1], y_median[0])]
            else:
                result_string = f'Multiple optimal points in range: ([{x_median[0]:.4f}, {x_median[1]:.4f}] x [{y_median[0]:.4f}, {y_median[1]:.4f}])\nObjective function value: {solution_value:.4f}'
                optimal_point = [2, (x_median[0], y_median[0]), (x_median[1], y_median[1])]

        return optimal_point, result_string, self.solution_path, None



    def _objective_function_value(self, point):
        """
        Objective function value f(x) = sum_k w_k (|x1 - a_k1| + |x2 - a_k2|) of the point x = (x1, x2).
        """
        return (np.sum(self.weights * (np.abs(point[0] - self.x_coords) + np.abs(point[1] - self.y_coords))))

    def weighted_median(self, values, half_weight, dimension):
        """
        Weighted median of the customers' coordinates in one dimension: sorts the customers by this
        coordinate and takes the first coordinate at which the cumulative weight reaches W/2. If the
        cumulative weight there is exactly W/2, every value up to the next larger coordinate is optimal.

        :param values: the coordinates of the customers in this dimension
        :param half_weight: W/2, half of the total weight
        :param dimension: 1 or 2 (only for the solution path)
        :return: [optimal coordinate] or [smallest optimal coordinate, largest optimal coordinate]
        """
        if dimension == 1:
            self.solution_path +=f"\nSorting customers according to x1-coordinates, we get:"
        else:
            self.solution_path +=f"\nSorting customers according to x2-coordinates, we get:"
        
        sorted_indices = np.argsort(values)
        sorted_values = values[sorted_indices]
        sorted_weights = self.weights[sorted_indices]

        self.solution_path +=f"\nSorted coordinates: {AdditionalMethods.format_vector(sorted_values)},"
        self.solution_path +=f"\nSorted indices: {AdditionalMethods.format_vector(sorted_indices+1)},"
        self.solution_path +=f"\nSorted weights: {AdditionalMethods.format_vector(sorted_weights)},"

        cumulative_weight = np.cumsum(sorted_weights)

        self.solution_path +=f"\nCumulated sorted weights: {AdditionalMethods.format_vector(cumulative_weight)},"

        # First position at which the cumulative weight reaches W/2 (with a tolerance for rounding errors)
        median_index = int(np.argmax((cumulative_weight > half_weight) | np.isclose(cumulative_weight, half_weight)))
        resulting_coordinate = [float(sorted_values[median_index])]

        self.solution_path +=f"\nMedian index: {median_index+1} with coordinate {resulting_coordinate[0]:.4f}."

        # Cumulative weight exactly W/2: every value up to the next larger coordinate is optimal as well
        if np.isclose(cumulative_weight[median_index], half_weight) and median_index + 1 < len(values):
            if sorted_values[median_index] != sorted_values[median_index + 1]:
                resulting_coordinate.append(float(sorted_values[median_index + 1]))
                self.solution_path +=f"\nSince at the x{dimension}-median coordinate, we get a cumulative weight of exactly W/2, we have multiple optimal points for this dimension."
            else:
                self.solution_path +=f"\nWe have only one optimal point for the x{dimension}-dimension."
        else:
            self.solution_path +=f"\nWe have only one optimal point for the x{dimension}-dimension."

        return resulting_coordinate