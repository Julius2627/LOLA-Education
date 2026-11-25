import numpy as np

class median_l2_metric_weighted:
    """
    Weighted median with Euclidean distances (l2 metric, Weber problem), approximated with Weiszfeld's
    algorithm.

    Minimises f(x) = sum_k w_k ||x - a_k||_2. There is no closed formula for the optimal point, so:
      1. Dominance criterion (see _check_dominance_criterion): if it holds for a customer, this customer
         is the optimal point.
      2. Otherwise Weiszfeld's algorithm starts at the weighted centroid and repeats the update
             x_new = sum_k (w_k / d_k) a_k / sum_k (w_k / d_k)   with d_k = ||x - a_k||_2
         until the relative change of the objective function value is at most delta.

    :param coordinates: the customers as lists [x1, x2, w, ...] with the weight w > 0; only the first three
                        entries are used

    :param delta: tolerance of the stopping criterion (asked for in the controller)
    """

    def __init__(self, coordinates, delta):
        numeric_coords = [point[:3] for point in coordinates]
        self.coordinates = np.array(numeric_coords, dtype=float)
        self.x_coords = self.coordinates[:, 0]
        self.y_coords = self.coordinates[:, 1]
        self.weights = self.coordinates[:, 2]

        self.delta = delta

    def run(self):
        """
        Checks the dominance criterion and, if no customer fulfils it, runs Weiszfeld's algorithm.

        :return: ([0, p] with the optimal point p = (x1, x2), result text, solution path, None)
        """
        # Check the dominance criterion
        index, solution_path = self._check_dominance_criterion()
        if len(index) == 1:
            x_k_plus_1 = self.x_coords[index[0]]
            y_k_plus_1 = self.y_coords[index[0]]
            f_k_plus_1 = self._compute_objective_function(x_k_plus_1, y_k_plus_1)
            optimal_point = [0, (float(x_k_plus_1), float(y_k_plus_1))]
            result_string = f"Optimal point according to dominance criterion at: ({x_k_plus_1:.4f} | {y_k_plus_1:.4f})\nObjective function value: {f_k_plus_1:.4f}"
            return optimal_point, result_string, solution_path, None

        # Initialize starting point (weighted centroid)
        sum_weights = np.sum(self.weights)
        x_k = np.sum(self.weights * self.x_coords) / sum_weights
        y_k = np.sum(self.weights * self.y_coords) / sum_weights
        f_k = self._compute_objective_function(x_k, y_k)

        solution_path += f"\n\nInitiating Weiszfeld algorithm."
        solution_path += f"\nInitial point: (x1: {x_k:.6f}, x2: {y_k:.6f}), objective function value = {f_k:.6f}"

        # Iteration loop
        k = 0
        while True:
            k += 1

            # On a customer the update rule would divide by 0, so the iteration stops there
            if (np.isclose(self.x_coords, x_k) & np.isclose(self.y_coords, y_k)).any():
                solution_path += ('\nCurrent point landed on a customer. Terminate and return corresponding value.')
                x_k_plus_1, y_k_plus_1, f_k_plus_1 = x_k, y_k, f_k
                break

            # Weiszfeld's update rule: x_new = sum_k (w_k / d_k) a_k / sum_k (w_k / d_k) with d_k = ||x - a_k||_2
            factor = self.weights / np.sqrt((x_k - self.x_coords) ** 2 + (y_k - self.y_coords) ** 2)

            x_k_plus_1 = np.sum(factor * self.x_coords) / np.sum(factor)
            y_k_plus_1 = np.sum(factor * self.y_coords) / np.sum(factor)

            # Compute the new objective function value
            f_k_plus_1 = self._compute_objective_function(x_k_plus_1, y_k_plus_1)
            relative_change = abs(f_k - f_k_plus_1) / f_k

            solution_path += (
                f"\nIteration {k}: x1 = {x_k_plus_1:.6f}, x2 = {y_k_plus_1:.6f}, objective function value = {f_k_plus_1:.6f}, relative change = {relative_change:.6e}"
            )

            # Stopping criterion: relative change of the objective function value at most delta
            if relative_change <= self.delta:
                solution_path += ('\nStopping criterion met.')
                break

            # Update for next iteration
            x_k, y_k, f_k = x_k_plus_1, y_k_plus_1, f_k_plus_1

        # Prepare result output
        optimal_point = [0, (float(x_k_plus_1), float(y_k_plus_1))]
        result_string = (
            f"Optimal point after {k} iterations at: ({x_k_plus_1:.4f} | {y_k_plus_1:.4f})\nObjective function value: {f_k_plus_1:.4f}"
        )

        return optimal_point, result_string, solution_path, None



    def _compute_objective_function(self, x, y):
        """
        Objective function value f(x) = sum_k w_k ||x - a_k||_2 of the point x = (x, y).
        """
        return np.sum(self.weights * np.sqrt((x - self.x_coords) ** 2 + (y - self.y_coords) ** 2))

    def _check_dominance_criterion(self):
        """
        Checks the dominance criterion: customer j is optimal if
            || sum_k w_k (a_j - a_k) / ||a_j - a_k||_2 ||_2 <= W_j,
        where the sum runs over the customers at other positions and W_j is the total weight of the
        customers at the position of j. The left side is the length of the gradient of the other summands
        of f at a_j. The check stops at the first customer that fulfils it.

        :return: ([index of the optimal customer], solution path), or ([], solution path) if no customer
                 fulfils the criterion
        """
        solution_path = "Checking dominance criterion."
        dominant_point = []
        skip = []

        for j in range(len(self.x_coords)):
            if j not in skip:
                weight_here = self.weights[j]
                same = np.zeros(len(self.x_coords), dtype=bool)
                same[j] = True
                # Customers at the same position count as one customer with the sum of their weights
                for i in range(len(self.x_coords)):
                    if i != j and np.isclose(self.x_coords[j], self.x_coords[i]) and np.isclose(self.y_coords[j],self.y_coords[i]):
                        solution_path += f'\nCustomer {j+1} and {i+1} are at the same position, so we add their weights and consider them together.'
                        skip.append(i)
                        weight_here += self.weights[i]
                        same[i] = True

                # Weighted unit vectors from the other customers to customer j; the length of their sum is compared
                # with W_j
                dx = self.x_coords[j] - self.x_coords
                dy = self.y_coords[j] - self.y_coords
                d = np.hypot(dx, dy)

                total = np.hypot(np.sum(self.weights[~same] * dx[~same] / d[~same]),
                                np.sum(self.weights[~same] * dy[~same] / d[~same]))

                solution_path += f'\nWeight of customer {j+1}: {weight_here:.4f}, value to compare: {total:.4f}'
                if total <= weight_here:
                    solution_path += f'\n\nDominance criterion is fulfilled.'
                    dominant_point.append(j)
                    return dominant_point, solution_path
        solution_path += f'\n\nDominance criterion is not fulfilled.'
        return dominant_point, solution_path