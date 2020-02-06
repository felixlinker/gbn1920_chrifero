import numpy
from multivitamin.basic.node import Node


class AdjacencyGraph:
    def __init__(self, graph=None, gid=None, matrix=None, edge_labels=None, node_labels=None):
        if graph:
            self.__from_multivitamin(graph)
        elif matrix and edge_labels and node_labels:
            self.id = gid
            self.adj_matrix = matrix
            self.edge_labels = edge_labels
            self.node_labels = node_labels
        else:
            raise ValueError('not enough arguments')

    def __from_multivitamin(self, graph):
        # Nodes and edges actually are sets; convert them to list here such that
        # the order of iteration is fixed
        self.id = graph.id
        nodes = list(graph.nodes)
        edges = list(graph.edges)
        shape = (len(nodes), len(nodes))
        self.adj_matrix = numpy.zeros(shape)
        self.edge_labels = numpy.full(shape, '')
        self.node_labels = list(map(lambda n: n.get_label(), nodes))

        node_indices = dict(zip(nodes, range(0, len(nodes))))
        for edge in edges:
            i1 = node_indices[edge.node1]
            i2 = node_indices[edge.node2]
            self.adj_matrix[i1][i2] = 1
            self.edge_labels[i1][i2] = edge.label

        # Make matrices symmetric; they might already be symmetric so check if
        # a value is present before taking it from the transposed matrix
        for i, v in numpy.ndenumerate(self.adj_matrix):
            self.adj_matrix[i] = v or self.adj_matrix.T[i]
        for i, v in numpy.ndenumerate(self.edge_labels):
            self.edge_labels[i] = v or self.edge_labels.T[i]

    def decompose(self):
        pass

    def remove_node(self, node_index):
        pass

    def to_multivitamin(self):
        pass
