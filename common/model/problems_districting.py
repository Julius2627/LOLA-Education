class DistrictingProblemRepository:
    """Provides predefined districting problems: the basic areas (points with an activity) and the parameters.
    A new problem can be added in the following format:
    '<Name>': {
                'areas': [(x, y, w), ...],   # one basic area per entry: its position and its activity w >= 0
                'p': 4,                      # the number of districts
                'K': 2,                      # the number of line directions (Recursive Partitioning)
                'beta': 0.5,                 # the weight of the balance against the compactness (Recursive Partitioning)
                'names': ['A', ...]          # optional: the names of the basic areas
            },
    The basic areas are numbered 1, 2, ... in the order of the list. Names starting with "Fac. Loc." or "Further"
    are shown in the Education Mode (see EDUCATION_PREFIXES in datapoints.py) and on the coordinate system page of the
    Applied Mode; the others are given in latitude and longitude and shown on the map page of the Applied Mode."""

    @staticmethod
    def get_predefined_problems():
        return {
            # The example of the lecture (chapter 6, Recursive Partitioning): 4 districts, horizontal and vertical lines
            'Fac. Loc. Lecture Example': {
                'areas': [(0.5, 5.0, 4), (1.0, 2.0, 2), (2.0, 4.0, 4), (2.5, 1.0, 3), (3.0, 3.5, 5),
                          (3.5, 2.5, 7), (4.0, 5.5, 6), (4.5, 3.0, 5), (5.0, 1.5, 6), (5.0, 5.0, 8)],
                'p': 4, 'K': 2, 'beta': 0.5
            },
            # 24 basic areas, 6 districts, 4 line directions (also diagonal lines)
            'Further Example: 24 Areas': {
                'areas': [(1.0, 1.8, 8), (1.1, 6.5, 7), (1.2, 4.0, 9), (1.2, 4.1, 5), (2.1, 2.0, 7), (2.4, 4.9, 10),
                          (2.9, 3.7, 8), (3.4, 4.5, 9), (4.2, 3.2, 9), (4.5, 6.5, 1), (5.1, 0.6, 10), (5.1, 6.9, 4),
                          (5.8, 0.2, 3), (5.9, 4.0, 1), (6.0, 4.5, 12), (6.9, 5.4, 9), (7.1, 2.9, 11), (7.3, 6.1, 2),
                          (7.5, 4.7, 12), (7.5, 4.8, 10), (7.8, 4.4, 7), (8.1, 8.0, 8), (8.8, 5.6, 3), (9.8, 7.4, 8)],
                'p': 6, 'K': 4, 'beta': 0.5
            },
            # Applied Mode, map: the 40 largest cities of Germany, activity: the population in thousands (about 2023,
            # rounded; the coordinates are those of the city centres, rounded)
            'German Cities (Population)': {
                'areas': [(52.52, 13.405, 3755), (53.551, 9.993, 1892), (48.137, 11.575, 1512), (50.938, 6.96, 1084),
                          (50.11, 8.682, 773), (48.776, 9.183, 633), (51.227, 6.773, 629), (51.34, 12.375, 616),
                          (51.514, 7.468, 595), (51.456, 7.012, 584), (53.079, 8.802, 577), (51.05, 13.738, 563),
                          (52.376, 9.732, 548), (49.452, 11.077, 526), (51.435, 6.763, 503), (51.482, 7.216, 365),
                          (51.257, 7.151, 358), (52.021, 8.532, 338), (50.737, 7.098, 335), (51.961, 7.626, 320),
                          (49.488, 8.466, 316), (49.007, 8.404, 308), (48.371, 10.898, 300), (50.082, 8.24, 283),
                          (51.18, 6.443, 268), (51.518, 7.086, 263), (50.776, 6.084, 252), (52.269, 10.521, 251),
                          (54.323, 10.123, 247), (50.828, 12.921, 248), (51.483, 11.97, 242), (52.12, 11.628, 240),
                          (47.999, 7.842, 237), (51.339, 6.586, 228), (49.993, 8.247, 220), (53.866, 10.686, 218),
                          (50.978, 11.029, 216), (51.47, 6.852, 210), (54.092, 12.099, 209), (51.312, 9.48, 202)],
                'names': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt am Main', 'Stuttgart',
                          'Düsseldorf', 'Leipzig', 'Dortmund', 'Essen', 'Bremen', 'Dresden',
                          'Hanover', 'Nuremberg', 'Duisburg', 'Bochum', 'Wuppertal', 'Bielefeld',
                          'Bonn', 'Münster', 'Mannheim', 'Karlsruhe', 'Augsburg', 'Wiesbaden',
                          'Mönchengladbach', 'Gelsenkirchen', 'Aachen', 'Braunschweig', 'Kiel', 'Chemnitz',
                          'Halle (Saale)', 'Magdeburg', 'Freiburg im Breisgau', 'Krefeld', 'Mainz', 'Lübeck',
                          'Erfurt', 'Oberhausen', 'Rostock', 'Kassel'],
                'p': 6, 'K': 4, 'beta': 0.5
            },
            # Applied Mode, map: the 70 universities of the power conferences of NCAA Division I (ACC, Big Ten, Big 12,
            # SEC and the remaining Pac-12, season 2024-25; coordinates of the campuses, rounded), every one with the
            # activity 1 (one member of a conference): 4 conferences of about the same size, close together
            'US Division I Universities (Power Conferences)': {
                'areas': [(42.335, -71.169, 1), (37.872, -122.259, 1), (34.678, -82.837, 1), (36.001, -78.938, 1),
                          (30.442, -84.298, 1), (33.776, -84.398, 1), (38.212, -85.759, 1), (25.722, -80.279, 1),
                          (35.785, -78.682, 1), (35.905, -79.047, 1), (41.705, -86.235, 1), (40.444, -79.961, 1),
                          (32.841, -96.785, 1), (37.428, -122.17, 1), (43.038, -76.134, 1), (38.034, -78.508, 1),
                          (37.228, -80.423, 1), (36.135, -80.278, 1), (40.102, -88.227, 1), (39.168, -86.523, 1),
                          (41.661, -91.536, 1), (38.987, -76.943, 1), (42.278, -83.738, 1), (42.701, -84.482, 1),
                          (44.974, -93.228, 1), (40.82, -96.7, 1), (42.056, -87.675, 1), (40.007, -83.031, 1),
                          (44.045, -123.072, 1), (40.798, -77.86, 1), (40.424, -86.921, 1), (40.501, -74.447, 1),
                          (34.069, -118.445, 1), (34.022, -118.285, 1), (47.655, -122.304, 1), (43.076, -89.412, 1),
                          (32.232, -110.951, 1), (33.424, -111.928, 1), (31.548, -97.114, 1), (40.252, -111.649, 1),
                          (28.602, -81.2, 1), (39.133, -84.515, 1), (40.007, -105.266, 1), (29.72, -95.344, 1),
                          (42.027, -93.648, 1), (38.958, -95.248, 1), (39.191, -96.581, 1), (36.127, -97.074, 1),
                          (32.71, -97.363, 1), (33.584, -101.875, 1), (40.764, -111.842, 1), (39.635, -79.955, 1),
                          (33.214, -87.546, 1), (36.068, -94.175, 1), (32.603, -85.487, 1), (29.644, -82.355, 1),
                          (33.948, -83.377, 1), (38.031, -84.504, 1), (30.413, -91.18, 1), (34.365, -89.538, 1),
                          (33.455, -88.789, 1), (38.94, -92.328, 1), (35.206, -97.446, 1), (33.994, -81.03, 1),
                          (35.952, -83.93, 1), (30.285, -97.734, 1), (30.619, -96.339, 1), (36.145, -86.803, 1),
                          (44.564, -123.28, 1), (46.732, -117.155, 1)],
                'names': ['Boston College', 'California', 'Clemson', 'Duke', 'Florida State', 'Georgia Tech',
                          'Louisville', 'Miami', 'NC State', 'North Carolina', 'Notre Dame', 'Pittsburgh',
                          'SMU', 'Stanford', 'Syracuse', 'Virginia', 'Virginia Tech', 'Wake Forest',
                          'Illinois', 'Indiana', 'Iowa', 'Maryland', 'Michigan', 'Michigan State',
                          'Minnesota', 'Nebraska', 'Northwestern', 'Ohio State', 'Oregon', 'Penn State',
                          'Purdue', 'Rutgers', 'UCLA', 'USC', 'Washington', 'Wisconsin',
                          'Arizona', 'Arizona State', 'Baylor', 'BYU', 'UCF', 'Cincinnati',
                          'Colorado', 'Houston', 'Iowa State', 'Kansas', 'Kansas State', 'Oklahoma State',
                          'TCU', 'Texas Tech', 'Utah', 'West Virginia', 'Alabama', 'Arkansas',
                          'Auburn', 'Florida', 'Georgia', 'Kentucky', 'LSU', 'Ole Miss',
                          'Mississippi State', 'Missouri', 'Oklahoma', 'South Carolina', 'Tennessee', 'Texas',
                          'Texas A&M', 'Vanderbilt', 'Oregon State', 'Washington State'],
                'p': 4, 'K': 4, 'beta': 0.5
            },
        }
