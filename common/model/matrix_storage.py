# common/model/matrix_storage.py

import networkx as nx
import numpy as np

class MatrixStorage:
    """
    A model class for storing and managing a network's adjacency matrix.
    This class allows setting, retrieving, and clearing the matrix along with its dimensions.
    It also provides utility methods to create an initial matrix and to convert the matrix into a graph.
    """

    def __init__(self):
        # Initialize with an empty matrix and zero nodes.
        self.matrix = []
        self.num_nodes = 0
        self.graph = None
        self.pos = None
        self.weights = []
        self.directed = False
    
    def set_directed(self, directed):
        self.directed = directed
    
    def is_directed(self):
        return self.directed

    def get_weights(self):
        return self.weights
    
    def set_weights(self, weights):
        self.weights = weights

    def complete_weights(self, raw_weights):
        parsed_weights = []
        has_numeric_weight = False

        for value in raw_weights:
            if value is None or str(value).strip() == "":
                parsed_weights.append(None)
            else:
                weight = float(value)
                parsed_weights.append(weight)
                has_numeric_weight = True

        if has_numeric_weight:
            return [w if w is not None else 0 for w in parsed_weights]
        else:
            return [1 for _ in parsed_weights]

    def set_matrix(self, matrix, num_nodes):
        """
        Store the adjacency matrix and its dimension.

        :param matrix: A list of lists representing the matrix.
        :param num_nodes: An integer representing the number of nodes.
        """
        self.matrix = matrix
        self.num_nodes = num_nodes

    def get_matrix(self):
        """
        Retrieve the stored adjacency matrix.

        :return: A tuple (matrix, num_nodes)
        """
        return self.matrix, self.num_nodes

    def clear_matrix(self):
        """
        Clears the stored matrix, its graph and its layout, and resets the node count.
        """
        self.matrix = []
        self.num_nodes = 0
        self.graph = None
        self.pos = None

    def create_matrix(self, node_count):
        """
        Creates an adjacency matrix with the given node count.
        The diagonal elements are filled with "n" (indicating no self-connection),
        and all off-diagonal elements are set to None.

        :param node_count: The number of nodes (int).
        :return: The created matrix (list of lists) and the node count.
        """
        matrix = []
        for i in range(node_count):
            row = []
            for j in range(node_count):
                if i == j:
                    row.append("n")  # Use "n" to indicate no self-connection
                else:
                    row.append(None)
            matrix.append(row)
        # Save the matrix and node count internally
        self.set_matrix(matrix, node_count)
        return matrix, node_count
    
    def matrix_in_graph(self):
        """
        Converts the stored adjacency matrix into a directed graph.
        Each non-None, non-"n" value in the stored matrix creates an edge with that weight.

        :return: A networkx Grapf or Digraph instance.
        """
        graph = nx.DiGraph() if self.directed else nx.Graph()
        for i in range(self.num_nodes):
            if (
                len(self.weights) > 0
                and isinstance(self.weights[0], (list, tuple, np.ndarray))
            ):
                # Mehrere Gewichtsspalten
                node_weight = [
                    weight_column[i]
                    for weight_column in self.weights
                ]
            else:
                # Eine Gewichtsspalte
                node_weight = self.weights[i]
            graph.add_node(i + 1, weight=node_weight)
            
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.matrix[i][j] is not None and self.matrix[i][j] != "n":
                    # Nodes are labeled starting from 1.
                    graph.add_edge(i + 1, j + 1, weight=self.matrix[i][j])
        self.graph = graph
        self.pos = nx.spring_layout(graph)
        return graph
    
    def get_graph(self):
        return self.graph

    def get_pos(self):
        return self.pos

    def new_layout(self):
        """
        Computes a new layout of the stored graph; every later drawing of the graph uses it.
        """
        self.pos = nx.spring_layout(self.graph)
    
