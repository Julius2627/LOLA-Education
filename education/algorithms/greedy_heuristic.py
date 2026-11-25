import numpy as np
from common.additional_methods import AdditionalMethods

class greedy_heuristic:
    """
    Greedy (ADD) heuristic for the uncapacitated facility location problem.

    Uncapacitated facility location problem (UFLP): open a set X of facilities so that the fixed costs of the
    open facilities plus the costs of serving every customer from its cheapest open facility,
        F(X) = sum_{j in X} f[j] + sum_i min_{j in X} c[i, j],
    are minimal.

    The heuristic starts without an open facility and u[i] = max_j c[i, j] as the cost of customer i. In every
    iteration it computes for every candidate j the saving delta[j] = sum_i max(0, u[i] - c[i, j]) and the
    net saving omega[j] = delta[j] - f[j], opens the candidate with the largest net saving as long as it is
    positive, and sets u[i] to the cost of customer i from its cheapest open facility. Candidates with
    omega[j] <= 0 are removed, since their saving can only decrease. If no net saving is positive in the
    first iteration, the facility with the lowest total cost is opened.

    :param dist_matrix: matrix of transportation costs c[i, j] (one row per customer i, one column per facility j)
    :param fix_costs: vector of fixed costs f[j] (one value per facility)
    """

    def __init__(self, dist_matrix, fix_costs):
        self.c = np.array(dist_matrix, dtype=float)
        self.f = np.array(fix_costs, dtype=float)
        self.n = len(self.c)
        self.m = len(self.f)

    def run(self):
        """
        Runs the greedy heuristic.

        :return: ([open facilities, facility of every customer] (1-based), result text, solution path, None)
        """
        n = self.n
        m = self.m
        c = self.c
        f = self.f

        # delta: savings of the candidates, omega: net savings, J: candidates, u: current cost of every customer
        delta=[np.nan for i in range(m)]
        omega=[np.nan for i in range(m)]
        J=[i for i in range(m)]
        u=[max(c[i]) for i in range(n)]
        # F: objective function value (at the start: the costs u without fixed costs)
        F=sum(u)
        X = []
        solution_path = f"Starting u-vector u_{0} = {AdditionalMethods.format_vector(u)}."

        it = 0
        while len(J) != 0:
            it += 1
            # Savings of every remaining candidate compared with the current costs u
            for j in J:
                delta[j] = sum(max(0,u[i]-c[i][j]) for i in range(n))
                omega[j] = delta[j] - f[j]

            solution_path += f"\nWe get the vectors delta_{it} = {AdditionalMethods.format_vector(delta)} and omega_{it} = {AdditionalMethods.format_vector(omega)}."

            # Stop if no candidate has a positive net saving
            if max(omega[j] for j in J) <= 0:
                break

            # Open the candidate with the largest net saving
            omega_tilde = max(omega[k] for k in J)
            new_location = omega.index(omega_tilde)
            omega[new_location] = np.nan
            delta[new_location] = np.nan

            X.append(new_location)
            J.remove(new_location)

            F = F - omega_tilde  # now F = F(X) for the open facilities X

            solution_path += f"\nWe open a facility at location {new_location + 1}.\nCurrent objective function value is {F:.4f}."
            # Candidates without a positive net saving are removed (their saving can only decrease)
            J_copy = J.copy()
            for h in J_copy:
                if omega[h] <= 0:
                    J.remove(h)
                    solution_path += f"\nWe remove location {h + 1} from consideration since it will not be profitable anymore."
            
            # New costs of the customers: cheapest open facility
            for i in range(n):
                u[i] = min(c[i][j] for j in X)
            solution_path += f"\nNew vector u_{it} = {AdditionalMethods.format_vector(u)}."

        # No facility opened: open the one with the largest net saving, i.e. the lowest total cost
        if len(X) == 0:
            omega_tilde = max(omega[k] for k in J)
            new_location = omega.index(omega_tilde)
            X.append(new_location)
            F = f[new_location] + sum(c[i][new_location] for i in range(n))
            solution_path += f"\nAll entries in the initial omega-vector are non-positive and hence, we open one facility with the lowest total costs."
        else:
            solution_path += f"\nTerminate since there are no more profitable facilities to add."

        Assignment, X_print = AdditionalMethods.assignment_customers(self.c, self.n, X)

        solution_output = [X_print, [x + 1 for x in Assignment]]
        result_string = f"We open facilities at the location(s) {', '.join(str(x) for x in X_print)}.\nObjective function value: {F:.4f}"

        return solution_output, result_string, solution_path, None