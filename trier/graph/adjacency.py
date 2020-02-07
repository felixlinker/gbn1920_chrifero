import numpy
from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge
from multivitamin.basic.graph import Graph
from itertools import chain
from enum import Enum
from scipy.sparse.csgraph import dijkstra


__map_is_reachable = numpy.vectorize(lambda v: v < float('inf'))


def __split_reachability(sub_graph, parent):
    reachability_matrix = dijkstra(sub_graph.adjacency_matrix, directed=False)
    indexes = numpy.array(range(sub_graph.adjacency_matrix.shape[0]))
    reachables = map(lambda r: indexes * r,
                     __map_is_reachable(reachability_matrix))
    for i, reachables in enumerate(reachables):
        # Only consider every set of reachables once
        if reachables[0] <= i:
            continue
        new_matrix = numpy.zeros(sub_graph.adjacency_matrix.shape)
        for row in reachables:
            for col in reachables:
                new_matrix[row,col] = sub_graph.adjacency_matrix[row,col]
                yield SubGraph(parent, label=sub_graph.label)


class SubGraphLabel(Enum):
    CYCLE = 0
    TAIL = 1


class SubGraph:
    def __init__(self, parent, adjacency_matrix=None, label=None):
        self.parent = parent
        if adjacency_matrix and adjacency_matrix.shape != parent.adjacency_matrix.shape:
            raise ValueError("adjacency matrices must agree on shape")
        self.adjacency_matrix = adjacency_matrix if adjacency_matrix else numpy.zeros(
            parent.adjacency_matrix.shape)
        self.label = label


