import numpy as np
from common.additional_methods import AdditionalMethods

class interchange_heuristic:
    """
    Interchange (swap) heuristic for the uncapacitated facility location problem.

    Uncapacitated facility location problem (UFLP): open a set X of facilities so that the fixed costs of the
    open facilities plus the costs of serving every customer from its cheapest open facility,
        F(X) = sum_{j in X} f[j] + sum_i min_{j in X} c[i, j],
    are minimal.

    Starting from a given set X of open facilities, the heuristic evaluates in every iteration every
    interchange of one open facility x with one closed facility j. If the best interchange is cheaper than
    the current solution, it is carried out and the next iteration starts; otherwise the heuristic stops.

    :param dist_matrix: matrix of transportation costs c[i, j] (one row per customer i, one column per facility j)
    :param fix_costs: vector of fixed costs f[j] (one value per facility)

    :param X: the starting solution, the open facilities (1-based)
    """

    def __init__(self, dist_matrix, fix_costs, X):
        self.c = np.array(dist_matrix, dtype=float)
        self.f = np.array(fix_costs, dtype=float)
        self.n = len(self.c)
        self.m = len(self.f)
        self.X = X


    def run(self):
        """
        Runs the interchange heuristic.

        :return: ([open facilities, facility of every customer] (1-based), result text, solution path, None)
        """
        n = self.n
        m = self.m
        c = self.c
        f = self.f
        # The given solution is 1-based; J: the closed facilities
        self.X = [x - 1 for x in self.X]
        X = self.X

        J = [i for i in range(m)]

        for i in X:
            J.remove(i)
        F = self._cost(X)
        
        solution_path = f"Objective function value of the given solution: {F:.4f}."

        if len(X) == m:
            next_it = False
            solution_path += f"\nAll facilities are already opened, so we cannot interchange any facilities. Terminate algorithm."
        else:
            next_it = True

        while next_it:
            next_it = False
            F_star = np.inf
            # Every interchange of an open facility x with a closed facility j
            for x in X:
                for j in J:
                    J_dash = J.copy()
                    X_dash = X.copy()
                    J_dash.remove(j)
                    X_dash.remove(x)
                    X_dash.append(j)
                    J_dash.append(x)
                    X_dash.sort()
                    J_dash.sort()
                    X_print = [x + 1 for x in X_dash]
                    F_dash = self._cost(X_dash)
                    solution_path += f"\nX' = [{', '.join(str(x) for x in X_print)}] with objective function value {F_dash:.4f}."
                    if F_star > F_dash:
                        F_star = F_dash
                        X_star = X_dash.copy()
                        J_star = J_dash.copy()
            X_print = [x + 1 for x in X_star]
            solution_path += f"\nBest found solution of this iteration is X* = [{', '.join(str(x) for x in X_print)}] with objective function value {F_star:.4f}."
            # Carry out the best interchange if it improves the solution, otherwise stop
            if F > F_star:
                X = X_star.copy()
                J = J_star.copy()
                F = F_star
                J_print = [x + 1 for x in J_star]
                next_it = True
                solution_path += f"\nImprovement in this iteration, X = [{', '.join(str(x) for x in X_print)}] with objective function value {F_star:.4f}, and J = [{', '.join(str(x) for x in J_print)}]."
            else:
                solution_path += f"\nNo improvement, terminate."

        # Every customer is assigned to its cheapest open facility
        Assignment, X_print = AdditionalMethods.assignment_customers(self.c, self.n, X)

        solution_output = [X_print, [x + 1 for x in Assignment]]
        result_string = f"We open facilities at the location(s) {', '.join(str(x) for x in X_print)}.\nObjective function value: {F:.4f}"

        return solution_output, result_string, solution_path, None



    def _cost(self, Solution):
        """
        Objective function value F(X): fixed costs of the open facilities plus the cost of every customer at
        its cheapest open facility.

        :param Solution: the open facilities (0-based)
        """
        return sum(self.f[i] for i in Solution) + sum(min(self.c[i,j] for j in Solution) for i in range(self.n))