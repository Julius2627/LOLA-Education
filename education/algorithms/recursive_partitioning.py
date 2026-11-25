import math


def convex_hull(points):
    """
    The convex hull of points in the plane (Andrew's monotone chain).

    :param points: [(x, y), ...]
    :return: the corners of the hull counter-clockwise, without points on its edges; one corner if all points are
             equal, two if they lie on one line
    """
    corners = sorted(set(points))
    if len(corners) <= 2:
        return corners

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for point in corners:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(corners):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def number(value):
    """A number for the texts: at most 4 decimals, without trailing zeros, a minus sign (12.5, 50, 0.04, −4.2286)."""
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text.replace("-", "−")


def area_set(areas):
    """A set of basic areas for the texts: {1, 3, 5}."""
    return "{" + ", ".join(str(i) for i in sorted(areas)) + "}"


class recursive_partitioning:
    """
    Recursive Partitioning for districting (Kalcsics, Nickel, Schröder 2005; the lecture's basic form).

    Districting: the basic areas V (points (x, y) with an activity w >= 0) are grouped into p districts that are
    balanced (activity w(D) close to mu = W(V)/p), compact and contiguous.

    The algorithm divides partition problems PP = (B, q) (the areas B form q districts) by lines, starting with
    (V, p), until every problem is trivial (q = 1: B is a district). A line partition LP = (B_l, B_r, q_l, q_r)
    divides B by a line L into B_l = B ∩ H≤(L) and B_r = B ∩ H>(L) with q_l + q_r = q: q_l = q_r = q/2 if q is
    even; if q is odd, both (q-1)/2, (q+1)/2 and (q+1)/2, (q-1)/2 are tried.

    K line directions theta = 0, pi/K, ..., (K-1)pi/K (K = 2: horizontal and vertical lines). For a direction the
    areas are sorted by x' = x sin(theta) - y cos(theta) (the line becomes vertical); B_l is the first k areas
    and the line goes through the last of them. Only positions with q_l <= k <= |B| - q_r where the next area has
    a larger x' are possible (a line cannot separate areas with the same x'). Best balanced position k*: k' is
    the last possible k with W(B_l)/q_l < W(B)/q, the next possible one has W(B_l)/q_l >= W(B)/q; k* = k' if
    W(B)/q - W(B_l^k')/q_l <= W(B_l^next)/q_l - W(B)/q, otherwise the next one.

    Every direction (and split) gives its best balanced line partition; they are ranked by
        rk(LP) = beta bal(LP)/bal_max + (1 - beta) cp(LP)/cp_max
    with the balance bal(LP) = max(|W(B_l)/q_l - mu|, |W(B_r)/q_r - mu|)/mu and the compactness cp(LP): the length
    of the line inside the convex hull of B (from c1 to c2); bal_max and cp_max are the largest values of the
    candidates (a term is 0 if its largest value is 0). The candidate with the smallest rk is realised (ties: the
    first direction, then the split with the smaller q_l). Unsolved problems are taken depth first, the left one
    first, so the districts D1, ..., Dp are numbered from left to right in the partitioning tree.

    The districts' convex hulls do not overlap (contiguity). Without a backtracking step (basic form), the
    algorithm stops if a problem cannot be divided in any direction (areas at the same place).

    :param areas: [(x, y, w), ...] the basic areas 1, ..., n
    :param p: the number of districts (1 <= p <= n)
    :param K: the number of line directions (>= 1)
    :param beta: the weight of the balance against the compactness (0 <= beta <= 1)
    """

    def __init__(self, areas, p, K=2, beta=0.5):
        self.areas = [(float(x), float(y), float(w)) for x, y, w in areas]
        self.p, self.K, self.beta = p, K, beta
        self.n = len(self.areas)
        scale = max([1.0] + [abs(value) for x, y, _ in self.areas for value in (x, y)])
        self.tol = 1e-9 * scale      # x' values closer than this count as equal (the same line)
        self.steps = []              # the partition problems in the order they are solved

    # ------------------------------------------------------------------ the parts of the algorithm

    def direction(self, k):
        """Direction k (0, ..., K-1): (theta in degrees, sin theta, cos theta); exact at multiples of 90 degrees."""
        theta = k * math.pi / self.K
        s, c = math.sin(theta), math.cos(theta)
        s, c = (round(s) if abs(s - round(s)) < 1e-12 else s), (round(c) if abs(c - round(c)) < 1e-12 else c)
        return k * 180 / self.K, s, c

    def rotated(self, i, s, c):
        """x' of area i (0-based) for the direction with sin theta = s, cos theta = c."""
        x, y, _ = self.areas[i]
        return x * s - y * c

    def best_balanced(self, B, q, q_l, q_r, s, c):
        """
        The best balanced line partition of (B, q) with q_l, q_r in one direction.

        :return: dict with the order of B, the x' values, the positions not possible (same x'), k* and the
                 comparison k' / next (for the solution path), B_l, B_r, the line (x' = value) and its weights; None
                 if no position is possible
        """
        x_rot = {i: self.rotated(i, s, c) for i in B}
        order = sorted(B, key=lambda i: (x_rot[i], i))
        cumulative = [0.0]
        for i in order:
            cumulative.append(cumulative[-1] + self.areas[i][2])
        W, target = cumulative[-1], cumulative[-1] / q
        possible = [k for k in range(q_l, len(B) - q_r + 1) if x_rot[order[k]] - x_rot[order[k - 1]] > self.tol]
        excluded = [k for k in range(q_l, len(B) - q_r + 1) if k not in possible]
        if not possible:
            return None
        below = [k for k in possible if cumulative[k] / q_l < target]
        above = [k for k in possible if cumulative[k] / q_l >= target]
        k_below, k_above = (below[-1] if below else None), (above[0] if above else None)
        if k_below is None:
            k_star = k_above
        elif k_above is None:
            k_star = k_below
        else:
            gap_below = target - cumulative[k_below] / q_l
            gap_above = cumulative[k_above] / q_l - target
            k_star = k_below if gap_below <= gap_above + 1e-9 * max(1.0, target) else k_above
        return {"order": order, "x_rot": x_rot, "cumulative": cumulative, "target": target, "excluded": excluded,
                "k_below": k_below, "k_above": k_above, "k": k_star,
                "left": order[:k_star], "right": order[k_star:], "value": x_rot[order[k_star - 1]],
                "through": order[k_star - 1], "W_l": cumulative[k_star], "W_r": W - cumulative[k_star]}

    def chord(self, B, s, c, value):
        """
        The part of the line x s - y c = value inside the convex hull of the areas B: its ends c1, c2 (c1 the left
        one; on a vertical line the upper one) and its length.
        """
        hull = convex_hull([self.areas[i][:2] for i in B])
        f = lambda point: point[0] * s - point[1] * c - value
        ends = [corner for corner in hull if abs(f(corner)) <= self.tol]
        for a, b in zip(hull, hull[1:] + hull[:1]):
            fa, fb = f(a), f(b)
            if (fa < -self.tol and fb > self.tol) or (fa > self.tol and fb < -self.tol):
                t = fa / (fa - fb)
                ends.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        along = lambda point: point[0] * c + point[1] * s       # position along the line
        e1, e2 = min(ends, key=along), max(ends, key=along)
        if abs(e1[0] - e2[0]) <= self.tol:
            c1, c2 = (e1, e2) if e1[1] >= e2[1] else (e2, e1)
        else:
            c1, c2 = (e1, e2) if e1[0] < e2[0] else (e2, e1)
        length = math.dist(c1, c2)
        return c1, c2, (length if length > self.tol else 0.0)     # rounding noise: 0 (the line touches the hull)

    # ------------------------------------------------------------------ the algorithm

    def run(self):
        """
        Runs Recursive Partitioning.

        :return: (result, result text, solution path, None); result: {"districts": [[areas of D1 (1-based)], ...],
                 "activity": [w(D1), ...], "balance": [bal(D1), ...], "lines": [(c1, c2) of L1, ...],
                 "hulls": [[corners of the convex hull of D1], ...]}, or None if there is no result
        """
        n, p, K, beta = self.n, self.p, self.K, self.beta
        if n == 0 or not isinstance(p, int) or not 1 <= p <= n:
            return None, "No result: the number of districts p must be between 1 and the number of basic areas.", "", None
        if not isinstance(K, int) or K < 1 or not 0 <= beta <= 1:
            return None, "No result: K must be at least 1 and beta between 0 and 1.", "", None
        if any(w < 0 for _, _, w in self.areas) or sum(w for _, _, w in self.areas) <= 0:
            return None, "No result: the activities must not be negative, and their sum must be positive.", "", None
        W_V = sum(w for _, _, w in self.areas)
        mu = W_V / p
        directions = [self.direction(k) for k in range(K)]

        path = [f"Recursive Partitioning: p = {p} districts, K = {K} line directions, β = {number(beta)}",
                f"W(V) = {number(W_V)}, μ = W(V)/p = {number(mu)}",
                "Line directions θ: " + ", ".join(self.direction_name(d) for d in directions),
                "A line in direction θ is vertical after rotating the coordinates to x' = x·sin θ − y·cos θ; "
                "B_l: the areas up to the line (x' ≤ the line), B_r: the others."]
        districts, lines = [], []
        unsolved = [("PP", list(range(n)), p)]        # depth first, the left problem first
        while unsolved:
            name, B, q = unsolved.pop()
            if q == 1:
                districts.append(B)
                self.steps.append({"name": name, "areas": sorted(i + 1 for i in B), "q": 1, "district": len(districts)})
                path.append(f"\n{name} = ({self.areas_text(B)}, 1) is trivial ⇒ district D{len(districts)} = "
                            f"{self.areas_text(B)}")
                continue
            W_B = sum(self.areas[i][2] for i in B)
            splits = [(q // 2, q // 2)] if q % 2 == 0 else [((q - 1) // 2, (q + 1) // 2), ((q + 1) // 2, (q - 1) // 2)]
            path.append(f"\n{name} = (B, q) with B = {self.areas_text(B)}, q = {q}: W(B) = {number(W_B)}, "
                        f"W(B)/q = {number(W_B / q)}")
            path.append(f"q even: q_l = q_r = {q // 2}" if q % 2 == 0 else
                        f"q odd: (q_l, q_r) = ({(q - 1) // 2}, {(q + 1) // 2}) and ({(q + 1) // 2}, {(q - 1) // 2})")
            candidates = []
            for theta, s, c in directions:
                path.append(f"  θ = {self.direction_name((theta, s, c))}: x' = {self.rotation_text(s, c)}; order by x': "
                            + ", ".join(f"{i + 1} ({number(self.rotated(i, s, c))})"
                                        for i in sorted(B, key=lambda i: (self.rotated(i, s, c), i))))
                for q_l, q_r in splits:
                    head = "    " if len(splits) == 1 else f"    (q_l, q_r) = ({q_l}, {q_r}): "
                    found = self.best_balanced(B, q, q_l, q_r, s, c)
                    if found is None:
                        path.append(head + "no line partition (the areas cannot be divided with q_l areas or more "
                                           "left and q_r areas or more right)")
                        continue
                    c1, c2, cp = self.chord(B, s, c, found["value"])
                    bal = max(abs(found["W_l"] / q_l - mu), abs(found["W_r"] / q_r - mu)) / mu
                    bal = bal if bal > 1e-12 else 0.0       # rounding noise: 0
                    candidate = dict(found, theta=theta, s=s, c=c, q_l=q_l, q_r=q_r, c1=c1, c2=c2, cp=cp, bal=bal)
                    candidates.append(candidate)
                    path.append(head + self.position_text(found, q_l))
                    path.append(f"    line {self.line_text(s, c, found['value'])} through area {found['through'] + 1}: "
                                f"B_l = {self.areas_text(found['left'])}, B_r = {self.areas_text(found['right'])}")
                    path.append(f"    bal = max(|{number(found['W_l'])}/{q_l} − {number(mu)}|, "
                                f"|{number(found['W_r'])}/{q_r} − {number(mu)}|)/{number(mu)} = {number(bal)}; "
                                f"c1 = {self.point_text(c1)}, c2 = {self.point_text(c2)}: cp = {number(cp)}")
            if not candidates:
                path.append(f"No direction gives a line partition of {name} (its areas lie at the same place in every "
                            "direction). The basic form of Recursive Partitioning stops here (no backtracking).")
                self.steps.append({"name": name, "areas": sorted(i + 1 for i in B), "q": q, "candidates": []})
                return (None, f"No result: {name} = ({self.areas_text(B)}, {q}) cannot be divided by a line.",
                        "\n".join(path), None)
            bal_max = max(candidate["bal"] for candidate in candidates)
            cp_max = max(candidate["cp"] for candidate in candidates)
            path.append(f"  bal_max = {number(bal_max)}, cp_max = {number(cp_max)}; "
                        "rk = β·bal/bal_max + (1 − β)·cp/cp_max:")
            best = None
            for index, candidate in enumerate(candidates):
                term_bal = candidate["bal"] / bal_max if bal_max > 0 else 0.0
                term_cp = candidate["cp"] / cp_max if cp_max > 0 else 0.0
                candidate["rk"] = beta * term_bal + (1 - beta) * term_cp
                if best is None or candidate["rk"] < candidates[best]["rk"] - 1e-12:
                    best = index
                path.append(f"    {self.candidate_name(candidate, splits)}: rk = {number(beta)}·{number(candidate['bal'])}/"
                            f"{number(bal_max)} + {number(1 - beta)}·{number(candidate['cp'])}/{number(cp_max)} = "
                            f"{number(candidate['rk'])}" if bal_max > 0 and cp_max > 0 else
                            f"    {self.candidate_name(candidate, splits)}: rk = {number(candidate['rk'])}"
                            " (a term whose largest value is 0 counts 0)")
            chosen = candidates[best]
            lines.append((chosen["c1"], chosen["c2"]))
            self.steps.append({"name": name, "areas": sorted(i + 1 for i in B), "q": q, "chosen": best,
                               "line": len(lines), "candidates": [
                                   {key: candidate[key] for key in ("theta", "q_l", "q_r", "k", "bal", "cp", "rk",
                                                                    "c1", "c2", "value")}
                                   | {"left": sorted(i + 1 for i in candidate["left"]),
                                      "right": sorted(i + 1 for i in candidate["right"])}
                                   for candidate in candidates]})
            left, right = chosen["left"], chosen["right"]
            name_l, name_r = (name + "l", name + "r") if name != "PP" else ("PP_l", "PP_r")
            path.append(f"  ⇒ realise {self.candidate_name(chosen, splits)} (smallest rk): line L{len(lines)}: "
                        f"{self.line_text(chosen['s'], chosen['c'], chosen['value'])}; new partition problems "
                        f"{name_l} = ({self.areas_text(left)}, {chosen['q_l']}) and "
                        f"{name_r} = ({self.areas_text(right)}, {chosen['q_r']})")
            unsolved.append((name_r, right, chosen["q_r"]))
            unsolved.append((name_l, left, chosen["q_l"]))

        activity = [sum(self.areas[i][2] for i in D) for D in districts]
        balance = [abs(w - mu) / mu for w in activity]
        result = {"districts": [sorted(i + 1 for i in D) for D in districts], "activity": activity,
                  "balance": balance, "lines": lines,
                  "hulls": [convex_hull([self.areas[i][:2] for i in D]) for D in districts]}
        path.append(f"\nDistrict layout DL (bal(D) = |w(D) − μ|/μ with μ = {number(mu)}):")
        path += [f"D{j + 1} = {self.areas_text(D)}: w(D{j + 1}) = {number(activity[j])}, "
                 f"bal(D{j + 1}) = {number(balance[j])}" for j, D in enumerate(districts)]
        text = [f"Recursive Partitioning: {p} districts (K = {K}, β = {number(beta)})"]
        text += [f"D{j + 1} = {self.areas_text(D)}: w = {number(activity[j])}, bal = {number(balance[j])}"
                 for j, D in enumerate(districts)]
        text.append(f"Largest deviation: max bal(D) = {number(max(balance))}")
        return result, "\n".join(text), "\n".join(path), None

    # ------------------------------------------------------------------ texts

    @staticmethod
    def areas_text(B):
        """Areas given 0-based, shown 1-based: {1, 3, 5}."""
        return area_set(i + 1 for i in B)

    @staticmethod
    def point_text(point):
        return f"({number(point[0])}, {number(point[1])})"

    @staticmethod
    def direction_name(direction):
        theta = direction[0]
        kind = {0: " (horizontal lines)", 90: " (vertical lines)"}.get(theta, "")
        return f"{number(theta)}°{kind}"

    @staticmethod
    def rotation_text(s, c):
        """x' = x sin(theta) - y cos(theta) with the numbers of the direction."""
        terms = []
        for factor, symbol in ((s, "x"), (-c, "y")):
            if factor == 0:
                continue
            sign = "−" if factor < 0 else "+"
            size = "" if abs(factor) == 1 else f"{number(abs(factor))}·"
            terms.append((sign, size + symbol))
        first_sign, first = terms[0]
        return ("−" if first_sign == "−" else "") + first + "".join(f" {sign} {term}" for sign, term in terms[1:])

    @staticmethod
    def line_text(s, c, value):
        """The line x s - y c = value as an equation: y = ..., x = ... or y = m·x + b."""
        if c == 0:
            return f"x = {number(value / s)}"
        if s == 0:
            return f"y = {number(-value / c)}"
        slope, offset = s / c, -value / c
        term = {"1": "x", "−1": "−x"}.get(number(slope), f"{number(slope)}·x")
        return f"y = {term} {'−' if offset < 0 else '+'} {number(abs(offset))}"

    def position_text(self, found, q_l):
        """How k* follows from k' and the next possible position."""
        cumulative, target, k_below, k_above, k = (found[key] for key in
                                                   ("cumulative", "target", "k_below", "k_above", "k"))
        value = lambda position: number(cumulative[position] / q_l)
        order, excluded = found["order"], found["excluded"]
        note = "".join(f" (k = {position} is not possible: areas {order[position - 1] + 1} and {order[position] + 1} "
                       "have the same x')" for position in excluded)
        if k_below is None:
            return (f"every possible B_l has W(B_l)/q_l ≥ W(B)/q = {number(target)}; the smallest possible: "
                    f"k* = {k} (W(B_l)/q_l = {value(k)})" + note)
        if k_above is None:
            return (f"every possible B_l has W(B_l)/q_l < W(B)/q = {number(target)}; the largest possible: "
                    f"k* = {k} (W(B_l)/q_l = {value(k)})" + note)
        gap_below = target - cumulative[k_below] / q_l
        gap_above = cumulative[k_above] / q_l - target
        relation = "≤" if k == k_below else ">"
        return (f"k' = {k_below}: W(B_l)/q_l = {value(k_below)} < {number(target)}; next possible k = {k_above}: "
                f"{value(k_above)} ≥ {number(target)}; {number(gap_below)} {relation} {number(gap_above)} ⇒ k* = {k}"
                + note)

    def candidate_name(self, candidate, splits):
        name = f"θ = {number(candidate['theta'])}°"
        return name if len(splits) == 1 else name + f", (q_l, q_r) = ({candidate['q_l']}, {candidate['q_r']})"