class AdjacencyGraph:
    def __init__(self, graph=None, gid=None, matrix=None, edge_labels=None, node_labels=None):
        self.sub_graphs = []
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
        self.cut_tails()
        self.split_cycles()
        return self.sub_graphs

    def cut_tails(self):
        '''
        First, size of search area will be reduced to identify cyclic structures:
        '''
        dec_matrix = self.adj_matrix
        del_adj_matrix = numpy.zeros_like(self.adj_matrix)
        is_trimmed = self.has_not_deg_one(dec_matrix)

        node_index_dict = {}
        '''
        for i in range(0, len(self.adj_matrix)):
            node_index_dict[i] = i
        '''
        while is_trimmed is not True:
            for i in range(0, len(dec_matrix[0])):
                if numpy.sum(self.adj_matrix[i], axis=0) == 1:
                    adj_pos = numpy.where(self.adj_matrix[i] == 1)[0]
                    del_adj_matrix[adj_pos[0]][i] = 1
                    del_adj_matrix[i][adj_pos[0]] = 1
                    self.adj_matrix[adj_pos[0]][i] = 0
                    self.adj_matrix[i][adj_pos[0]] = 0
                    #dec_matrix = self.remove_node(dec_matrix, node_index=i)
                    #node_index_dict = self.update_node_dict(node_index_dict, node_index=i)
                    break
            is_trimmed = self.has_not_deg_one(self.adj_matrix)
        return self.sub_graphs

    def get_tails(self):
        return filter(lambda sg: sg.label == SubGraphLabel.TAIL, self.sub_graphs)

    def __split_connected_subgraphs(self):
        # Split every subgraph into a set of strongly connected components
        splitted = [__split_reachability(sg, self) for sg in self.sub_graphs]
        # Merge the list of connected components
        self.sub_graphs = list(chain.from_iterable(splitted))

    def split_cycles(self):
        '''
        Finding cyclic paths:
        NOTE1: Unnoetig, wenn weniger als 5 Knoten.

        NOTE2: Die nodes nach Grad zu sortieren waere eine sinnvolle Ergaenzung

        NOTE3: Schlaueres Abbruchkriterium finden, auch wenn die tatsaechliche
        Anzahl an Operationen geringer ist als die Schleifen vermuten lassen.\

        NOTE4: Dictionary fuer urspruengliche node_indices.
        '''
        # print(dec_matrix)
        cycles = []
        assigned_nodes = []
        class_dict = {}
        dec_matrix = self.adj_matrix

        if len(dec_matrix[0]) > 5:

            for i in range(0, len(dec_matrix[0])):
                path_length = 1
                path_list = []
                new_path = []
                new_path.append(i)
                path_list.append(new_path)
                while path_length < 6:
                    path_index = len(path_list)-1

                    for p in range(0, len(path_list)):
                        path = path_list[p]
                        neighbors = self.get_adjacent_nodes(
                            dec_matrix, path[len(path)-1])
                        # print(neighbors)

                        for node in neighbors:
                            if node not in path or path[0] == node:
                                next_path = path
                                next_path.append(node)
                                path_list.append(next_path)
                                # print(next_path)

                                if path[0] == node:
                                    cycle_nodes = self.lookup(
                                        path, node_index_dict)

                                    if self.is_new_cycle(cycle_nodes, cycles):
                                        print("Cycle found: " +
                                              str(cycle_nodes))
                                        cycles.append(cycle_nodes)
                                        '''
                                        An sich sollte hier dann noch abgefragt werden ob der
                                        Cycle lang genug ist, aber vielleicht, faellt uns ja noch
                                        ein Nutzen fuer 4-Zyklen ein...
                                        '''
                                        assigned_nodes = assigned_nodes + cycle_nodes
                                        for n in cycle_nodes:
                                            class_dict[n] = 'cycle'

                    path_list = path_list[path_index+1:]
                    path_length += 1
                    # print(path_length)

        '''
        Naechster Schritt waere, die in cycles enthaltenen Pfade zu markieren - die
        uebrigen sind dann die fuer die restliche Klassifikation interessanten.
        Dafuer brauchen wir wieder die urspruengliche Matrix.



        for n in range(0, len(self.adj_matrix)):
            if n not in assigned_nodes and self.node_labels[n][n] != 'H':
                node_class, neighbors = self.classify_node(self.adj_matrix, node_index=n)
                class_dict[n]= node_class
                for v in neighbors:
                    if v not in class_dict.keys():
                        class_dict[v] = node_class
                if node_class is not None:
                    assigned_nodes = assigned_nodes+ neighbors
        '''
        return self.sub_graphs

    def get_cycles(self):
        return filter(lambda sg: sg.label == SubGraphLabel.CYCLE, self.sub_graphs)

    def lookup(self, path, node_dict):
        cycle = []
        for node in path:
            cycle.append(node_dict.get(node))
        return cycle

    def update_node_dict(self, node_dict, node_index):
        for key in node_dict:
            if int(key) >= node_index and int(key)+1 < len(node_dict):
                node_dict[key] = node_dict.get(int(key)+1)
        return node_dict

    def has_not_deg_one(self, matrix):
        for i in range(0, len(matrix[0])):
            if numpy.sum(matrix[i], axis=0) == 1:
                return False
        return True

    def remove_node(self, dec_matrix, node_index):
        matr_del = numpy.delete(dec_matrix, obj=node_index, axis=0)
        matr_del = numpy.delete(matr_del, obj=node_index, axis=1)
        return matr_del

    def get_adjacent_nodes(self, matrix, node_index):
        return numpy.where(matrix[node_index] == 1)[0]

    def is_new_cycle(self, path, cycles):
        for c in cycles:
            if set(path) == set(c):
                return False
        return True

    def classify_node(self, matrix, node_index):
        neighbors = self.get_adjacent_nodes(matrix, node_index)
        inv_neighbors = []
        H_count = 0
        for n in neighbors:
            if self.node_labels[n][n] == 'H':
                H_count += 1

        if self.node_labels[node_index][node_index] == 'C':
            if len(neighbors) >= 3 and H_count >= 3:
                for n in neighbors:
                    if self.node_labels[n][n] == 'H':
                        inv_neighbors.append(n)
                return 'methyl', inv_neighbors

        else:
            pass

        '''
        To be continued.
        '''

        return None, inv_neighbors

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
        def r2edges(r): return [i for mask, i in zip(r, indices) if mask]
        # list of lists of connected node ids at node index
        nodei_2_index = map(r2edges, self.adj_matrix)

        def r2labels(r): return [s for s in r if s]
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
