import numpy
from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge
from multivitamin.basic.graph import Graph
from itertools import chain


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
        def t2node(t):
            i, ls = t
            return Node(str(i), ls)
        # Create multivitamin nodes with label and index as id
        nodes = list(
            map(t2node, zip(range(0, len(self.node_labels)), self.node_labels)))

        # Indices for each adjecency matrix column
        indices = range(0, self.adj_matrix.shape[1])
        # Use the adjecency matrix row as selector for the indices
        def r2edges(r): return [ i for mask, i in zip(r, indices) if mask ]
        # list of lists of connected node ids at node index
        nodei_2_index = map(r2edges, self.adj_matrix)

        def r2labels(r): return [ s for s in r if s ]
        # list of lists of labels at node index
        nodei_2_label = map(r2labels, self.edge_labels)

        # Put labels to respective node indices
        nodei_2_index_label = map(lambda t: zip(
            t[0], t[1]), zip(nodei_2_index, nodei_2_label))

        def mappingt2edgest(t):
            i, node_ilts = t
            from_node = nodes[i]

            def ilt2edge(t):
                index, label = t
                return Edge(from_node, nodes[int(index)], label)
            return (from_node, list(map(ilt2edge, node_ilts)))
        # map from node to edges involving node
        node_2_edges = dict(
            map(mappingt2edgest, zip(indices, nodei_2_index_label)))
        for node, edges in node_2_edges.items():
            # Save node2 as neighbor as node (which is key) was used as node1 in
            # constructor above
            node.neighbours = set(map(lambda e: e.node2, edges))

        return Graph(id=self.id, nodes=set(node_2_edges.keys()),
                     edges=set(chain.from_iterable(node_2_edges.values())),
                     nodes_labelled=True, edges_labelled=True,
                     is_directed=False)
