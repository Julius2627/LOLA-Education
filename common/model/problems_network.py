class NetworkProblemRepository:
    """Provides the predefined network problems: 'directed', 'coords' (x or latitude, y or longitude, weight, name)
    and 'matrix' (lengths, None: no edge). An undirected network can give 'edges' (name, name, length) instead of
    'matrix'."""

    @staticmethod
    def get_predefined_problems():
        problems = {
            'ICE Network Germany': {
                'directed': True,
                'coords': [
                    (48.137154, 11.576124, 1.0, "München"),       
                    (52.520008, 13.404954, 1.0, "Berlin"),        
                    (53.551086, 9.993682, 1.0, "Hamburg"),        
                    (50.935173, 6.953101, 1.0, "Köln"),           
                    (50.110924, 8.682127, 1.0, "Frankfurt"), 

                    (48.783333, 9.183333, 1.0, "Stuttgart"),      
                    (51.233334, 6.783333, 1.0, "Düsseldorf"),
                    (51.514244, 7.468429, 1.0, "Dortmund"),       
                    (51.451, 7.016, 1.0, "Essen"),                
                    (53.0793, 8.8017, 1.0, "Bremen"),

                    (51.3397, 12.3731, 1.0, "Leipzig"),           
                    (51.0504, 13.7373, 1.0, "Dresden"),         
                    (52.3759, 9.7320, 1.0, "Hannover"),           
                    (49.4521, 11.0767, 1.0, "Nürnberg"),         
                    (51.4352, 6.7616, 1.0, "Duisburg"),           

                    (47.9990, 7.8421, 1.0, "Freiburg(Breisgau)"), 
                    (48.993997, 8.400558, 1.0, "Karlsruhe"),
                    (49.48776, 8.46622, 1.0, "Mannheim")
                ],
                'matrix': [
                    [None, None, None, None, None, 117, None, None, None, None, None, None, None, 64, None, None, None, None],
                    [None, None, 120, None, None, None, None, None, None, None, 75, 103, 100, None, None, None, None, None],
                    [None, 124, None, None, None, None, None, None, None, 52, None, None, 75, None, None, None, None, None],
                    [None, None, None, None, 63, None, 22, None, None, None, None, None, None, None, None, None, None, None],
                    [None, None, None, 63, None, 78, None, None, None, None, 176, None, 137, 120, None, None, None, 39],
                    [120, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 39, 35],
                    [None, None, None, 25, None, None, None, None, None, None, None, None, None, None, 11, None, None, None],
                    [None, None, None, None, None, None, None, None, 21, None, None, None, 101, None, None, None, None, None],
                    [None, None, None, None, None, None, None, 20, None, None, None, None, None, None, 10, None, None, None],
                    [None, None, 55, None, None, None, None, None, None, None, None, None, 59, None, None, None, None, None],
                    [None, 70, None, None, 183, None, None, None, None, None, None, 67, None, 133, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None, None, 76, None, None, None, None, None, None, None],
                    [None, 107, 74, None, 130, None, None, 99, None, 60, None, None, None, 177, None, None, None, None],
                    [65, None, None, None, 121, None, None, None, None, None, 124, None, 180, None, None, None, None, None],
                    [None, None, None, None, None, None, 12, None, 10, None, None, None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 62, None],
                    [None, None, None, None, None, 36, None, None, None, None, None, None, None, None, None, 62, None, 23],
                    [None, None, None, None, 35, 37, None, None, None, None, None, None, None, None, None, None, 23, None]
                ]
            },
            'Fac. Loc. Lecture Example 1': {
                'directed': False,
                'coords': [
                    (0, 0, 3.0, "v1"),
                    (0, -4, 1.0, "v2"),
                    (2, 0, 2.0, "v3"),
                    (2, -4, 5.0, "v4"),
                    (4, -2, 7.0, "v5")
                ],
                'matrix': [
                    [None, 7,    8,    None, None],
                    [7,    None, 4, None, None],
                    [8,    4, None, 8, 5],
                    [None,    None,    8,    None, 5],
                    [None,    None,    5,    5, None]
                ]
            },
            'Fac. Loc. Lecture Example 2': {
                'directed': False,
                'coords': [
                    (0, 0, 3.0, "v1"),
                    (0, -4, 1.0, "v2"),
                    (2, 0, 6.0, "v3"),
                    (2, -4, 5.0, "v4"),
                    (4, -2, 4.0, "v5")
                ],
                'matrix': [
                    [None, 7,    8,    None, None],
                    [7,    None, 4, None, None],
                    [8,    4, None, 8, 5],
                    [None,    None,    8,    None, 5],
                    [None,    None,    5,    5, None]
                ]
            },
            'Fac. Loc. Lecture Example 3': {
                'directed': False,
                'coords': [
                    (0, 0, 1.0, "v1"),
                    (0, -4, 1.0, "v2"),
                    (4, 0, 2.0, "v3"),
                    (4, -4, 2.0, "v4")
                ],
                'matrix': [
                    [None, 8,    3,    None],
                    [8,    None, None, 3],
                    [3,   None, None, 4],
                    [None,    3,    4,    None]
                ]
            },
            'Fac. Loc. Lecture Example 4': {
                'directed': False,
                'coords': [
                    (0, 0, 5.0, "v1"),
                    (0, -4, 1.0, "v2"),
                    (2, 0, 2.0, "v3"),
                    (2, -4, 5.0, "v4"),
                    (4, -2, 7.0, "v5")
                ],
                'matrix': [
                    [None, 7,    8,    None, None],
                    [7,    None, 4, None, None],
                    [8,    4, None, 8, 5],
                    [None,    None,    8,    None, 5],
                    [None,    None,    5,    5, None]
                ]
            },

            'GT Lecture Ch. 6 Example 1': {
                'directed': False,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (0,  -4, 1.0, "v2"),
                    (4, 0, 1.0, "v3"),
                    (4,  -4, 1.0, "v4")
                ],
                'matrix': [
                    [None, 5,    2, None],     # v1
                    [5, None, None,    1],     # v2
                    [2,    None,    None, 3],  # v3
                    [None,    1, 3,    None]   # v4
                ]
            },
            'GT Lecture Ch. 6 Example 2': {
                'directed': True,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (0,  -4, 1.0, "v2"),
                    (4, 0, 1.0, "v3"),
                    (4,  -4, 1.0, "v4")
                ],
                'matrix': [
                    [None, 4,  1, None],     # v1
                    [2, None, None,    1],     # v2
                    [None,  None,    None, 3],  # v3
                    [2,    None, None,    None]   # v4
                ]
            },
            'GT Lecture Ch. 7 Example 1': {
                'directed': False,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (4,  0, 1.0, "v2"),
                    (0, -4, 1.0, "v3"),
                    (4, -4, 1.0, "v4")
                ],
                'matrix': [
                    [None, 1,    4,    2],  # v1
                    [1,    None, None, 5],     # v2
                    [4,    None, None, 1],     # v3
                    [2, 5,    1,    None]   # v4
                ]
            },
            'GT Lecture Ch. 7 Example 2': {
                'directed': False,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (4,  0, 1.0, "v2"),
                    (5, -2, 1.0, "v3"),
                    (1, -2, 1.0, "v4"),
                    (3, -3, 1.0, "v5")
                ],
                'matrix': [
                    [None, 4,  None,  1, None],     # v1
                    [4,  None, 2, None,  None],    # v2
                    [None,  2, None, 2,  None],    # v3
                    [1, None,  2,  None, 1],    # v4
                    [None, None,   None,   1,   None]   # v5
                ]
            },
            'GT Lecture Ch. 8 Example 1': {
                'directed': True,
                'coords': [
                    (-4,  0, 1.0, "v1"),
                    (0,  4, 1.0, "v2"),
                    (0, -4, 1.0, "v3"),
                    (4, 0, 1.0, "v4")
                ],
                'matrix': [
                    [None, 1,  None,  1],     # v1
                    [None,  None, 4, 1],    # v2
                    [1,  1, None, None],    # v3
                    [1, None,  4,  None]    # v4
                ]
            },
            'GT Lecture Ch. 8 Example 2': {
                'directed': True,
                'coords': [
                    (-4,  0, 2.0, "v1"),
                    (0,  4, 3.0, "v2"),
                    (0, -4, 2.0, "v3"),
                    (4, 0, 1.0, "v4")
                ],
                'matrix': [
                    [None, 1,  None,  1],     # v1
                    [None,  None, 4, 1],    # v2
                    [1,  1, None, None],    # v3
                    [1, None,  4,  None]    # v4
                ]
            },
            'GT Lecture Ch. 8 Example 3': {
                'directed': False,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (4,  0, 1.0, "v2"),
                    (0, -4, 2.0, "v3"),
                    (4,  -4, 2.0, "v4")
                ],
                'matrix': [
                    [None, 8,  3, None],     # v1
                    [8, None, None,    3],     # v2
                    [3,  None,    None, 4],  # v3
                    [None,    3, 4,    None]   # v4
                ]
            },
            'GT Lecture Ch. 8 Example 4': {
                'directed': False,
                'coords': [
                    (0,  0, 2.0, "v1"),
                    (4,  0, 2.0, "v2"),
                    (0, -4, 2.0, "v3"),
                    (4, -4, 2.0, "v4"),
                    (2, -2, 8.0, "s")
                ],
                'matrix': [
                    [None, 0.1,  0.1,  None, 10],     # v1
                    [0.1,  None, None, 0.1,  10],    # v2
                    [0.1,  None, None, 0.1,  10],    # v3
                    [None, 0.1,  0.1,  None, 10],    # v4
                    [10, 10,   10,   10,   None]   # s
                ]
            },
            'GT Lecture Ch. 8 Example Q-Crit. 1': {
                'directed': False,

                'coords': [
                    (0,  0, 1.0, "v1"),
                    (4,  0, 1.0, "v2"),
                    (0,  2, 1.0, "v3"),
                    (4,  2, 1.0, "v4"),
                    (0, -2, 1.0, "v5"),
                    (4, -2, 1.0, "v6")
                ],

                'weights': [
                    [1, 2, 1, 2, 2, 2],  # erster Gewichtsvektor
                    [2, 1, 2, 2, 2, 1]   # zweiter Gewichtsvektor
                ],

                'matrix': [
                    [None, 1,    1,    None, 3,    None],  # v1
                    [1,    None, None, 3,    None, 1   ],  # v2
                    [1,    None, None, 3,    2,    None],  # v3
                    [None, 3,    3,    None, None, 2   ],  # v4
                    [3,    None, 2,    None, None, 3   ],  # v5
                    [None, 1,    None, 2,    3,    None]   # v6
                ]
            },
            'GT Lecture Ch. 8 Example Q-Crit. 2': {
                'directed': False,

                'coords': [
                    (0,  1, "v1"),
                    (4,  1, "v2"),
                    (0, -1, "v3"),
                    (4, -1, "v4")
                ],

                'weights': [
                    [1, 2, 2, 2],  # erster Gewichtsvektor
                    [3, 1, 2, 1]   # zweiter Gewichtsvektor
                ],

                'matrix': [
                    [None, 1,    2,    None],  # v1
                    [1,    None, None, 1   ],  # v2
                    [2,    None, None, 1   ],  # v3
                    [None, 1,    1,    None]   # v4
                ]
            },
            'GT Lecture Ch. 9 Example 1': {
                'directed': False,
                'coords': [
                    (-4,  0, 1.0, "v1"),
                    (0,  0, 1.0, "v2"),
                    (4, 0, 1.0, "v3"),
                    (0, -4, 1.0, "v4"),
                    (4, -4, 1.0, "v5")
                ],
                'matrix': [
                    [None, 6,  None,  None, None],     # v1
                    [6,  None, 3, 4, None],    # v2
                    [None,  3, None, None, 2],    # v3
                    [None, 4,  None,  None, 5],    # v4
                    [None, None, 2, 5, None]
                ]
            },
            'GT Lecture Ch. 9 Example 2': {
                'directed': False,
                'coords': [
                    (-4,  0, 1.0, "v1"),
                    (0,  4, 1.0, "v2"),
                    (2, 0, 1.0, "v3"),
                    (-2, 0, 1.0, "v4"),
                    (0, -4, 1.0, "v5"),
                    (4, 0, 1.0, "v6")
                ],
                'matrix': [
                    [None, 5,  None,  7, 4, None],     # v1
                    [5,  None, 5, 3, None, 6],    # v2
                    [None,  5, None, 2, 3, 8],    # v3
                    [7, 3,  2,  None, 4, None],    # v4
                    [4, None, 3, 4, None, 5],
                    [None, 6, 8, None, 5, None]
                ]
            },
            'GT Lecture Ch. 9 Example 3': {
                'directed': False,
                'coords': [
                    (-4,  4, 10.0, "v1"),
                    (0,  2, 8.0, "v2"),
                    (4, 4, 22.0, "v3"),
                    (-4, -4, 18.0, "v4"),
                    (0, -2, 7.0, "v5"),
                    (4, -4, 16.0, "v6")
                ],
                'matrix': [
                    [None, 8,  15,  10, None, None],     # v1
                    [8,  None, 12, 7, 16, None],    # v2
                    [15,  12, None, None, 9, 11],    # v3
                    [10, 7,  None,  None, 11, 17],    # v4
                    [None, 16, 9, 11, None, 13],
                    [None, None, 11, 17, 13, None]
                ]
            },

            'GT Exercise 6 Task 2/3': {
                'directed': False,
                'coords': [
                    (0, 0, 1.0, "v1"),
                    (4, 0, 1.0, "v2"),
                    (0, -4, 1.0, "v3"),
                    (4, -4, 1.0, "v4")
                ],
                'matrix': [
                    [None, 1,    4,    2],
                    [1,    None, None, 5],
                    [4,    None, None, 1],
                    [2,    5,    1,    None]
                ]
            },
            'GT Exercise 7 Task 1a':{
                'directed': False,
                'coords': [
                    (0, 0, 3.0, "v1"),
                    (4, 0, 4.0, "v2"),
                    (2, -1, 1.0, "v3"),
                    (0, -4, 2.0, "v4"),
                    (4, -4, 2.0, "v5"),
                    (2, -6, 6,  "v6")
                ],
                'matrix': [
                    [None, None, 2,    None, None, None],  # v1
                    [None, None, 4,    None, None, None],  # v2
                    [2,    4,    None, 8,    3,    None],  # v3
                    [None, None, 8,    None, 4,    1],     # v4
                    [None, None, 3,    4,    None, 2],     # v5
                    [None, None, None, 1,    2,    None]   # v6
                ]
            },
            'GT Exercise 7 Task 1b': {
                'directed': True,
                'coords': [
                    (2,  0, 2.0, "v1"),
                    (2, -2, 5.0, "v2"),
                    (0, -4, 5.0, "v3"),
                    (4, -4, 2.0, "v4"),
                    (0, -6, 4.0, "v5"),
                    (4, -6, 2.0, "v6")
                ],
                'matrix': [
                    [None, 5,    None, None, None, None],  # v1
                    [3,    None, None, 2,    None, None],  # v2
                    [None, 3,    None, None, 2,    None],  # v3
                    [None, None, 4,    None, None, 4],     # v4
                    [None, None, 2,    None, None, None],  # v5
                    [None, None, None, 1,    None, None]   # v6
                ]
            },
            'GT Exercise 7 Task 2': {
                'directed': False,
                'coords': [
                    (0, 0, "v1"),
                    (4, 0, "v2"),
                    (0, -4, "v3"),
                    (4, -4, "v4")
                ],
                'weights': [
                    [2, 1, 1, 1],  # erster Gewichtsvektor
                    [1, 1, 2, 1]   # zweiter Gewichtsvektor
                ],
                'matrix': [
                    [None, 4,    2,    3],
                    [4,    None, 3, 2],
                    [2,    3, None, 4],
                    [3,    2,    4,    None]
                ]
            },
            'GT Exercise 8 Task 1': {
                'directed': False,
                'coords': [
                    (0,  0, 1.0, "v1"),
                    (2,  1, 1.0, "v2"),
                    (2, -1, 1.0, "v3"),
                    (5,  1, 1.0, "v4"),
                    (5, -1, 1.0, "v5"),
                    (7,  0, 1.0, "v6")
                ],
                'matrix': [
                    [None, 3,    4,    None, None, None],  # v1
                    [3,    None, 3,    4,    5,    None],  # v2
                    [4,    3,    None, None, 2,    None],  # v3
                    [None, 4,    None, None, 4,    4   ],  # v4
                    [None, 5,    2,    4,    None, 3   ],  # v5
                    [None, None, None, 4,    3,    None]   # v6
                ]
            },
            'GT Exercise 8 Task 2': {
                'directed': False,
                'coords': [
                    (0,  0,  6.0, "v1"),
                    (2,  1,  4.0, "v2"),
                    (2, -1,  8.0, "v3"),
                    (5,  1, 10.0, "v4"),
                    (5, -1, 10.0, "v5"),
                    (7,  0,  6.0, "v6")
                ],
                'matrix': [
                    [None, 6,    8,    None, None, None],  # v1
                    [6,    None, 6,    8,    10,   None],  # v2
                    [8,    6,    None, None, 8,    None],  # v3
                    [None, 8,    None, None, 8,    8   ],  # v4
                    [None, 10,   8,    8,    None, 6   ],  # v5
                    [None, None, None, 8,    6,    None]   # v6
                ]
            },

            # Applied Mode: the planar examples as networks
            'KIT Campus': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (49.011556, 8.416286, 1.0, "KIT Library"),
                    (49.014810, 8.420493, 1.0, "Lecture Hall Fasanengarten"),
                    (49.012909, 8.415479, 1.0, "Audimax"),
                    (49.011915, 8.417309, 1.0, "Dining Hall"),
                    (49.009456, 8.414187, 1.0, "Mechanical Engineering Building"),
                    (49.011428, 8.413905, 1.0, "Chemistry Building"),
                    (48.993192, 8.401711, 1.0, "Karlsruhe Central Station"),
                    (49.013525, 8.404359, 1.0, "Karlsruhe Palace"),
                ],
                'edges': [
                    ("KIT Library", "Lecture Hall Fasanengarten", 0.68),
                    ("KIT Library", "Audimax", 0.21),
                    ("KIT Library", "Dining Hall", 0.14),
                    ("KIT Library", "Mechanical Engineering Building", 0.37),
                    ("KIT Library", "Chemistry Building", 0.31),
                    ("KIT Library", "Karlsruhe Central Station", 4.0),
                    ("KIT Library", "Karlsruhe Palace", 1.29),
                    ("Lecture Hall Fasanengarten", "Audimax", 0.54),
                    ("Lecture Hall Fasanengarten", "Dining Hall", 0.57),
                    ("Lecture Hall Fasanengarten", "Mechanical Engineering Building", 1.04),
                    ("Lecture Hall Fasanengarten", "Chemistry Building", 0.97),
                    ("Lecture Hall Fasanengarten", "Karlsruhe Central Station", 4.1),
                    ("Lecture Hall Fasanengarten", "Karlsruhe Palace", 1.5),
                    ("Audimax", "Dining Hall", 0.21),
                    ("Audimax", "Mechanical Engineering Building", 0.54),
                    ("Audimax", "Chemistry Building", 0.48),
                    ("Audimax", "Karlsruhe Central Station", 4.2),
                    ("Audimax", "Karlsruhe Palace", 1.16),
                    ("Dining Hall", "Chemistry Building", 0.45),
                    ("Dining Hall", "Karlsruhe Central Station", 4.05),
                    ("Dining Hall", "Karlsruhe Palace", 1.35),
                    ("Mechanical Engineering Building", "Chemistry Building", 0.32),
                    ("Mechanical Engineering Building", "Karlsruhe Central Station", 3.82),
                    ("Mechanical Engineering Building", "Karlsruhe Palace", 1.27),
                    ("Chemistry Building", "Karlsruhe Central Station", 4.13),
                    ("Chemistry Building", "Karlsruhe Palace", 1.14),
                    ("Karlsruhe Central Station", "Karlsruhe Palace", 4.64),
                ]
            },
            'Karlsruhe Bars': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (49.005440, 8.411916, 1.0, "Agostea Nightclub"),
                    (49.004029, 8.404239, 1.0, "Die Stadtmitte"),
                    (49.008894, 8.403844, 1.0, "Café Emaille"),
                    (49.011650, 8.395029, 1.0, "Scruffy's Irish Pub"),
                    (49.013893, 8.357782, 1.0, "Vanguarde"),
                    (49.008519, 8.395981, 1.0, "La Cage"),
                    (49.008638, 8.395750, 1.0, "Enchilada Karlsruhe"),
                    (49.007621, 8.414519, 1.0, "Old Chapel Pub"),
                ],
                'edges': [
                    ("Agostea Nightclub", "Die Stadtmitte", 0.66),
                    ("Agostea Nightclub", "Café Emaille", 1.65),
                    ("Agostea Nightclub", "La Cage", 1.56),
                    ("Agostea Nightclub", "Old Chapel Pub", 0.56),
                    ("Die Stadtmitte", "Café Emaille", 1.31),
                    ("Die Stadtmitte", "Scruffy's Irish Pub", 1.65),
                    ("Die Stadtmitte", "La Cage", 1.13),
                    ("Die Stadtmitte", "Old Chapel Pub", 1.1),
                    ("Café Emaille", "Scruffy's Irish Pub", 1.03),
                    ("Café Emaille", "Vanguarde", 4.21),
                    ("Café Emaille", "La Cage", 0.83),
                    ("Café Emaille", "Old Chapel Pub", 1.66),
                    ("Scruffy's Irish Pub", "Vanguarde", 3.33),
                    ("Scruffy's Irish Pub", "Enchilada Karlsruhe", 0.57),
                    ("Vanguarde", "Enchilada Karlsruhe", 3.45),
                    ("La Cage", "Enchilada Karlsruhe", 0.02),
                    ("La Cage", "Old Chapel Pub", 1.68),
                ]
            },
            'Berlin Landmarks': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (52.516270, 13.377703, 1.0, "Brandenburg Gate"),
                    (52.518654, 13.376102, 1.0, "Reichstag Building"),
                    (52.520645, 13.409779, 1.0, "TV Tower"),
                    (52.504454, 13.440839, 1.0, "East Side Gallery"),
                    (52.500250, 13.308714, 1.0, "Kurfürstendamm"),
                    (52.488444, 13.470315, 1.0, "Treptower Park"),
                    (52.509649, 13.376168, 1.0, "Potsdamer Platz"),
                    (52.522681, 13.402342, 1.0, "Hackescher Markt"),
                ],
                'edges': [
                    ("Brandenburg Gate", "Reichstag Building", 0.34),
                    ("Brandenburg Gate", "TV Tower", 2.49),
                    ("Brandenburg Gate", "East Side Gallery", 5.27),
                    ("Brandenburg Gate", "Kurfürstendamm", 6.12),
                    ("Brandenburg Gate", "Treptower Park", 8.34),
                    ("Brandenburg Gate", "Potsdamer Platz", 0.81),
                    ("Brandenburg Gate", "Hackescher Markt", 2.16),
                    ("Reichstag Building", "TV Tower", 2.77),
                    ("Reichstag Building", "East Side Gallery", 5.55),
                    ("Reichstag Building", "Kurfürstendamm", 6.33),
                    ("Reichstag Building", "Treptower Park", 8.63),
                    ("Reichstag Building", "Potsdamer Platz", 1.07),
                    ("Reichstag Building", "Hackescher Markt", 2.35),
                    ("TV Tower", "East Side Gallery", 3.34),
                    ("TV Tower", "Kurfürstendamm", 8.59),
                    ("TV Tower", "Treptower Park", 6.34),
                    ("TV Tower", "Potsdamer Platz", 3.09),
                    ("TV Tower", "Hackescher Markt", 1.04),
                    ("East Side Gallery", "Treptower Park", 3.21),
                    ("East Side Gallery", "Potsdamer Platz", 5.6),
                    ("East Side Gallery", "Hackescher Markt", 3.73),
                    ("Kurfürstendamm", "Potsdamer Platz", 5.94),
                    ("Treptower Park", "Potsdamer Platz", 8.31),
                    ("Treptower Park", "Hackescher Markt", 6.73),
                ]
            },
            'London Landmarks': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (51.500729, -0.124625, 1.0, "Big Ben"),
                    (51.507351, -0.127758, 1.0, "Trafalgar Square"),
                    (51.504365, -0.086474, 1.0, "The Shard"),
                    (51.503324, -0.119543, 1.0, "London Eye"),
                    (51.505456, -0.075356, 1.0, "Tower Bridge"),
                    (51.513787, -0.098451, 1.0, "St. Paul's Cathedral"),
                    (51.518769, -0.126409, 1.0, "British Museum"),
                    (51.530133, -0.153764, 1.0, "Regent's Park"),
                ],
                'edges': [
                    ("Big Ben", "Trafalgar Square", 0.86),
                    ("Big Ben", "The Shard", 3.35),
                    ("Big Ben", "London Eye", 0.85),
                    ("Big Ben", "Tower Bridge", 4.49),
                    ("Big Ben", "St. Paul's Cathedral", 2.82),
                    ("Big Ben", "Regent's Park", 4.87),
                    ("Trafalgar Square", "The Shard", 3.84),
                    ("Trafalgar Square", "Tower Bridge", 5.01),
                    ("Trafalgar Square", "St. Paul's Cathedral", 2.5),
                    ("Trafalgar Square", "British Museum", 1.72),
                    ("Trafalgar Square", "Regent's Park", 4.05),
                    ("The Shard", "London Eye", 3.08),
                    ("The Shard", "Tower Bridge", 1.19),
                    ("The Shard", "St. Paul's Cathedral", 1.94),
                    ("The Shard", "British Museum", 4.31),
                    ("The Shard", "Regent's Park", 7.1),
                    ("London Eye", "Tower Bridge", 4.26),
                    ("London Eye", "St. Paul's Cathedral", 2.25),
                    ("London Eye", "British Museum", 2.62),
                    ("London Eye", "Regent's Park", 5.41),
                    ("Tower Bridge", "St. Paul's Cathedral", 2.69),
                    ("Tower Bridge", "British Museum", 5.2),
                    ("Tower Bridge", "Regent's Park", 8.28),
                    ("St. Paul's Cathedral", "British Museum", 2.77),
                    ("St. Paul's Cathedral", "Regent's Park", 5.77),
                    ("British Museum", "Regent's Park", 3.26),
                ]
            },
            'Munich Beer Gardens': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (48.137633, 11.579979, 1.0, "Hofbräuhaus"),
                    (48.143503, 11.551566, 1.0, "Augustiner-Keller"),
                    (48.139206, 11.545647, 1.0, "Augustiner Bräustuben"),
                    (48.126042, 11.559521, 1.0, "Paulaner Bräuhaus"),
                    (48.160516, 11.598326, 1.0, "Seehaus (English Garden)"),
                    (48.135109, 11.575537, 1.0, "Viktualienmarkt Beer Garden"),
                    (48.148114, 11.558320, 1.0, "Löwenbräukeller"),
                    (48.152552, 11.592097, 1.0, "Chinese Tower"),
                ],
                'edges': [
                    ("Hofbräuhaus", "Seehaus (English Garden)", 3.62),
                    ("Hofbräuhaus", "Viktualienmarkt Beer Garden", 0.59),
                    ("Hofbräuhaus", "Chinese Tower", 2.5),
                    ("Augustiner-Keller", "Augustiner Bräustuben", 1.7),
                    ("Augustiner-Keller", "Paulaner Bräuhaus", 4.05),
                    ("Augustiner-Keller", "Viktualienmarkt Beer Garden", 3.05),
                    ("Augustiner-Keller", "Löwenbräukeller", 1.36),
                    ("Augustiner-Keller", "Chinese Tower", 4.75),
                    ("Augustiner Bräustuben", "Paulaner Bräuhaus", 2.95),
                    ("Augustiner Bräustuben", "Seehaus (English Garden)", 5.89),
                    ("Augustiner Bräustuben", "Viktualienmarkt Beer Garden", 2.92),
                    ("Augustiner Bräustuben", "Chinese Tower", 4.77),
                    ("Paulaner Bräuhaus", "Viktualienmarkt Beer Garden", 2.09),
                    ("Paulaner Bräuhaus", "Löwenbräukeller", 4.2),
                    ("Seehaus (English Garden)", "Viktualienmarkt Beer Garden", 4.18),
                    ("Seehaus (English Garden)", "Chinese Tower", 1.2),
                    ("Viktualienmarkt Beer Garden", "Löwenbräukeller", 2.97),
                    ("Viktualienmarkt Beer Garden", "Chinese Tower", 3.06),
                    ("Löwenbräukeller", "Chinese Tower", 3.96),
                ]
            },
            'Tokyo Landmarks': {   # bike routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (35.658581, 139.745438, 1.0, "Tokyo Tower"),
                    (35.685072, 139.709547, 1.0, "Shinjuku Gyoen"),
                    (35.713403, 139.795526, 1.0, "Senso-ji Temple"),
                    (35.676397, 139.699326, 1.0, "Meiji Shrine"),
                    (35.658034, 139.701636, 1.0, "Shibuya Crossing"),
                    (35.699593, 139.774219, 1.0, "Akihabara"),
                    (35.670502, 139.702414, 1.0, "Harajuku"),
                    (35.671170, 139.766249, 1.0, "Ginza"),
                ],
                'edges': [
                    ("Tokyo Tower", "Shinjuku Gyoen", 6.11),
                    ("Tokyo Tower", "Senso-ji Temple", 9.17),
                    ("Tokyo Tower", "Meiji Shrine", 5.67),
                    ("Tokyo Tower", "Shibuya Crossing", 4.39),
                    ("Tokyo Tower", "Akihabara", 6.0),
                    ("Tokyo Tower", "Harajuku", 4.66),
                    ("Tokyo Tower", "Ginza", 3.26),
                    ("Shinjuku Gyoen", "Senso-ji Temple", 10.74),
                    ("Shinjuku Gyoen", "Meiji Shrine", 3.07),
                    ("Shinjuku Gyoen", "Shibuya Crossing", 4.74),
                    ("Shinjuku Gyoen", "Akihabara", 7.51),
                    ("Shinjuku Gyoen", "Harajuku", 3.45),
                    ("Shinjuku Gyoen", "Ginza", 7.23),
                    ("Senso-ji Temple", "Meiji Shrine", 12.64),
                    ("Senso-ji Temple", "Shibuya Crossing", 13.13),
                    ("Senso-ji Temple", "Akihabara", 3.6),
                    ("Senso-ji Temple", "Harajuku", 12.34),
                    ("Senso-ji Temple", "Ginza", 6.33),
                    ("Meiji Shrine", "Shibuya Crossing", 2.46),
                    ("Meiji Shrine", "Akihabara", 9.42),
                    ("Meiji Shrine", "Harajuku", 1.18),
                    ("Meiji Shrine", "Ginza", 8.25),
                    ("Shibuya Crossing", "Akihabara", 9.7),
                    ("Shibuya Crossing", "Harajuku", 1.52),
                    ("Shibuya Crossing", "Ginza", 7.14),
                    ("Akihabara", "Harajuku", 9.23),
                    ("Akihabara", "Ginza", 4.05),
                    ("Harajuku", "Ginza", 7.24),
                ]
            },
            'Silicon Valley': {   # road routes (OSRM, routing.openstreetmap.de), mean of both directions, km
                'directed': False,
                'coords': [
                    (37.422004, -122.084075, 1.0, "Google HQ"),
                    (37.334835, -122.011392, 1.0, "Apple HQ"),
                    (37.484722, -122.148333, 1.0, "Meta HQ"),
                    (37.427489, -122.171786, 1.0, "Stanford University"),
                    (37.774930, -122.419420, 1.0, "San Francisco"),
                    (37.338208, -121.886329, 1.0, "San Jose"),
                    (37.871593, -122.272743, 1.0, "Berkeley"),
                    (37.804364, -122.271114, 1.0, "Oakland"),
                ],
                'edges': [
                    ("Google HQ", "Apple HQ", 16.75),
                    ("Google HQ", "Meta HQ", 11.24),
                    ("Google HQ", "Stanford University", 12.67),
                    ("Google HQ", "San Francisco", 56.92),
                    ("Google HQ", "San Jose", 22.67),
                    ("Google HQ", "Berkeley", 67.47),
                    ("Google HQ", "Oakland", 59.36),
                    ("Apple HQ", "Meta HQ", 26.03),
                    ("Apple HQ", "Stanford University", 24.51),
                    ("Apple HQ", "San Francisco", 71.71),
                    ("Apple HQ", "San Jose", 15.26),
                    ("Meta HQ", "Stanford University", 8.86),
                    ("Meta HQ", "San Francisco", 48.87),
                    ("Meta HQ", "San Jose", 31.97),
                    ("Meta HQ", "Berkeley", 57.17),
                    ("Meta HQ", "Oakland", 49.06),
                    ("Stanford University", "San Francisco", 55.57),
                    ("Stanford University", "San Jose", 34.81),
                    ("Stanford University", "Berkeley", 65.09),
                    ("Stanford University", "Oakland", 56.98),
                    ("San Francisco", "San Jose", 77.65),
                    ("San Francisco", "Berkeley", 21.65),
                    ("San Francisco", "Oakland", 18.32),
                    ("San Jose", "Berkeley", 73.72),
                    ("San Jose", "Oakland", 65.62),
                    ("Berkeley", "Oakland", 8.27),
                ]
            },
            'Great Lakes': {   # water distances between the harbours (NOAA, Distances Between United States Ports 2026), km
                'directed': False,
                'coords': [
                    (43.653226, -79.383184, 1.0, "Toronto, Canada"),
                    (41.878114, -87.629798, 1.0, "Chicago, USA"),
                    (42.331427, -83.045754, 1.0, "Detroit, USA"),
                    (43.038902, -87.906474, 1.0, "Milwaukee, USA"),
                    (45.501689, -73.567256, 1.0, "Montreal, Canada"),
                    (46.813878, -71.207981, 1.0, "Quebec City, Canada"),
                    (46.783829, -92.105268, 1.0, "Duluth, USA"),
                    (41.499321, -81.694361, 1.0, "Cleveland, USA"),
                ],
                'edges': [
                    ("Toronto, Canada", "Detroit, USA", 481.2),
                    ("Toronto, Canada", "Montreal, Canada", 550.4),
                    ("Toronto, Canada", "Cleveland, USA", 346.0),
                    ("Chicago, USA", "Detroit, USA", 1018.7),
                    ("Chicago, USA", "Milwaukee, USA", 136.8),
                    ("Chicago, USA", "Duluth, USA", 1300.3),
                    ("Chicago, USA", "Cleveland, USA", 1190.9),
                    ("Detroit, USA", "Milwaukee, USA", 914.1),
                    ("Detroit, USA", "Montreal, Canada", 986.5),
                    ("Detroit, USA", "Duluth, USA", 1168.4),
                    ("Detroit, USA", "Cleveland, USA", 173.8),
                    ("Milwaukee, USA", "Duluth, USA", 1195.7),
                    ("Milwaukee, USA", "Cleveland, USA", 1086.3),
                    ("Montreal, Canada", "Quebec City, Canada", 257.5),
                    ("Montreal, Canada", "Cleveland, USA", 851.3),
                    ("Duluth, USA", "Cleveland, USA", 1340.6),
                ]
            },
            'European Capitals': {   # rail distances between the main stations (BRouter, rail profile), shortest paths, km
                'directed': False,
                'coords': [
                    (48.856614, 2.352222, 1.0, "Paris, France"),
                    (51.507351, -0.127758, 1.0, "London, UK"),
                    (52.520007, 13.404954, 1.0, "Berlin, Germany"),
                    (41.902784, 12.496366, 1.0, "Rome, Italy"),
                    (40.416775, -3.703790, 1.0, "Madrid, Spain"),
                    (48.208174, 16.373819, 1.0, "Vienna, Austria"),
                    (50.075538, 14.437800, 1.0, "Prague, Czechia"),
                    (59.329323, 18.068581, 1.0, "Stockholm, Sweden"),
                    (60.169856, 24.938379, 1.0, "Helsinki, Finland"),
                    (55.755826, 37.617300, 1.0, "Moscow, Russia"),
                ],
                'edges': [
                    ("Paris, France", "London, UK", 460.8),
                    ("Paris, France", "Berlin, Germany", 1228.0),
                    ("Paris, France", "Rome, Italy", 1625.2),
                    ("Paris, France", "Madrid, Spain", 1857.6),
                    ("Paris, France", "Prague, Czechia", 1275.1),
                    ("Paris, France", "Stockholm, Sweden", 2213.0),
                    ("London, UK", "Berlin, Germany", 1373.0),
                    ("London, UK", "Rome, Italy", 1995.1),
                    ("London, UK", "Prague, Czechia", 1456.2),
                    ("London, UK", "Stockholm, Sweden", 2224.4),
                    ("Berlin, Germany", "Madrid, Spain", 2673.4),
                    ("Berlin, Germany", "Vienna, Austria", 701.4),
                    ("Berlin, Germany", "Prague, Czechia", 384.5),
                    ("Berlin, Germany", "Stockholm, Sweden", 1409.9),
                    ("Berlin, Germany", "Helsinki, Finland", 2641.7),
                    ("Berlin, Germany", "Moscow, Russia", 2153.7),
                    ("Rome, Italy", "Madrid, Spain", 2315.9),
                    ("Rome, Italy", "Vienna, Austria", 1086.2),
                    ("Rome, Italy", "Prague, Czechia", 1286.4),
                    ("Madrid, Spain", "Vienna, Austria", 2614.2),
                    ("Madrid, Spain", "Prague, Czechia", 2539.3),
                    ("Madrid, Spain", "Stockholm, Sweden", 3933.2),
                    ("Vienna, Austria", "Prague, Czechia", 349.2),
                    ("Vienna, Austria", "Helsinki, Finland", 2803.4),
                    ("Vienna, Austria", "Moscow, Russia", 2315.4),
                    ("Prague, Czechia", "Helsinki, Finland", 2691.7),
                    ("Prague, Czechia", "Moscow, Russia", 2203.7),
                    ("Stockholm, Sweden", "Helsinki, Finland", 1993.3),
                    ("Helsinki, Finland", "Moscow, Russia", 1073.1),
                ]
            },
            'World Cities': {   # great-circle distances (Haversine) between the main international airports, km
                'directed': False,
                'coords': [
                    (34.052235, -118.243683, 1.0, "Los Angeles, USA"),
                    (35.689487, 139.691706, 1.0, "Tokyo, Japan"),
                    (40.712776, -74.005974, 1.0, "New York City, USA"),
                    (19.432608, -99.133209, 1.0, "Mexico City, Mexico"),
                    (28.613939, 77.209023, 1.0, "Delhi, India"),
                    (31.230416, 121.473701, 1.0, "Shanghai, China"),
                    (1.352083, 103.819836, 1.0, "Singapore"),
                    (55.755826, 37.617300, 1.0, "Moscow, Russia"),
                ],
                'edges': [
                    ("Los Angeles, USA", "Tokyo, Japan", 8812.1),
                    ("Los Angeles, USA", "New York City, USA", 3975.3),
                    ("Los Angeles, USA", "Mexico City, Mexico", 2501.1),
                    ("Los Angeles, USA", "Delhi, India", 12876.6),
                    ("Los Angeles, USA", "Shanghai, China", 10414.5),
                    ("Los Angeles, USA", "Singapore", 14100.8),
                    ("Los Angeles, USA", "Moscow, Russia", 9757.6),
                    ("Tokyo, Japan", "New York City, USA", 10875.7),
                    ("Tokyo, Japan", "Mexico City, Mexico", 11313.0),
                    ("Tokyo, Japan", "Delhi, India", 5861.7),
                    ("Tokyo, Japan", "Shanghai, China", 1736.8),
                    ("Tokyo, Japan", "Singapore", 5299.3),
                    ("Tokyo, Japan", "Moscow, Russia", 7493.6),
                    ("New York City, USA", "Mexico City, Mexico", 3365.8),
                    ("New York City, USA", "Delhi, India", 11754.6),
                    ("New York City, USA", "Shanghai, China", 11873.4),
                    ("New York City, USA", "Singapore", 15340.1),
                    ("New York City, USA", "Moscow, Russia", 7480.8),
                    ("Mexico City, Mexico", "Delhi, India", 14662.9),
                    ("Mexico City, Mexico", "Shanghai, China", 12897.4),
                    ("Mexico City, Mexico", "Singapore", 16597.9),
                    ("Mexico City, Mexico", "Moscow, Russia", 10690.3),
                    ("Delhi, India", "Shanghai, China", 4293.4),
                    ("Delhi, India", "Singapore", 4159.5),
                    ("Delhi, India", "Moscow, Russia", 4363.0),
                    ("Shanghai, China", "Singapore", 3805.9),
                    ("Shanghai, China", "Moscow, Russia", 6850.3),
                    ("Singapore", "Moscow, Russia", 8450.2),
                ]
            },
            'Australian Cities': {   # great-circle distances (Haversine) between the main international airports, km
                'directed': False,
                'coords': [
                    (-33.868820, 151.209296, 1.0, "Sydney"),
                    (-37.813628, 144.963058, 1.0, "Melbourne"),
                    (-27.469771, 153.025124, 1.0, "Brisbane"),
                    (-31.950527, 115.860457, 1.0, "Perth"),
                    (-34.928499, 138.600746, 1.0, "Adelaide"),
                    (-35.280937, 149.130009, 1.0, "Canberra"),
                    (-42.882138, 147.327195, 1.0, "Hobart"),
                    (-12.463440, 130.845642, 1.0, "Darwin"),
                ],
                'edges': [
                    ("Sydney", "Melbourne", 706.1),
                    ("Sydney", "Brisbane", 752.9),
                    ("Sydney", "Perth", 3277.7),
                    ("Sydney", "Adelaide", 1164.5),
                    ("Sydney", "Canberra", 236.2),
                    ("Sydney", "Hobart", 1038.6),
                    ("Sydney", "Darwin", 3155.1),
                    ("Melbourne", "Brisbane", 1380.9),
                    ("Melbourne", "Perth", 2699.5),
                    ("Melbourne", "Adelaide", 640.1),
                    ("Melbourne", "Canberra", 470.3),
                    ("Melbourne", "Hobart", 618.0),
                    ("Melbourne", "Darwin", 3131.2),
                    ("Brisbane", "Perth", 3608.0),
                    ("Brisbane", "Adelaide", 1620.2),
                    ("Brisbane", "Canberra", 955.8),
                    ("Brisbane", "Hobart", 1791.2),
                    ("Brisbane", "Darwin", 2851.0),
                    ("Perth", "Adelaide", 2115.5),
                    ("Perth", "Canberra", 3084.9),
                    ("Perth", "Hobart", 3015.5),
                    ("Perth", "Darwin", 2653.1),
                    ("Adelaide", "Canberra", 970.1),
                    ("Adelaide", "Hobart", 1170.3),
                    ("Adelaide", "Darwin", 2621.5),
                    ("Canberra", "Hobart", 850.2),
                    ("Canberra", "Darwin", 3141.4),
                    ("Hobart", "Darwin", 3742.5),
                ]
            },
            'South American Capitals': {   # great-circle distances (Haversine) between the main international airports, km
                'directed': False,
                'coords': [
                    (-34.603684, -58.381559, 1.0, "Buenos Aires, Argentina"),
                    (-33.448890, -70.669265, 1.0, "Santiago, Chile"),
                    (-15.793889, -47.882778, 1.0, "Brasília, Brazil"),
                    (-12.046374, -77.042793, 1.0, "Lima, Peru"),
                    (-0.180653, -78.467834, 1.0, "Quito, Ecuador"),
                    (-16.489689, -68.119293, 1.0, "La Paz, Bolivia"),
                    (4.710989, -74.072092, 1.0, "Bogotá, Colombia"),
                    (-25.263740, -57.575926, 1.0, "Asunción, Paraguay"),
                ],
                'edges': [
                    ("Buenos Aires, Argentina", "Santiago, Chile", 1137.6),
                    ("Buenos Aires, Argentina", "Brasília, Brazil", 2358.4),
                    ("Buenos Aires, Argentina", "Lima, Peru", 3152.4),
                    ("Buenos Aires, Argentina", "Quito, Ecuador", 4372.1),
                    ("Buenos Aires, Argentina", "La Paz, Bolivia", 2250.1),
                    ("Buenos Aires, Argentina", "Bogotá, Colombia", 4688.0),
                    ("Buenos Aires, Argentina", "Asunción, Paraguay", 1070.0),
                    ("Santiago, Chile", "Brasília, Brazil", 3010.1),
                    ("Santiago, Chile", "Lima, Peru", 2461.8),
                    ("Santiago, Chile", "Quito, Ecuador", 3782.6),
                    ("Santiago, Chile", "La Paz, Bolivia", 1894.6),
                    ("Santiago, Chile", "Bogotá, Colombia", 4250.3),
                    ("Santiago, Chile", "Asunción, Paraguay", 1572.0),
                    ("Brasília, Brazil", "Lima, Peru", 3178.3),
                    ("Brasília, Brazil", "Quito, Ecuador", 3771.8),
                    ("Brasília, Brazil", "La Paz, Bolivia", 2165.7),
                    ("Brasília, Brazil", "Bogotá, Colombia", 3683.5),
                    ("Brasília, Brazil", "Asunción, Paraguay", 1442.4),
                    ("Lima, Peru", "Quito, Ecuador", 1329.7),
                    ("Lima, Peru", "La Paz, Bolivia", 1083.9),
                    ("Lima, Peru", "Bogotá, Colombia", 1888.2),
                    ("Lima, Peru", "Asunción, Paraguay", 2529.2),
                    ("Quito, Ecuador", "La Paz, Bolivia", 2136.2),
                    ("Quito, Ecuador", "Bogotá, Colombia", 712.0),
                    ("Quito, Ecuador", "Asunción, Paraguay", 3579.4),
                    ("La Paz, Bolivia", "Bogotá, Colombia", 2448.2),
                    ("La Paz, Bolivia", "Asunción, Paraguay", 1472.1),
                    ("Bogotá, Colombia", "Asunción, Paraguay", 3782.7),
                ]
            },
            "World's Tallest Buildings": {   # great-circle distances (Haversine) between the main international airports, km
                'directed': False,
                'coords': [
                    (25.197197, 55.274376, 1.0, "Burj Khalifa, Dubai"),
                    (31.235650, 121.501254, 1.0, "Shanghai Tower, China"),
                    (35.710054, 139.810714, 1.0, "Tokyo Skytree, Japan"),
                    (37.512554, 127.102679, 1.0, "Lotte World Tower, Seoul"),
                    (40.748817, -73.985428, 1.0, "Empire State Building, USA"),
                    (22.303379, 114.160226, 1.0, "International Commerce Centre, Hong Kong"),
                    (55.748330, 37.540740, 1.0, "Federation Tower, Moscow"),
                    (10.795085, 106.721914, 1.0, "Landmark 81, Vietnam"),
                ],
                'edges': [
                    ("Burj Khalifa, Dubai", "Shanghai Tower, China", 6448.2),
                    ("Burj Khalifa, Dubai", "Tokyo Skytree, Japan", 7934.4),
                    ("Burj Khalifa, Dubai", "Lotte World Tower, Seoul", 6728.1),
                    ("Burj Khalifa, Dubai", "Empire State Building, USA", 11001.5),
                    ("Burj Khalifa, Dubai", "International Commerce Centre, Hong Kong", 5919.6),
                    ("Burj Khalifa, Dubai", "Federation Tower, Moscow", 3711.9),
                    ("Burj Khalifa, Dubai", "Landmark 81, Vietnam", 5619.0),
                    ("Shanghai Tower, China", "Tokyo Skytree, Japan", 1736.8),
                    ("Shanghai Tower, China", "Lotte World Tower, Seoul", 821.6),
                    ("Shanghai Tower, China", "Empire State Building, USA", 11873.4),
                    ("Shanghai Tower, China", "International Commerce Centre, Hong Kong", 1255.1),
                    ("Shanghai Tower, China", "Federation Tower, Moscow", 6850.3),
                    ("Shanghai Tower, China", "Landmark 81, Vietnam", 2746.2),
                    ("Tokyo Skytree, Japan", "Lotte World Tower, Seoul", 1209.7),
                    ("Tokyo Skytree, Japan", "Empire State Building, USA", 10875.7),
                    ("Tokyo Skytree, Japan", "International Commerce Centre, Hong Kong", 2901.5),
                    ("Tokyo Skytree, Japan", "Federation Tower, Moscow", 7493.6),
                    ("Tokyo Skytree, Japan", "Landmark 81, Vietnam", 4323.3),
                    ("Lotte World Tower, Seoul", "Empire State Building, USA", 11089.3),
                    ("Lotte World Tower, Seoul", "International Commerce Centre, Hong Kong", 2068.3),
                    ("Lotte World Tower, Seoul", "Federation Tower, Moscow", 6585.0),
                    ("Lotte World Tower, Seoul", "Landmark 81, Vietnam", 3561.5),
                    ("Empire State Building, USA", "International Commerce Centre, Hong Kong", 12969.6),
                    ("Empire State Building, USA", "Federation Tower, Moscow", 7480.8),
                    ("Empire State Building, USA", "Landmark 81, Vietnam", 14292.7),
                    ("International Commerce Centre, Hong Kong", "Federation Tower, Moscow", 7136.4),
                    ("International Commerce Centre, Hong Kong", "Landmark 81, Vietnam", 1493.3),
                    ("Federation Tower, Moscow", "Landmark 81, Vietnam", 7726.5),
                ]
            },
            'Erasmus Partner Cities': {   # rail distances between the main stations (BRouter, rail profile), km;
                # Reykjavik and Aksaray: direct flights from their closest airport, great-circle distance between the airports, km
                'directed': False,
                'coords': [
                    (50.668000, 4.615000, 1.0, "Louvain-la-Neuve, Belgium"),
                    (50.467000, 4.867000, 1.0, "Namur, Belgium"),
                    (55.368000, 10.428000, 1.0, "Odense, Denmark"),
                    (59.396000, 24.664000, 1.0, "Tallinn, Estonia"),
                    (60.186000, 24.829000, 1.0, "Espoo/Helsinki, Finland"),
                    (61.449000, 23.858000, 1.0, "Hervanta, Finland"),
                    (61.065000, 28.097000, 1.0, "Lappeenranta, Finland"),
                    (61.485000, 21.797000, 1.0, "Pori, Finland"),
                    (63.106000, 21.595000, 1.0, "Vaasa, Finland"),
                    (43.923000, 2.148000, 1.0, "Albi, France"),
                    (45.188000, 5.724000, 1.0, "Grenoble, France"),
                    (45.764000, 4.835000, 1.0, "Lyon, France"),
                    (43.296000, 5.369000, 1.0, "Marseille, France"),
                    (43.611000, 3.877000, 1.0, "Montpellier, France"),
                    (48.692000, 6.184000, 1.0, "Nancy, France"),
                    (48.844000, 2.587000, 1.0, "Noisy-le-Grand/Paris, France"),
                    (48.713000, 2.208000, 1.0, "Palaiseau/Paris, France"),
                    (45.439000, 4.387000, 1.0, "Saint-Étienne, France"),
                    (48.584000, 7.750000, 1.0, "Strasbourg, France"),
                    (37.941000, 23.653000, 1.0, "Piraeus, Greece"),
                    (40.640000, 22.944000, 1.0, "Thessaloniki, Greece"),
                    (64.135000, -21.895000, 1.0, "Reykjavik, Iceland"),
                    (41.118000, 16.872000, 1.0, "Bari, Italy"),
                    (45.698000, 9.677000, 1.0, "Bergamo, Italy"),
                    (45.464000, 9.190000, 1.0, "Milan, Italy"),
                    (44.647000, 10.925000, 1.0, "Modena, Italy"),
                    (41.902000, 12.496000, 1.0, "Rome, Italy"),
                    (46.067000, 11.121000, 1.0, "Trento, Italy"),
                    (45.070000, 7.686000, 1.0, "Turin, Italy"),
                    (45.815000, 15.981000, 1.0, "Zagreb, Croatia"),
                    (54.898000, 23.903000, 1.0, "Kaunas, Lithuania"),
                    (49.611000, 6.131000, 1.0, "Luxembourg, Luxembourg"),
                    (52.002000, 4.377000, 1.0, "Delft, Netherlands"),
                    (51.441000, 5.469000, 1.0, "Eindhoven, Netherlands"),
                    (52.239000, 6.849000, 1.0, "Enschede, Netherlands"),
                    (63.430000, 10.395000, 1.0, "Trondheim, Norway"),
                    (46.624000, 14.307000, 1.0, "Klagenfurt, Austria"),
                    (51.107000, 17.038000, 1.0, "Wrocław, Poland"),
                    (51.759000, 19.456000, 1.0, "Łódź, Poland"),
                    (52.406000, 16.925000, 1.0, "Poznań, Poland"),
                    (41.550000, -8.421000, 1.0, "Braga/Guimarães, Portugal"),
                    (38.736000, -9.139000, 1.0, "Lisbon, Portugal"),
                    (41.149000, -8.611000, 1.0, "Porto, Portugal"),
                    (58.410000, 15.621000, 1.0, "Linköping, Sweden"),
                    (65.584000, 22.156000, 1.0, "Luleå, Sweden"),
                    (55.705000, 13.193000, 1.0, "Lund, Sweden"),
                    (59.329000, 18.068000, 1.0, "Stockholm, Sweden"),
                    (47.498000, 8.724000, 1.0, "Winterthur, Switzerland"),
                    (43.362000, -8.411000, 1.0, "A Coruña, Spain"),
                    (41.385000, 2.173000, 1.0, "Barcelona, Spain"),
                    (43.263000, -2.935000, 1.0, "Bilbao, Spain"),
                    (36.527000, -6.292000, 1.0, "Cádiz, Spain"),
                    (40.416000, -3.703000, 1.0, "Madrid, Spain"),
                    (40.964000, -5.663000, 1.0, "Salamanca, Spain"),
                    (49.195000, 16.607000, 1.0, "Brno, Czech Republic"),
                    (50.075000, 14.437000, 1.0, "Prague, Czech Republic"),
                    (38.368000, 33.998000, 1.0, "Aksaray, Turkey"),
                    (41.008000, 28.978000, 1.0, "Istanbul, Turkey"),
                    (47.497000, 19.040000, 1.0, "Budapest, Hungary"),
                ],
                'edges': [
                    ("Louvain-la-Neuve, Belgium", "Namur, Belgium", 34.0),
                    ("Louvain-la-Neuve, Belgium", "Eindhoven, Netherlands", 179.8),
                    ("Namur, Belgium", "Noisy-le-Grand/Paris, France", 323.2),
                    ("Namur, Belgium", "Luxembourg, Luxembourg", 164.9),
                    ("Odense, Denmark", "Enschede, Netherlands", 667.5),
                    ("Odense, Denmark", "Lund, Sweden", 209.0),
                    ("Tallinn, Estonia", "Espoo/Helsinki, Finland", 800.0),
                    ("Tallinn, Estonia", "Kaunas, Lithuania", 733.2),
                    ("Tallinn, Estonia", "Stockholm, Sweden", 2504.4),
                    ("Espoo/Helsinki, Finland", "Hervanta, Finland", 186.9),
                    ("Espoo/Helsinki, Finland", "Lappeenranta, Finland", 251.5),
                    ("Hervanta, Finland", "Lappeenranta, Finland", 320.4),
                    ("Hervanta, Finland", "Pori, Finland", 132.6),
                    ("Pori, Finland", "Vaasa, Finland", 355.7),
                    ("Pori, Finland", "Stockholm, Sweden", 1927.9),
                    ("Vaasa, Finland", "Trondheim, Norway", 1659.9),
                    ("Vaasa, Finland", "Luleå, Sweden", 737.6),
                    ("Albi, France", "Montpellier, France", 321.6),
                    ("Albi, France", "Saint-Étienne, France", 460.1),
                    ("Albi, France", "Barcelona, Spain", 469.8),
                    ("Albi, France", "Bilbao, Spain", 711.2),
                    ("Grenoble, France", "Lyon, France", 131.4),
                    ("Grenoble, France", "Marseille, France", 297.4),
                    ("Grenoble, France", "Montpellier, France", 299.6),
                    ("Grenoble, France", "Turin, Italy", 243.5),
                    ("Lyon, France", "Nancy, France", 413.0),
                    ("Lyon, France", "Noisy-le-Grand/Paris, France", 441.7),
                    ("Lyon, France", "Palaiseau/Paris, France", 433.3),
                    ("Lyon, France", "Saint-Étienne, France", 59.8),
                    ("Lyon, France", "Winterthur, Switzerland", 446.5),
                    ("Marseille, France", "Montpellier, France", 176.0),
                    ("Montpellier, France", "Saint-Étienne, France", 326.9),
                    ("Montpellier, France", "Barcelona, Spain", 346.5),
                    ("Nancy, France", "Noisy-le-Grand/Paris, France", 349.3),
                    ("Nancy, France", "Strasbourg, France", 145.4),
                    ("Nancy, France", "Luxembourg, Luxembourg", 116.7),
                    ("Noisy-le-Grand/Paris, France", "Palaiseau/Paris, France", 42.3),
                    ("Noisy-le-Grand/Paris, France", "Luxembourg, Luxembourg", 386.4),
                    ("Strasbourg, France", "Winterthur, Switzerland", 222.8),
                    ("Strasbourg, France", "Prague, Czech Republic", 673.3),
                    ("Piraeus, Greece", "Thessaloniki, Greece", 511.4),
                    ("Piraeus, Greece", "Istanbul, Turkey", 1310.1),
                    ("Thessaloniki, Greece", "Bari, Italy", 2287.5),
                    ("Thessaloniki, Greece", "Istanbul, Turkey", 813.9),
                    ("Thessaloniki, Greece", "Budapest, Hungary", 1008.4),
                    ("Reykjavik, Iceland", "Louvain-la-Neuve, Belgium", 2148.9),
                    ("Reykjavik, Iceland", "Espoo/Helsinki, Finland", 2444.3),
                    ("Reykjavik, Iceland", "Lyon, France", 2653.4),
                    ("Reykjavik, Iceland", "Noisy-le-Grand/Paris, France", 2243.3),
                    ("Reykjavik, Iceland", "Palaiseau/Paris, France", 2261.3),
                    ("Reykjavik, Iceland", "Milan, Italy", 2809.0),
                    ("Reykjavik, Iceland", "Rome, Italy", 3317.9),
                    ("Reykjavik, Iceland", "Delft, Netherlands", 2036.0),
                    ("Reykjavik, Iceland", "Wrocław, Poland", 2694.5),
                    ("Reykjavik, Iceland", "Lisbon, Portugal", 2940.6),
                    ("Reykjavik, Iceland", "Lund, Sweden", 2145.3),
                    ("Reykjavik, Iceland", "Stockholm, Sweden", 2144.7),
                    ("Reykjavik, Iceland", "Winterthur, Switzerland", 2631.9),
                    ("Reykjavik, Iceland", "Barcelona, Spain", 2981.9),
                    ("Reykjavik, Iceland", "Madrid, Spain", 2890.1),
                    ("Reykjavik, Iceland", "Prague, Czech Republic", 2654.6),
                    ("Reykjavik, Iceland", "Istanbul, Turkey", 4113.8),
                    ("Reykjavik, Iceland", "Budapest, Hungary", 3115.7),
                    ("Bari, Italy", "Rome, Italy", 475.7),
                    ("Bari, Italy", "Zagreb, Croatia", 1218.0),
                    ("Bergamo, Italy", "Milan, Italy", 53.3),
                    ("Bergamo, Italy", "Modena, Italy", 192.3),
                    ("Bergamo, Italy", "Trento, Italy", 199.0),
                    ("Bergamo, Italy", "Winterthur, Switzerland", 328.6),
                    ("Milan, Italy", "Turin, Italy", 143.3),
                    ("Modena, Italy", "Rome, Italy", 387.2),
                    ("Modena, Italy", "Trento, Italy", 183.9),
                    ("Rome, Italy", "Zagreb, Croatia", 957.7),
                    ("Trento, Italy", "Klagenfurt, Austria", 351.2),
                    ("Trento, Italy", "Winterthur, Switzerland", 458.7),
                    ("Zagreb, Croatia", "Klagenfurt, Austria", 248.3),
                    ("Zagreb, Croatia", "Budapest, Hungary", 358.4),
                    ("Kaunas, Lithuania", "Łódź, Poland", 593.8),
                    ("Kaunas, Lithuania", "Lund, Sweden", 1564.8),
                    ("Delft, Netherlands", "Eindhoven, Netherlands", 118.4),
                    ("Eindhoven, Netherlands", "Enschede, Netherlands", 177.0),
                    ("Enschede, Netherlands", "Prague, Czech Republic", 788.9),
                    ("Trondheim, Norway", "Linköping, Sweden", 887.6),
                    ("Trondheim, Norway", "Luleå, Sweden", 993.0),
                    ("Trondheim, Norway", "Stockholm, Sweden", 804.8),
                    ("Klagenfurt, Austria", "Brno, Czech Republic", 474.1),
                    ("Wrocław, Poland", "Łódź, Poland", 254.1),
                    ("Wrocław, Poland", "Poznań, Poland", 164.5),
                    ("Wrocław, Poland", "Brno, Czech Republic", 272.8),
                    ("Wrocław, Poland", "Prague, Czech Republic", 310.7),
                    ("Łódź, Poland", "Poznań, Poland", 251.0),
                    ("Poznań, Poland", "Lund, Sweden", 1046.1),
                    ("Braga/Guimarães, Portugal", "Porto, Portugal", 53.4),
                    ("Braga/Guimarães, Portugal", "A Coruña, Spain", 283.9),
                    ("Braga/Guimarães, Portugal", "Salamanca, Spain", 479.7),
                    ("Lisbon, Portugal", "Porto, Portugal", 329.9),
                    ("Lisbon, Portugal", "Cádiz, Spain", 699.3),
                    ("Linköping, Sweden", "Lund, Sweden", 372.4),
                    ("Linköping, Sweden", "Stockholm, Sweden", 208.5),
                    ("Winterthur, Switzerland", "Prague, Czech Republic", 686.2),
                    ("A Coruña, Spain", "Bilbao, Spain", 814.5),
                    ("Barcelona, Spain", "Bilbao, Spain", 642.0),
                    ("Barcelona, Spain", "Madrid, Spain", 650.2),
                    ("Bilbao, Spain", "Madrid, Spain", 544.9),
                    ("Bilbao, Spain", "Salamanca, Spain", 431.6),
                    ("Cádiz, Spain", "Madrid, Spain", 668.2),
                    ("Cádiz, Spain", "Salamanca, Spain", 858.9),
                    ("Madrid, Spain", "Salamanca, Spain", 268.4),
                    ("Brno, Czech Republic", "Prague, Czech Republic", 253.4),
                    ("Brno, Czech Republic", "Budapest, Hungary", 344.7),
                    ("Aksaray, Turkey", "Istanbul, Turkey", 503.9),
                ]
            }
        }
        for problem in problems.values():
            if "edges" in problem:
                problem["matrix"] = NetworkProblemRepository._matrix(problem["coords"], problem.pop("edges"))
        return problems

    @staticmethod
    def _matrix(coords, edges):
        """Length matrix (None: no edge) of an undirected network given as edges (name, name, length)."""
        index = {coord[3]: k for k, coord in enumerate(coords)}
        matrix = [[None] * len(coords) for _ in coords]
        for a, b, length in edges:
            matrix[index[a]][index[b]] = matrix[index[b]][index[a]] = length
        return matrix
