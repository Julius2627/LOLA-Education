"""DUALOC (Erlenkotter 1978) for the uncapacitated facility location problem (UFLP).

Notation (customers i and facilities j are numbered from 0 in the code and from 1 in all texts):
    c[i, j]  cost of serving customer i from facility j
    f[j]     fixed cost of facility j
    v[i]     dual value of customer i
    s[j]     slack of facility j = f[j] - sum over all customers i of max(0, v[i] - c[i, j])
The sum of the v-values is a lower bound, the cost of a constructed solution an upper bound.
"""

import numpy as np
from common.additional_methods import AdditionalMethods

# All values are rounded to 10 decimal places after every addition and subtraction (function
# clean). This removes tiny floating-point errors (e.g. 0.1 + 0.2 = 0.30000000000000004), so that
# tests like "s[j] == 0" work and the solution path shows clean numbers.
DECIMALS = 10


def clean(value):
    """Rounds the value to DECIMALS decimal places and returns it as a plain Python number
    (a list of numpy numbers would be printed as [np.float64(3.0), ...] in the solution path)."""
    return float(round(value, DECIMALS))


class dualoc:
    """
    Exact solution of the uncapacitated facility location problem with DUALOC (Erlenkotter 1978).

    Uncapacitated facility location problem (UFLP): open a set X of facilities so that the fixed costs of the
    open facilities plus the costs of serving every customer from its cheapest open facility,
        F(X) = sum_{j in X} f[j] + sum_i min_{j in X} c[i, j],
    are minimal.

    Every node of the branch and bound tree runs
      1. dual ascent: raise the dual values v[i] as far as the slacks s[j] allow (lower bound sum of v),
      2. construction heuristic: a solution from the facilities with slack 0 (upper bound),
      3. dual adjust while the bounds differ: try to raise the sum of v further and construct again.
    If dual adjust brings no improvement, the node branches on a facility (kept closed / definitely
    opened). The best solution found is optimal once all nodes are processed.

    :param dist_matrix: matrix of transportation costs c[i, j] (one row per customer i, one column per facility j)
    :param fix_costs: vector of fixed costs f[j] (one value per facility)
    """

    def __init__(self, dist_matrix, fix_costs):
        # Copy the input into numpy arrays (the input itself is not changed)
        self.c = np.array(dist_matrix, dtype=float)
        self.f = np.array(fix_costs, dtype=float)
        self.n = len(self.c)    # number of customers
        self.m = len(self.f)    # number of potential facilities

        # Big M: fixed cost of a facility that is kept closed in a branch and bound node
        # (sum of all fixed costs plus, for every facility, its largest transportation cost;
        # np.max(self.c, axis=0) = largest value of every column)
        self.M = np.sum(self.f) + np.sum(np.max(self.c, axis=0))

        # Every row of c sorted from small to large: the levels v[i] passes in the dual ascent
        self.c_sort = [np.sort(self.c[i]) for i in range(self.n)]


    def run(self):
        """
        Runs DUALOC.

        :return: ([open facilities, facility of every customer] (1-based), result text, solution path, None)
        """
        n = self.n
        m = self.m
        c = self.c
        f = self.f
        M = self.M
        c_sort = self.c_sort
        I_vector = [i for i in range(n)]

        solution_path = f"Sorted c-values:\n{AdditionalMethods.format_matrix(c_sort)}"

        # Branch and bound: a node is [facilities kept closed, facilities definitely opened].
        # The first node fixes nothing; the nodes are processed in the order they were created.
        open_nodes = [[[], []]]

        # Best found solution (incumbent); at the start: facility 1 alone
        best_found_solution = [0]
        best_found_assignment = [0 for i in range(n)]
        best_found_solution_value = clean(f[0] + sum([c[i, 0] for i in I_vector]))

        while len(open_nodes) != 0:
            node = open_nodes.pop(0)
            if len(node[0]) != 0 or len(node[1]) != 0:
                if len(node[0]) == 0:
                    solution_path += f"\nConsidering the node where we definitely open facilities at locations {[j+1 for j in node[1]]} (setting their fixed costs to zero)."
                elif len(node[1]) == 0:
                    solution_path += f"\nConsidering the node where we definitely keep facilities closed at {[j+1 for j in node[0]]} (setting their fixed costs to Big M)."
                else:
                    solution_path += f"\nConsidering the node where we definitely open facilities at locations {[j+1 for j in node[1]]} (setting their fixed costs to zero) and keep them closed at {[j+1 for j in node[0]]} (setting their fixed costs to Big M)."

            # Fixed costs of this node: Big M for the closed facilities, 0 for the opened ones
            f_node = f.copy()
            for j in node[0]:
                f_node[j] = M
            for j in node[1]:
                f_node[j] = 0.0
            # The real fixed costs of the definitely opened facilities (paid in every solution of the node)
            fixed_costs_opened = sum([f[j] for j in node[1]])

            # Every node starts again with v[i] = smallest c[i, j] and the slacks that belong to it
            v_vector = [clean(c_sort[i][0]) for i in I_vector]
            s_vector = [clean(f_node[j] - sum([max(0, v_vector[i] - c[i, j]) for i in I_vector])) for j in range(m)]

            v_vector, s_vector, solution_path = self.dual_ascent(v_vector, s_vector, I_vector, solution_path)
            improvement = True
            old_v_solution = v_vector.copy()

            while improvement:
                opened_facilities, assignment_vector, potential_facilities, solution_path = self.construction_heuristic(v_vector, s_vector, solution_path)
                transport_costs = sum([c[i, assignment_vector[i]] for i in range(n)])
                # Upper bound of the node: cost of the solution with the fixed costs of the node
                current_sol_value = clean(transport_costs + sum([f_node[j] for j in opened_facilities]))
                # Actual objective function value of the solution (real fixed costs)
                actual_current_solution_value = clean(transport_costs + sum([f[j] for j in opened_facilities]))
                current_solution = opened_facilities.copy()
                current_assignment = assignment_vector.copy()
                # Lower bound of the node: sum of the v-values
                lower_bound = clean(sum(v_vector))

                if lower_bound == current_sol_value:
                    solution_path += f"\nOur lower bound (sum of v = {lower_bound}) at the current node is equal to the upper bound at the current node (objective function value with possibly adjusted fixed costs: {current_sol_value})."
                    if actual_current_solution_value < best_found_solution_value:
                        solution_path += f"\nThe actual objective function value of our solution is better than the best found solution; update the incumbent and fathom the node."
                        best_found_solution_value = actual_current_solution_value
                        best_found_solution = current_solution.copy()
                        best_found_assignment = current_assignment.copy()
                    else:
                        solution_path += f"\nThe actual objective function value of our solution is not better than the best found solution; fathom the node."
                    improvement = False
                else:
                    # Every constructed solution is feasible, so it can improve the incumbent
                    if actual_current_solution_value < best_found_solution_value:
                        solution_path += f"\nThe actual objective function value of our solution ({actual_current_solution_value}) is better than the best found solution; update the incumbent."
                        best_found_solution_value = actual_current_solution_value
                        best_found_solution = current_solution.copy()
                        best_found_assignment = current_assignment.copy()

                    # No solution of this node can be better than the lower bound plus the real fixed
                    # costs of the definitely opened facilities
                    if clean(lower_bound + fixed_costs_opened) >= best_found_solution_value:
                        solution_path += f"\nOur lower bound at the current node (sum of v plus the fixed costs of the definitely opened facilities: {clean(lower_bound + fixed_costs_opened)}) is not smaller than the objective function value of the best found solution ({best_found_solution_value}); fathom the node."
                        improvement = False
                        continue

                    solution_path += f"\nOur lower bound (sum of v = {lower_bound}) at the current node is strictly smaller than the upper bound at the current node (objective function value with possibly adjusted fixed costs: {current_sol_value}). We perform the dual adjust procedure."
                    v_vector, s_vector, solution_path = self.dual_adjust(v_vector, s_vector, opened_facilities, potential_facilities, solution_path)

                    # Dual adjust has helped only if the sum of the v-values (lower bound) has increased
                    if clean(sum(v_vector)) <= clean(sum(old_v_solution)):
                        improvement = False
                        # Branch on the first facility that is neither closed nor opened in this node
                        successful = False
                        for j in range(m):
                            if j not in node[0] and j not in node[1]:
                                successful = True
                                break
                        if successful:
                            new_nodes_0part = node[0].copy()
                            new_nodes_1part = node[1].copy()
                            new_nodes_0part.append(j)
                            new_nodes_1part.append(j)
                            new_node0 = [new_nodes_0part, node[1].copy()]
                            new_node1 = [node[0].copy(), new_nodes_1part]
                            open_nodes.append(new_node0)
                            open_nodes.append(new_node1)
                            solution_path += f"\nApplying dual adjust brought no new solution; branch (fix) location {j+1}."
                        else:
                            solution_path += f"\nApplying dual adjust brought no new solution and further branching is not possible; fathom the node."
                    else:
                        old_v_solution = v_vector.copy()
                        solution_path += f"\nApplying dual adjust brought a new solution; construct the solution."

        solution_path += f"\nNo undiscovered nodes left; terminate."
        solution_output = [[x + 1 for x in best_found_solution], [x + 1 for x in best_found_assignment]]
        result_string = f"We open facilities at the location(s) {', '.join(str(x+1) for x in best_found_solution)}.\nObjective function value: {best_found_solution_value:.4f}"

        return solution_output, result_string, solution_path, None



    def dual_ascent(self, v, s, I_start, solution_path):
        """
        Raises the v-values of the customers in I_start as far as the slacks s allow.
        v and s are changed and returned.
        """
        n = self.n
        m = self.m
        c = self.c
        c_sort = self.c_sort

        I = I_start.copy()      # customers whose v-value can still be raised

        solution_path += f"\nStarting dual ascent for customers {[i+1 for i in I]}."

        # J_i[i] = facilities j with c[i, j] <= v[i]; their slack decreases when v[i] is raised
        J_i = [[j for j in range(m) if v[i] >= c[i, j]] for i in range(n)]

        for i in I:
            solution_path += f"\nStarting values for customer {i + 1}: v_{i+1} = {v[i]}, J_{i + 1} = {[j+1 for j in J_i[i]]}."

        while len(I) != 0:
            # One round: every customer still in I is raised once (by at most one level)
            I_copy = I.copy()
            for i in I_copy:
                # delta_i = smallest slack in J_i: v[i] cannot be raised by more than this
                delta_i = min([s[j] for j in J_i[i]])
                if delta_i == 0:
                    solution_path += f"\nWe get delta_{i+1} = 0; remove {i + 1}."
                    I.remove(i)
                    continue

                # Next level: the smallest c[i, j] that is larger than v[i] (if there is one)
                larger = [value for value in c_sort[i] if value > v[i]]

                # Raise v[i] up to the next level, but at most by delta_i
                if len(larger) == 0:
                    delta = delta_i
                else:
                    delta = min(delta_i, clean(min(larger) - v[i]))

                v[i] = clean(v[i] + delta)
                for j in J_i[i]:
                    s[j] = clean(s[j] - delta)
                J_i[i] = [j for j in range(m) if v[i] >= c[i, j]]

                # If a slack has reached 0, v[i] cannot be raised any more
                if delta == delta_i:
                    I.remove(i)
                    solution_path += f"\nWe get delta_{i+1} = {delta_i}, delta = {delta}, v_{i+1} = {v[i]}, s-vector = {s}, J_{i+1} = {[j+1 for j in J_i[i]]}; remove {i + 1} as delta_i = delta."
                else:
                    solution_path += f"\nWe get delta_{i+1} = {delta_i}, delta = {delta}, v_{i+1} = {v[i]}, s-vector = {s}, J_{i+1} = {[j+1 for j in J_i[i]]}."
        solution_path += f"\nStop dual ascent as set I is empty. Final v-values: {v}, final s-values: {s}."
        return v, s, solution_path

    def construction_heuristic(self, v, s, solution_path):
        """
        Builds a solution from the facilities with slack 0 (J+).
        Returns the opened facilities X, the assignment of the customers, J+ and the solution path.
        """
        n = self.n
        m = self.m
        I = [i for i in range(n)]
        c = self.c

        J = [j for j in range(m)]
        J_plus = [j for j in J if s[j] == 0]    # facilities whose fixed cost is completely paid
        solution_path += f"\nStarting construction heuristic with v = {v} and s = {s}. We have J+ = {[j+1 for j in J_plus]}."
        X = []      # opened facilities

        # J_i[i] = facilities in J+ that customer i can use: c[i, j] <= v[i]
        # Step 1: a customer with only one such facility needs it, so it is opened
        J_i = []
        for i in I:
            J_i.append([j for j in J_plus if c[i, j] <= v[i]])
            if len(J_i[i]) == 1:
                if J_i[i][0] not in X:
                    X.append(J_i[i][0])
                    solution_path += f"\nSince {i+1} can only be assigned to {J_i[i][0]+1}, we open {J_i[i][0] + 1}."
                else:
                    solution_path += f"\nWe can assign {i+1} to opened facility {J_i[i][0] + 1}."

        # Step 2: a customer with two or more such facilities uses an opened one; if none of them
        # is open, the cheapest of them (smallest c[i, j]) is opened
        for i in I:
            if len(J_i[i]) >= 2:
                opened = [j for j in J_i[i] if j in X]
                if len(opened) > 0:
                    solution_path += f"\nWe can assign {i+1} to an opened facility from {[k+1 for k in opened]}."
                    continue

                # c[i, J_i[i]] = costs of customer i at the facilities in J_i[i]; np.argmin gives the
                # position of the smallest one (the first one if several are equal)
                j_star = J_i[i][np.argmin(c[i, J_i[i]])]

                solution_path += f"\nWe can assign {i+1} to no opened facility, so we open a facility at location {j_star+1}."
                X.append(j_star)

        # Every customer is assigned to its cheapest opened facility
        Assignment = []
        for i in I:
            Assignment.append(X[np.argmin(c[i, X])])

        solution_path += f"\nWe open the facilities {[j+1 for j in X]} and have the following assignment vector: {[Assignment[i] + 1 for i in I]}."

        return X, Assignment, J_plus, solution_path

    def dual_adjust(self, v, s, X, J_plus, solution_path):
        """
        Tries to raise the sum of the v-values: a customer i that pays more than its cost at two or
        more opened facilities lowers v[i] by one level, then the dual ascent is repeated.
        v and s are changed and returned.
        """
        n = self.n
        m = self.m
        I = [i for i in range(n)]
        c = self.c

        for i in I:
            # J_i = opened facilities at which customer i pays more than its cost (v[i] > c[i, j])
            J_i = [j for j in X if v[i] > c[i, j]]

            if len(J_i) <= 1:
                solution_path += f"\nFor i = {i+1} we have J_{i+1} = {[j+1 for j in J_i]}; since the cardinality is not larger than 1, we go to the next i."
                continue

            # j* = cheapest facility in J_i, j** = second cheapest
            j_star = J_i[np.argmin(c[i, J_i])]

            J_i_without_jstar = J_i.copy()
            J_i_without_jstar.remove(j_star)
            j_starstar = J_i_without_jstar[np.argmin(c[i, J_i_without_jstar])]

            # I_j* (I_j**) = customers k whose only facility in J+ with c[k, j] <= v[k] is j* (j**)
            I_j_star = []
            I_j_star_star = []
            for k in I:
                k_test = [j for j in J_plus if v[k] >= c[k, j]]
                if len(k_test) == 1:
                    if k_test[0] == j_star:
                        I_j_star.append(k)
                    if k_test[0] == j_starstar:
                        I_j_star_star.append(k)

            solution_path += f"\nFor i = {i+1} we get J_{i+1} = {[j+1 for j in J_i]}, j* = {j_star+1}, j** = {j_starstar+1}, I_j* = {[k+1 for k in I_j_star]}, I_j** = {[k+1 for k in I_j_star_star]}."

            if len(I_j_star_star) == 0 and len(I_j_star) == 0:
                solution_path += f"\nSince I_j* and I_j** are empty, we go to the next i."
                continue

            # Lower v[i] to the next smaller level delta = largest c[i, j] below v[i]. Every facility
            # j with c[i, j] < v[i] gets back the difference v[i] - delta as slack.
            delta = clean(max([c[i, j] for j in range(m) if v[i] > c[i, j]]))
            for j in range(m):
                if v[i] > c[i, j]:
                    s[j] = clean(s[j] + v[i] - delta)
            v[i] = delta

            I_first = I_j_star.copy()
            for k in I_j_star_star:
                I_first.append(k)

            solution_path += f"\nWe get delta = {delta}, so the new s-vector is {s}; set v_{i+1} to {delta} and perform dual ascent with I = {[k+1 for k in I_first]}."
            v, s, solution_path = self.dual_ascent(v, s, I_first, solution_path)
            if i not in I_first:
                I_first.append(i)
                solution_path += f"\nNext, we perform dual ascent with I = {[k+1 for k in I_first]}."
                v, s, solution_path = self.dual_ascent(v, s, I_first, solution_path)
            solution_path += f"\nLast, we perform dual ascent with I = {[k+1 for k in I]}."
            v, s, solution_path = self.dual_ascent(v, s, I, solution_path)
            solution_path += f"\nDual adjust completed, we get the v-values {v} and s-values {s}."
        return v, s, solution_path