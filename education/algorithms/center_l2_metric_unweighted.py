import numpy as np
from common.additional_methods import AdditionalMethods

class center_l2_metric_unweighted:
    """
    Unweighted center with Euclidean distances (l2 metric): the smallest circle that covers all customers.

    Minimises f(x) = max_k ||x - a_k||_2; the optimal point (the midpoint of the circle) is unique. The
    smallest circle is determined by two customers (as its diameter) or by three customers (as the
    circumcircle of an acute triangle). Up to four customers it is calculated directly. For more customers
    the Elzinga-Hearn algorithm starts with the circle of two customers and, as long as a customer lies
    outside, calculates the smallest circle of this customer and the customers that define the current
    circle (step 3: two of them, step 6: three).

    :param coordinates: the customers as lists [x1, x2, ...]; only the first two entries are used
    """

    def __init__(self, coordinates):
        # Use only the first two elements (x and y) from each point.
        numeric_coords = [point[:2] for point in coordinates]
        self.coordinates = np.array(numeric_coords, dtype=float)
        self.x_coords = self.coordinates[:, 0]
        self.y_coords = self.coordinates[:, 1]
        self.solution_path = ""


    def run(self):
        """
        Runs the algorithm.

        :return: ([0, p] with the optimal point p = (x1, x2), result text, solution path, None)
        """
        number_points = len(self.coordinates)

        # Up to four points: smallest circle directly
        if number_points == 1:
            self.solution_path = f"Since we have only one point, the center is at that point."
            mid_point, solution_value = (self.x_coords[0], self.y_coords[0]), 0
        elif number_points == 2:
            self.solution_path = f"Since we have only two points, we only determine the circumcircle for these two points."
            mid_point, solution_value = self._two_point_calculation(0, 1)
            self.solution_path += f"\nMidpoint is ({mid_point[0]:.4f}, {mid_point[1]:.4f}) and the radius is {solution_value:.4f}."
        elif number_points == 3:
            self.solution_path = f"Since we have only three points, we only determine the circumcircle for these three points."
            mid_point, solution_value, _ = self._three_point_calculation(0, 1, 2)
        elif number_points == 4:
            self.solution_path = f"Since we have only four points, we only determine the circumcircle for these four points via enumeration."
            mid_point, solution_value, _ = self._four_point_calculation(0, 1, 2, 3)

        # Using Elzinga Hearn for more than four points
        else:
            self.solution_path = f"Since we have more than four points, we use the Elzinga and Hearn algorithm."
            _points = [i for i in range(number_points)]
            current_points = []
            # Start with the smallest circle of the first two points
            self.solution_path += f"\nDetermining the circumcircle of the first two points ({self.coordinates[0][0]:.4f}, {self.coordinates[0][1]:.4f}) and ({self.coordinates[1][0]:.4f}, {self.coordinates[1][1]:.4f})."
            mid_point, solution_value = self._two_point_calculation(0, 1)
            self.solution_path += f"\nMidpoint is ({mid_point[0]:.4f}, {mid_point[1]:.4f}) and the radius is {solution_value:.4f}."
            current_points.append(0)
            current_points.append(1)
            # Points that this circle does not cover
            check_points = [i for i in _points if i not in current_points]
            for i in check_points.copy():
                other_distance = AdditionalMethods.distance_calculation_lp(mid_point, i, self.coordinates, 2, 2)
                if solution_value >= other_distance or np.isclose(solution_value, other_distance):
                    self.solution_path += f"\nThe point ({self.coordinates[i][0]:.4f}, {self.coordinates[i][1]:.4f}) is also covered by the circumcircle; indices of open points: {', '.join(str(x+1) for x in check_points)}."
                    check_points.remove(i)
            # As long as a point is not covered: step 3 if the circle is defined by two points, step 6 if by three;
            # 9 = stop
            if (len(check_points) >= 1):
                next_step = 3
                next_point = check_points[0]
                while(next_step != 9):
                    if next_step == 3:
                        mid_point, solution_value, current_points, next_point, next_step = self._step3(current_points, _points, next_point)
                    elif next_step == 6:
                        mid_point, solution_value, current_points, next_point, next_step = self._step6(current_points, _points, next_point)
            else:
                self.solution_path += f"\nAll points are covered by the circumcircle."

        result_string = f"Optimal point: ({mid_point[0]:.4f} | {mid_point[1]:.4f})\nObjective function value: {solution_value:.4f}"
        optimal_point = [0, (mid_point[0], mid_point[1])]
        
        # Return a list of optimal points, the result string, and the solution path.
        return optimal_point, result_string, self.solution_path, None



    def _two_point_calculation(self, point1, point2):
        """
        Smallest circle that covers two points: the midpoint of the line segment, half of its length as radius.

        :param point1: index of the first point
        :param point2: index of the second point
        :return: (midpoint [x1, x2], radius)
        """
        middle_point = [(self.coordinates[point1][0] + self.coordinates[point2][0])/2, (self.coordinates[point1][1] + self.coordinates[point2][1])/2]
        radius = AdditionalMethods.distance_calculation_lp(middle_point, point1, self.coordinates, 2, 2)
        return middle_point, radius

    def _three_point_calculation(self, point1, point2, point3):
        """
        Smallest circle that covers three points. If the circle with the longest side of the triangle as
        diameter covers the third point (right or obtuse triangle), it is this circle; otherwise (acute
        triangle) it is the circumcircle.

        :param point1: index of the first point
        :param point2: index of the second point
        :param point3: index of the third point
        :return: (midpoint [x1, x2], radius, indices of the two or three points that define the circle)
        """
        self.solution_path += f"\nDetermining the circumcircle of points ({self.coordinates[point1][0]:.4f}, {self.coordinates[point1][1]:.4f}), ({self.coordinates[point2][0]:.4f}, {self.coordinates[point2][1]:.4f}) and ({self.coordinates[point3][0]:.4f}, {self.coordinates[point3][1]:.4f})."
        distance12 = AdditionalMethods.distance_calculation_lp(point1, point2, self.coordinates, 2, 2)
        distance13 = AdditionalMethods.distance_calculation_lp(point1, point3, self.coordinates, 2, 2)
        distance23 = AdditionalMethods.distance_calculation_lp(point2, point3, self.coordinates, 2, 2)

        # Sort the points so that (p1, p2) is the longest side of the triangle
        if(distance12 > distance13 and distance12 > distance23):
            p1, p2, p3 = point1, point2, point3
        elif(distance13 > distance23):
            p1, p2, p3 = point1, point3, point2
        else:
            p1, p2, p3 = point2, point3, point1

        # Circle with the longest side as diameter; if it covers the third point, it is the smallest circle
        middle_point, radius = self._two_point_calculation(p1, p2)
        other_distance = AdditionalMethods.distance_calculation_lp(middle_point, p3, self.coordinates, 2, 2)
        if radius >= other_distance or np.isclose(radius, other_distance):
            self.solution_path += f"\nSince the points form an obtuse triangle, we determine the circumcircle of the points ({self.coordinates[p1][0]:.4f}, {self.coordinates[p1][1]:.4f}) and ({self.coordinates[p2][0]:.4f}, {self.coordinates[p2][1]:.4f})."
            self.solution_path += f"\nMidpoint is ({middle_point[0]:.4f}, {middle_point[1]:.4f}) and the radius is {radius:.4f}."
            return middle_point, radius, [p1, p2]

        # Acute triangle: circumcircle, whose midpoint is the intersection of two perpendicular bisectors (pairs
        # with equal x2 coordinates are avoided, their bisector is vertical)
        if (self.coordinates[point2][1] != self.coordinates[point1][1]):
            m12, b12 = self._bisector(point1, point2)
        else:
            m12, b12 = self._bisector(point2, point3)
        if (self.coordinates[point3][1] != self.coordinates[point1][1]):
            m13, b13 = self._bisector(point1, point3)
        else:
            m13, b13 = self._bisector(point2, point3)
        self.solution_path += f"\nThe points form an acute triangle. We get the perpendicular bisectors with the parameters m1={m12:.4f}, b1={b12:.4f}, m2={m13:.4f}, b2={b13:.4f}."
        # Intersection of the lines x2 = m12 * x1 + b12 and x2 = m13 * x1 + b13
        middle_point = [(b13-b12) / (m12-m13), (m12*b13-b12*m13) / (m12-m13)]
        radius = AdditionalMethods.distance_calculation_lp(point1, middle_point, self.coordinates, 2, 2)
        self.solution_path += f"\nMidpoint is ({middle_point[0]:.4f}, {middle_point[1]:.4f}) and the radius is {radius:.4f}."
        return middle_point, radius, [point1, point2, point3]

    def _four_point_calculation(self, point1, point2, point3, point4):
        """
        Smallest circle that covers four points, by enumeration: it is the smallest circle of one of the four
        triples, and every triple whose smallest circle also covers the fourth point gives it.

        :param point1: index of the first point
        :param point2: index of the second point
        :param point3: index of the third point
        :param point4: index of the fourth point
        :return: (midpoint [x1, x2], radius, indices of the two or three points that define the circle)
        """
        self.solution_path += f"\nWe determine the circumcircle of the four points ({self.coordinates[point1][0]:.4f}, {self.coordinates[point1][1]:.4f}), ({self.coordinates[point2][0]:.4f}, {self.coordinates[point2][1]:.4f}), ({self.coordinates[point3][0]:.4f}, {self.coordinates[point3][1]:.4f}) and ({self.coordinates[point4][0]:.4f}, {self.coordinates[point4][1]:.4f}) via enumeration."
        
        # Try the triples until the smallest circle of one of them also covers the fourth point
        for p in [(point1, point2, point3, point4), (point1, point2, point4, point3), (point1, point3, point4, point2), (point2, point3, point4, point1)]:
            middle_point, radius, defining_points = self._three_point_calculation(p[0], p[1], p[2])
            other_distance = AdditionalMethods.distance_calculation_lp(middle_point, p[3], self.coordinates, 2, 2)
            if radius >= other_distance or np.isclose(radius, other_distance):
                if len(defining_points)== 2:
                    self.solution_path += f"\nThe circumcircle of the four points is determined by the two points ({self.coordinates[defining_points[0]][0]:.4f}, {self.coordinates[defining_points[0]][1]:.4f}) and ({self.coordinates[defining_points[1]][0]:.4f}, {self.coordinates[defining_points[1]][1]:.4f})."
                else:
                    self.solution_path += f"\nThe circumcircle of the four points is determined by the three points ({self.coordinates[defining_points[0]][0]:.4f}, {self.coordinates[defining_points[0]][1]:.4f}), ({self.coordinates[defining_points[1]][0]:.4f}, {self.coordinates[defining_points[1]][1]:.4f}) and ({self.coordinates[defining_points[2]][0]:.4f}, {self.coordinates[defining_points[2]][1]:.4f})."
                self.solution_path += f"\nMidpoint is ({middle_point[0]:.4f}, {middle_point[1]:.4f}) and the radius is {radius:.4f}."
                return middle_point, radius, defining_points
        
    
    def _step3(self, points, all_points, other_point):
        """
        Step 3 of the Elzinga-Hearn algorithm: the current circle is defined by two points and other_point is
        not covered, so the smallest circle of these three points is calculated.

        :param points: indices of the two points that define the current circle
        :param all_points: indices of all points
        :param other_point: index of a point that is not covered
        :return: (midpoint, radius, indices of the points that define the new circle, a point that is still
                 not covered (np.nan if there is none), next step: 3, 6 or 9 = stop)
        """
        # Calculation circumcircle of the three points
        self.solution_path += f"\nStep 3: Choose the non-covered point ({self.coordinates[other_point][0]:.4f}, {self.coordinates[other_point][1]:.4f}) and determine the circumcircle for three points."
        middle_point, radius, defining_points= self._three_point_calculation(points[0], points[1], other_point)
        open_points, next_step = self._cover_and_next_step(all_points, points, middle_point, defining_points, other_point, radius)
        return middle_point, radius, defining_points, open_points, next_step

    def _step6(self, points, all_points, other_point):
        """
        Step 6 of the Elzinga-Hearn algorithm: the current circle is defined by three points and other_point
        is not covered, so the smallest circle of these four points is calculated.

        :param points: indices of the three points that define the current circle
        :param all_points: indices of all points
        :param other_point: index of a point that is not covered
        :return: (midpoint, radius, indices of the points that define the new circle, a point that is still
                 not covered (np.nan if there is none), next step: 3, 6 or 9 = stop)
        """
        # Calculation circumcircle of the four points
        self.solution_path += f"\nStep 6: Choose the non-covered point ({self.coordinates[other_point][0]:.4f}, {self.coordinates[other_point][1]:.4f}) and determine the circumcircle for four points."
        middle_point, radius, defining_points = self._four_point_calculation(points[0], points[1], points[2], other_point)
        open_points, next_step = self._cover_and_next_step(all_points, points, middle_point, defining_points, other_point, radius)
        return middle_point, radius, defining_points, open_points, next_step

    def _bisector(self, p, q):
        """
        Perpendicular bisector of the points p and q as the line x2 = m * x1 + b (p and q must have different
        x2 coordinates, otherwise the bisector is vertical).

        :return: (m, b)
        """
        m = (self.coordinates[p][0] - self.coordinates[q][0]) / (self.coordinates[q][1] - self.coordinates[p][1])
        b = (pow(self.coordinates[q][0],2) + pow(self.coordinates[q][1],2) - pow(self.coordinates[p][0],2) - pow(self.coordinates[p][1],2)) / (2*(self.coordinates[q][1] - self.coordinates[p][1]))
        return m, b

    def _cover_and_next_step(self, all_points, points, middle_point, defining_points, other_point, radius):
        """
        Checks which points the new circle covers and chooses the next step: 9 (stop) if all points are
        covered, otherwise step 3 (circle defined by two points) or step 6 (by three points) with the first
        point that is not covered.

        :return: (first point that is not covered or np.nan, next step)
        """
        open_points = [i for i in all_points if i not in points]
        open_points.remove(other_point)
        self.solution_path += f"\nThe point ({self.coordinates[other_point][0]:.4f}, {self.coordinates[other_point][1]:.4f}) is now covered by the circumcircle; indices of open points: {', '.join(str(x+1) for x in open_points)}."
        # Check which points are covered
        for i in open_points.copy():
            other_distance = AdditionalMethods.distance_calculation_lp(middle_point, i, self.coordinates, 2, 2)
            if radius >= other_distance or np.isclose(radius, other_distance):
                self.solution_path += f"\nThe point ({self.coordinates[i][0]:.4f}, {self.coordinates[i][1]:.4f}) is covered by the circumcircle; indices of open points: {', '.join(str(x+1) for x in open_points)}."
                open_points.remove(i)
        # If all points are covered, go to step 9, otherwise to step 3 or 6
        if(len(open_points) == 0):
            return np.nan, 9
        else:
            if(len(defining_points) == 2):
                self.solution_path += f"\nThe circumcircle is determined by two points and not all points are covered. Go to step 3."
                return open_points[0], 3
            else:
                self.solution_path += f"\nThe circumcircle is determined by three points and not all points are covered. Go to step 6."
                return open_points[0], 6