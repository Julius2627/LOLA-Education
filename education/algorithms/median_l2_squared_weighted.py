import numpy as np

class median_l2_squared_weighted:
    """
    Weighted median with squared Euclidean distances.

    Minimises f(x) = sum_k w_k ||x - a_k||_2^2. The function is strictly convex, and its gradient
    2 sum_k w_k (x - a_k) is zero only at the weighted centroid
        x* = sum_k w_k a_k / sum_k w_k,
    which is therefore the only optimal point.

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

        :return: ([0, p] with the optimal point p = (x1, x2), result text, solution path, None)
        """
        # Weighted centroid x* = sum_k w_k a_k / sum_k w_k (formula from the lecture)
        sum_weights = np.sum(self.weights)

        x_star = np.sum(self.weights * self.x_coords) / sum_weights
        y_star = np.sum(self.weights * self.y_coords) / sum_weights

        # Calculate objective function value f(x)
        f_x = np.sum(self.weights * ((x_star - self.x_coords) ** 2 + (y_star - self.y_coords) ** 2))

        result_string = f"Optimal point: ({x_star:.4f} | {y_star:.4f})\nObjective function value: {f_x:.4f}"
        solution_path = f"Using the formula from the lecture slide, we get the solution parts:"
        solution_path += f"\nSum of weights: {sum_weights:.4f},"
        solution_path += f"\nSum of weighted x1-coordinates: {np.sum(self.weights * self.x_coords):.4f},"
        solution_path += f"\nSum of weighted x2-coordinates: {np.sum(self.weights * self.y_coords):.4f}."

        return [0, (float(x_star), float(y_star))], result_string, solution_path, None