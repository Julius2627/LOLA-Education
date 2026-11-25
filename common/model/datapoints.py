# common/model/datapoints.py
from common.model.problems_districting import DistrictingProblemRepository
from common.model.problems_dualoc import DualocProblemRepository
from common.model.problems_network import NetworkProblemRepository

# Datasets whose names start with these words are shown in the Education Mode (Facility Location and
# Graph Theory courses, further examples); the Applied Mode shows all datasets.
EDUCATION_PREFIXES = ("Fac. Loc.", "GT", "Further")


class Model:
    """
    A model class for storing and managing 2D data points with weights and optional names.

    Each point is a tuple in the form (x, y, weight, name). If weight or name is not provided,
    default values will be assigned.

    The model also holds a collection of predefined datasets ("bundles") stored in a dictionary.
    """

    def __init__(self):
        self.points = []  # List of currently active points (tuples of 4 values)
        self.datasets = {}  # Dictionary to hold named point bundles
        self.dualoc_problems = {}  # Holds predefined DUALOC problem datasets
        self.network_problems = {}  # Holds predefined network problems
        self.districting_problems = {}  # Holds predefined districting problems

        self.load_default_datasets()  # Load the predefined default bundles
        self.load_dualoc_problems()  # Load predefined DUALOC problems
        self.load_network_problems()  # Load predefined network problems
        self.load_districting_problems()  # Load predefined districting problems
    # --------------------------------------------------
    # Methods for managing individual data points
    # --------------------------------------------------

    def add_point(self, point):
        """
        Add a point to the internal point list.

        :param point: Tuple (x, y), (x, y, weight), or (x, y, weight, name)
        """
        default_name = f"Datapoint {len(self.points) + 1}"
        if len(point) == 2:
            x, y = point
            weight = 1
            self.points.append((x, y, weight, default_name))
        elif len(point) == 3:
            x, y, weight = point
            self.points.append((x, y, weight, default_name))
        elif len(point) >= 4:
            self.points.append(point[:4])  # Only keep first 4 elements
        else:
            raise ValueError("Point must be at least a tuple with (x, y)")

    def remove_all_points(self):
        """
        Clear the list of currently stored points.
        """
        self.points.clear()

    def get_points(self):
        """
        Get the list of all stored points.
        :return: List of tuples (x, y, weight, name)
        """
        return self.points

    def points_toString(self):
        """
        Format all points into a human-readable string with 2 decimal places.
        """
        return "\n".join([f"{x:.2f}, {y:.2f}, {w:.2f}, {name}" for x, y, w, name in self.points])

    # --------------------------------------------------
    # Methods for managing and accessing datasets
    # --------------------------------------------------

    def get_dataset(self, name):
        """
        Retrieve a dataset by name.
        :param name: Dataset key
        :return: List of points if found, otherwise None
        """
        return self.datasets.get(name)

    def list_datasets(self, education_only=False):
        """
        Get a list of the available dataset names.
        :param education_only: True for the datasets of the Education Mode only (see EDUCATION_PREFIXES)
        :return: List of dataset keys
        """
        return [name for name in self.datasets if not education_only or name.startswith(EDUCATION_PREFIXES)]

    def get_dualoc_problem(self, name):
        """
        Retrieve a predefined DUALOC problem by name.
        :param name: The name of the problem
        :return: Dictionary with 'c_ij_original' and 'f_j' or None
        """
        return self.dualoc_problems.get(name)

    def get_network_problem(self, name):
        """
        Retrieve a predefined network problem by name.
        :param name: The name of the problem
        :return: Dictionary with 'Behnhoefe' and 'Adjazenzmatrix' or None
        """
        return self.network_problems.get(name)

    def get_districting_problem(self, name):
        """
        Retrieve a predefined districting problem by name.
        :param name: The name of the problem
        :return: Dictionary with 'areas' [(x, y, w), ...], 'p', 'K', 'beta' and (optional) 'names', or None
        """
        return self.districting_problems.get(name)

    def list_districting_problems(self, education_only=False):
        """
        List the available districting problem names.
        :param education_only: True for the problems of the Education Mode only (see EDUCATION_PREFIXES)
        :return: List of strings
        """
        return [name for name in self.districting_problems if not education_only or name.startswith(EDUCATION_PREFIXES)]

    def list_dualoc_problems(self, education_only=False):
        """
        List the available DUALOC problem names.
        :param education_only: True for the problems of the Education Mode only (see EDUCATION_PREFIXES)
        :return: List of strings
        """
        return [name for name in self.dualoc_problems if not education_only or name.startswith(EDUCATION_PREFIXES)]
    
    def list_network_problems(self, directed=None, max_nodes=None, education_only=False):
      
        """
        List available network problem names.
        If directed is True/False, only matching problems are returned.
        If directed is None, all problems are returned.
        If max_nodes is given, only problems with at most that many nodes are returned.
        If education_only is True, only the problems of the Education Mode are returned (see EDUCATION_PREFIXES).
        """
        return [
            name
            for name, problem in self.network_problems.items()
            if (directed is None or problem.get("directed") == directed)
            and (max_nodes is None or len(problem["matrix"]) <= max_nodes)
            and (not education_only or name.startswith(EDUCATION_PREFIXES))
        ]

    def load_default_datasets(self):
        """
        Load built-in sample datasets into the model.
        These are mainly example or geographic datasets.
        """
        self.datasets = {
            "Fac. Loc. Lecture Example 1": [
                (1, 4, 2.0, "a1"),
                (2, 6, 3.0, "a2"),
                (5, 1, 1.0, "a3"),
                (4, 2, 1.0, "a4"),
                (6, 5, 2.0, "a5")
            ],
            "Fac. Loc. Lecture Example 2": [
                (1, 4, 1.0, "a1"),
                (2, 6, 1.0, "a2"),
                (5, 1, 1.0, "a3"),
                (4, 2, 1.0, "a4"),
                (8, 5, 1.0, "a5")
            ],
            "Fac. Loc. Lecture Example 3": [
                (1, 1, 1.0, "a1"),
                (2, 5, 1.0, "a2"),
                (3, 3, 1.0, "a3"),
                (4, 2, 1.0, "a4")
            ],
            "Further Example 1": [
                (1, 2, 1.0, "Point 1"),
                (2, 3, 1.0, "Point 2"),
                (3, 1, 1.0, "Point 3"),
                (4, 4, 1.0, "Point 4")
            ],
            "Further Example 2": [
                (1.5, 1.5, 1.0, "Point 1"),
                (2.5, 2.5, 1.0, "Point 2"),
                (3.5, 3.5, 1.0, "Point 3")
            ],
            "Fac. Loc. Exercise 7":[
                (6, 5, 2, "Bakery"),
                (10, 3, 1, "Greengrocer"),
                (12, 7, 1, "Apparel Store"),
                (10, 7, 0.5, "Hairdresser" )
            ],
            "Fac. Loc. Exercise 8":[
                (18,2,6.0,"Automotive Plant 1"),
                (4,0,2.0,"Automotive Plant 2"),
                (6,20,7.0,"Automotive Plant 3"),
                (12,18,4.0,"Automotive Plant 4")
            ],
            "Fac. Loc. Exercise 9":[
               (4,12,4.0, "Area 1"),
               (8,2,2.0, "Area 2"),
               (14,10,2.0, "Area 3"), 
               (2,3,8.0, "Area 4"),
               (14,4,9.0, "Area 5")
            ],
            "Fac. Loc. Exercise 10":[
                (5,10,1.0, "Hospital 1"),
                (7,6,1.0, "Hospital 2"),
                (4,2,1.0, "Hospital 3"),
                (10,4,1.0, "Hospital 4")
            ],
            "Fac. Loc. Exercise 11a-1":[
                (5,2,3.0, "P1"),
                (8,5,5.0, "P2"),
                #(3,7,0.0, "P3"),
                (1,2,2.0, "H")
            ],
            "Fac. Loc. Exercise 11a-2":[
                (5,2,2.0, "P1"),
                #(8,5,0.0, "P2"),
                (3,7,5.0, "P3"),
                (1,2,2.0, "H")
            ],
            "KIT Campus": [
                (49.011556, 8.416286, 1.0, "KIT Library"),
                (49.014810, 8.420493, 1.0, "Lecture Hall Fasanengarten"),
                (49.012909, 8.415479, 1.0, "Audimax"),
                (49.011915, 8.417309, 1.0, "Dining Hall"),
                (49.009456, 8.414187, 1.0, "Mechanical Engineering Building"),
                (49.011428, 8.413905, 1.0, "Chemistry Building"),
                (48.993192, 8.401711, 1.0, "Karlsruhe Central Station"),
                (49.013525, 8.404359, 1.0, "Karlsruhe Palace")
            ],
            "Karlsruhe Bars": [
                (49.005440, 8.411916, 1.0, "Agostea Nightclub"),
                (49.004029, 8.404239, 1.0, "Die Stadtmitte"),
                (49.008894, 8.403844, 1.0, "Café Emaille"),
                (49.011650, 8.395029, 1.0, "Scruffy's Irish Pub"),
                (49.013893, 8.357782, 1.0, "Vanguarde"),
                (49.008519, 8.395981, 1.0, "La Cage"),
                (49.008638, 8.395750, 1.0, "Enchilada Karlsruhe"),
                (49.007621, 8.414519, 1.0, "Old Chapel Pub")
            ],
            "Silicon Valley": [
                (37.422004, -122.084075, 1.0, "Google HQ"),
                (37.334835, -122.011392, 1.0, "Apple HQ"),
                (37.484722, -122.148333, 1.0, "Meta HQ"),
                (37.427489, -122.171786, 1.0, "Stanford University"),
                (37.774930, -122.419420, 1.0, "San Francisco"),
                (37.338208, -121.886329, 1.0, "San Jose"),
                (37.871593, -122.272743, 1.0, "Berkeley"),
                (37.804364, -122.271114, 1.0, "Oakland")
            ],
            "Berlin Landmarks": [
                (52.516270, 13.377703, 1.0, "Brandenburg Gate"),
                (52.518654, 13.376102, 1.0, "Reichstag Building"),
                (52.520645, 13.409779, 1.0, "TV Tower"),
                (52.504454, 13.440839, 1.0, "East Side Gallery"),
                (52.500250, 13.308714, 1.0, "Kurfürstendamm"),
                (52.488444, 13.470315, 1.0, "Treptower Park"),
                (52.509649, 13.376168, 1.0, "Potsdamer Platz"),
                (52.522681, 13.402342, 1.0, "Hackescher Markt")
            ],
            "London Landmarks": [
                (51.500729, -0.124625, 1.0, "Big Ben"),
                (51.507351, -0.127758, 1.0, "Trafalgar Square"),
                (51.504365, -0.086474, 1.0, "The Shard"),
                (51.503324, -0.119543, 1.0, "London Eye"),
                (51.505456, -0.075356, 1.0, "Tower Bridge"),
                (51.513787, -0.098451, 1.0, "St. Paul's Cathedral"),
                (51.518769, -0.126409, 1.0, "British Museum"),
                (51.530133, -0.153764, 1.0, "Regent's Park")
            ],
            "Munich Beer Gardens": [
                (48.137633, 11.579979, 1.0, "Hofbräuhaus"),
                (48.143503, 11.551566, 1.0, "Augustiner-Keller"),
                (48.139206, 11.545647, 1.0, "Augustiner Bräustuben"),
                (48.126042, 11.559521, 1.0, "Paulaner Bräuhaus"),
                (48.160516, 11.598326, 1.0, "Seehaus (English Garden)"),
                (48.135109, 11.575537, 1.0, "Viktualienmarkt Beer Garden"),
                (48.148114, 11.558320, 1.0, "Löwenbräukeller"),
                (48.152552, 11.592097, 1.0, "Chinese Tower")
            ],
            "Tokyo Landmarks": [
                (35.658581, 139.745438, 1.0, "Tokyo Tower"),
                (35.685072, 139.709547, 1.0, "Shinjuku Gyoen"),
                (35.713403, 139.795526, 1.0, "Senso-ji Temple"),
                (35.676397, 139.699326, 1.0, "Meiji Shrine"),
                (35.658034, 139.701636, 1.0, "Shibuya Crossing"),
                (35.699593, 139.774219, 1.0, "Akihabara"),
                (35.670502, 139.702414, 1.0, "Harajuku"),
                (35.671170, 139.766249, 1.0, "Ginza")
            ],
            "European Capitals": [
                (48.856614, 2.352222, 1.0, "Paris, France"),
                (51.507351, -0.127758, 1.0, "London, UK"),
                (52.520007, 13.404954, 1.0, "Berlin, Germany"),
                (41.902784, 12.496366, 1.0, "Rome, Italy"),
                (40.416775, -3.703790, 1.0, "Madrid, Spain"),
                (48.208174, 16.373819, 1.0, "Vienna, Austria"),
                (50.075538, 14.437800, 1.0, "Prague, Czechia"),
                (59.329323, 18.068581, 1.0, "Stockholm, Sweden"),
                (60.169856, 24.938379, 1.0, "Helsinki, Finland"),
                (55.755826, 37.617300, 1.0, "Moscow, Russia")
            ],
            "World Cities": [
                (34.052235, -118.243683, 1.0, "Los Angeles, USA"),
                (35.689487, 139.691706, 1.0, "Tokyo, Japan"),
                (40.712776, -74.005974, 1.0, "New York City, USA"),
                (19.432608, -99.133209, 1.0, "Mexico City, Mexico"),
                (28.613939, 77.209023, 1.0, "Delhi, India"),
                (31.230416, 121.473701, 1.0, "Shanghai, China"),
                (1.352083, 103.819836, 1.0, "Singapore"),
                (55.755826, 37.617300, 1.0, "Moscow, Russia")
            ],
            "Great Lakes": [
                (43.653226, -79.383184, 1.0, "Toronto, Canada"),
                (41.878114, -87.629798, 1.0, "Chicago, USA"),
                (42.331427, -83.045754, 1.0, "Detroit, USA"),
                (43.038902, -87.906474, 1.0, "Milwaukee, USA"),
                (45.501689, -73.567256, 1.0, "Montreal, Canada"),
                (46.813878, -71.207981, 1.0, "Quebec City, Canada"),
                (46.783829, -92.105268, 1.0, "Duluth, USA"),
                (41.499321, -81.694361, 1.0, "Cleveland, USA")
            ],
            "Australian Cities": [
                (-33.868820, 151.209296, 1.0, "Sydney"),
                (-37.813628, 144.963058, 1.0, "Melbourne"),
                (-27.469771, 153.025124, 1.0, "Brisbane"),
                (-31.950527, 115.860457, 1.0, "Perth"),
                (-34.928499, 138.600746, 1.0, "Adelaide"),
                (-35.280937, 149.130009, 1.0, "Canberra"),
                (-42.882138, 147.327195, 1.0, "Hobart"),
                (-12.463440, 130.845642, 1.0, "Darwin")
            ],
            "South American Capitals": [
                (-34.603684, -58.381559, 1.0, "Buenos Aires, Argentina"),
                (-33.448890, -70.669265, 1.0, "Santiago, Chile"),
                (-15.793889, -47.882778, 1.0, "Brasília, Brazil"),
                (-12.046374, -77.042793, 1.0, "Lima, Peru"),
                (-0.180653, -78.467834, 1.0, "Quito, Ecuador"),
                (-16.489689, -68.119293, 1.0, "La Paz, Bolivia"),
                (4.710989, -74.072092, 1.0, "Bogotá, Colombia"),
                (-25.263740, -57.575926, 1.0, "Asunción, Paraguay")
            ],
            "World's Tallest Buildings": [
                (25.197197, 55.274376, 1.0, "Burj Khalifa, Dubai"),
                (31.235650, 121.501254, 1.0, "Shanghai Tower, China"),
                (35.710054, 139.810714, 1.0, "Tokyo Skytree, Japan"),
                (37.512554, 127.102679, 1.0, "Lotte World Tower, Seoul"),
                (40.748817, -73.985428, 1.0, "Empire State Building, USA"),
                (22.303379, 114.160226, 1.0, "International Commerce Centre, Hong Kong"),
                (55.748330, 37.540740, 1.0, "Federation Tower, Moscow"),
                (10.795085, 106.721914, 1.0, "Landmark 81, Vietnam")
            ],
            "Erasmus Partner Cities": [
                (50.668, 4.615, 1.0, "Louvain-la-Neuve, Belgium"),
                (50.467, 4.867, 1.0, "Namur, Belgium"),
                (55.368, 10.428, 1.0, "Odense, Denmark"),
                (59.396, 24.664, 1.0, "Tallinn, Estonia"),
                (60.186, 24.829, 1.0, "Espoo/Helsinki, Finland"),
                (61.449, 23.858, 1.0, "Hervanta, Finland"),
                (61.065, 28.097, 1.0, "Lappeenranta, Finland"),
                (61.485, 21.797, 1.0, "Pori, Finland"),
                (63.106, 21.595, 1.0, "Vaasa, Finland"),
                (43.923, 2.148, 1.0, "Albi, France"),
                (45.188, 5.724, 1.0, "Grenoble, France"),
                (45.764, 4.835, 1.0, "Lyon, France"),
                (43.296, 5.369, 1.0, "Marseille, France"),
                (43.611, 3.877, 1.0, "Montpellier, France"),
                (48.692, 6.184, 1.0, "Nancy, France"),
                (48.844, 2.587, 1.0, "Noisy-le-Grand/Paris, France"),
                (48.713, 2.208, 1.0, "Palaiseau/Paris, France"),
                (45.439, 4.387, 1.0, "Saint-Étienne, France"),
                (48.584, 7.750, 1.0, "Strasbourg, France"),
                (37.941, 23.653, 1.0, "Piraeus, Greece"),
                (40.640, 22.944, 1.0, "Thessaloniki, Greece"),
                (64.135, -21.895, 1.0, "Reykjavik, Iceland"),
                (41.118, 16.872, 1.0, "Bari, Italy"),
                (45.698, 9.677, 1.0, "Bergamo, Italy"),
                (45.464, 9.190, 1.0, "Milan, Italy"),
                (44.647, 10.925, 1.0, "Modena, Italy"),
                (41.902, 12.496, 1.0, "Rome, Italy"),
                (46.067, 11.121, 1.0, "Trento, Italy"),
                (45.070, 7.686, 1.0, "Turin, Italy"),
                (45.815, 15.981, 1.0, "Zagreb, Croatia"),
                (54.898, 23.903, 1.0, "Kaunas, Lithuania"),
                (49.611, 6.131, 1.0, "Luxembourg, Luxembourg"),
                (52.002, 4.377, 1.0, "Delft, Netherlands"),
                (51.441, 5.469, 1.0, "Eindhoven, Netherlands"),
                (52.239, 6.849, 1.0, "Enschede, Netherlands"),
                (63.430, 10.395, 1.0, "Trondheim, Norway"),
                (46.624, 14.307, 1.0, "Klagenfurt, Austria"),
                (51.107, 17.038, 1.0, "Wrocław, Poland"),
                (51.759, 19.456, 1.0, "Łódź, Poland"),
                (52.406, 16.925, 1.0, "Poznań, Poland"),
                (41.550, -8.421, 1.0, "Braga/Guimarães, Portugal"),
                (38.736, -9.139, 1.0, "Lisbon, Portugal"),
                (41.149, -8.611, 1.0, "Porto, Portugal"),
                (58.410, 15.621, 1.0, "Linköping, Sweden"),
                (65.584, 22.156, 1.0, "Luleå, Sweden"),
                (55.705, 13.193, 1.0, "Lund, Sweden"),
                (59.329, 18.068, 1.0, "Stockholm, Sweden"),
                (47.498, 8.724, 1.0, "Winterthur, Switzerland"),
                (43.362, -8.411, 1.0, "A Coruña, Spain"),
                (41.385, 2.173, 1.0, "Barcelona, Spain"),
                (43.263, -2.935, 1.0, "Bilbao, Spain"),
                (36.527, -6.292, 1.0, "Cádiz, Spain"),
                (40.416, -3.703, 1.0, "Madrid, Spain"),
                (40.964, -5.663, 1.0, "Salamanca, Spain"),
                (49.195, 16.607, 1.0, "Brno, Czech Republic"),
                (50.075, 14.437, 1.0, "Prague, Czech Republic"),
                (38.368, 33.998, 1.0, "Aksaray, Turkey"),
                (41.008, 28.978, 1.0, "Istanbul, Turkey"),
                (47.497, 19.040, 1.0, "Budapest, Hungary")
            ]
        }

    def load_dualoc_problems(self):
        """
        Load predefined DUALOC problems from the repository.
        """
        self.dualoc_problems = DualocProblemRepository.get_predefined_problems()

    def load_network_problems(self):
        """
        Load predefined DUALOC problems from the repository.
        """
        self.network_problems = NetworkProblemRepository.get_predefined_problems()

    def load_districting_problems(self):
        """
        Load predefined districting problems from the repository.
        """
        self.districting_problems = DistrictingProblemRepository.get_predefined_problems()
