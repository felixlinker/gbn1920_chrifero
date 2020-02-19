import numpy
from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge
from multivitamin.basic.graph import Graph
from enum import Enum
from scipy.sparse.csgraph import dijkstra

from ..util.func import concat

_map_is_reachable = numpy.vectorize(lambda v: v < float('inf'))


def _split_reachability(sub_graph, parent):
    reachability_matrix = dijkstra(sub_graph.adj_matrix, directed=False)
    indexes = numpy.array(range(sub_graph.adj_matrix.shape[0]))
    reachables = map(lambda r: indexes * r,
                     _map_is_reachable(reachability_matrix))
    for i, reachables in enumerate(reachables):
        # Only consider every set of reachables once
        if reachables[0] < i:
            continue
        new_matrix = numpy.zeros(sub_graph.adj_matrix.shape)
        for row in reachables:
            for col in reachables:
                new_matrix[row, col] = sub_graph.adj_matrix[row, col]
        yield SubGraph(parent, adj_matrix=new_matrix, label=sub_graph.label)


class SubGraphLabel(Enum):
    CYCLE = 0
    TAIL = 1


class SubGraph:
    def __init__(self, parent, adj_matrix=None, label=None,atom_dict = None):
        self.parent = parent
        if adj_matrix is not None and adj_matrix.shape != parent.adj_matrix.shape:
            raise ValueError("adjacency matrices must agree on shape")
        self.adj_matrix = adj_matrix if adj_matrix is not None else numpy.zeros(
            parent.adj_matrix.shape)
        self.label = label
        if atom_dict is None and self.adj_matrix is not None:
            self.atom_dict = self.get_chem_label()
        elif self.adj_matrix is None:
            print("Warning: Subgraph with empty adjacency matrix.")

    def __len__(self):
        """Returns the number of all nodes in the subgraph."""
        # Get the number of rows that are connected to at least one node
        return len(list(filter(lambda s: 0 < s, map(numpy.sum, self.adj_matrix))))

    def get_chem_label(self):
        '''Returns a classifier for structural type as str'''
        self.atom_dict = {}

        labels  = []
        for n in range(0, len(self.adj_matrix)):
            if numpy.sum(self.adj_matrix[n], axis=0) >= 1:
                labels.append(self.parent.node_labels[n][0])
        labels.sort()
        for ch in labels:
            if ch not in self.atom_dict.keys():
                self.atom_dict[ch] = labels.count(ch)
        return self.atom_dict


    def __str__(self):
        if self.label == SubGraphLabel.CYCLE:
            ch_str = "R"
        else:
            ch_str = "T"
        for key in sorted(self.atom_dict.keys()):
            ch_str = ch_str + ''.join([str(key)*self.atom_dict.get(key)])
            #ch_str = ch_str + str(key)
        return ch_str

class AdjacencyGraph:
    def __init__(self, graph=None, gid=None, matrix=None, edge_labels=None, node_labels=None):
        self.sub_graphs = []
        if graph:
            self._from_multivitamin(graph)
        elif matrix and edge_labels and node_labels:
            self.id = gid
            self.adj_matrix = matrix
            self.edge_labels = edge_labels
            self.node_labels = node_labels
        else:
            raise ValueError('not enough arguments')

    def _from_multivitamin(self, graph):
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
        self._split_connected_subgraphs()
        self.split_cycles()
        return self.sub_graphs

    def cut_tails(self):
        '''
        First, size of search area will be reduced to identify cyclic structures:
        '''
        dec_matrix = self.adj_matrix
        del_adj_matrix = numpy.zeros_like(self.adj_matrix)
        is_trimmed = self.has_not_deg_one(dec_matrix)

        '''
        for i in range(0, len(self.adj_matrix)):
            node_index_dict[i] = i
        '''
        while is_trimmed is not True:
            for i in range(0, len(self.adj_matrix[0])):
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
        if len(numpy.nonzero(del_adj_matrix)[0]) > 0:
            self.sub_graphs.append(SubGraph(parent=self, adj_matrix=del_adj_matrix, label=SubGraphLabel.TAIL))
        return self.sub_graphs

    def get_tails(self):
        return filter(lambda sg: sg.label == SubGraphLabel.TAIL, self.sub_graphs)

    def _split_connected_subgraphs(self):
        # Split every subgraph into a set of strongly connected components
        splitted = [_split_reachability(sg, self) for sg in self.sub_graphs]
        # Merge the list of connected components
        self.sub_graphs = concat(splitted)

    def split_cycles(self):
        '''
        Finding cyclic paths:

        NOTE2: Die nodes nach Grad zu sortieren waere eine sinnvolle Ergaenzung.
        Oder auch nicht, gemessen daran dass ziemlich viele Knoten ohnehin wegfallen.
        '''
        # print(dec_matrix)
        cycles = []

        for i in range(0, len(self.adj_matrix[0])):
            if numpy.sum(self.adj_matrix[i], axis=0) >= 1:
                path_length = 1
                path_list = []
                new_path = []
                new_path.append(i)
                path_list.append(new_path)
                while path_length <= 6:
                    path_index = len(path_list)-1
                    for p in range(0, len(path_list)):
                        path = path_list[p]
                        neighbors = self.get_adjacent_nodes(self.adj_matrix, path[len(path)-1])

                        for node in neighbors:
                            if node not in path:
                                next_path = path.copy()
                                #print('Next path: ' + str(next_path))
                                next_path.append(node)
                                path_list.append(next_path)
                                #print(next_path)
                            elif path[0] == node and len(path) >= 3:
                                if self.is_new_cycle(path, cycles):
                                    cycles.append(path)

                    path_list = path_list[path_index+1:]
                    #print(path_list)
                    path_length += 1
                    # print(path_length)

        for path in cycles:
            sub_matrix = numpy.zeros_like(self.adj_matrix)
            for n in range(0, len(path)-1):
                sub_matrix[path[n]][path[n+1]] =1
                sub_matrix[path[n+1]][path[n]] =1
                self.adj_matrix[path[n]][path[n+1]] =0
                self.adj_matrix[path[n+1]][path[n]] =0
            sub_matrix[path[0]][path[len(path)-1]] =1
            sub_matrix[path[len(path)-1]][path[0]] =1
            self.adj_matrix[path[0]][path[len(path)-1]] =0
            self.adj_matrix[path[len(path)-1]][path[0]] =0
            
            self.sub_graphs.append(SubGraph(parent=self,adj_matrix=sub_matrix, label=SubGraphLabel.CYCLE))

        return self.sub_graphs

    def get_cycles(self):
        return filter(lambda sg: sg.label == SubGraphLabel.CYCLE, self.sub_graphs)

    def has_not_deg_one(self, matrix):
        for i in range(0, len(matrix[0])):
            if numpy.sum(matrix[i], axis=0) == 1:
                return False
        return True

    def get_adjacent_nodes(self, matrix, node_index):
        return numpy.where(matrix[node_index] == 1)[0]

    def is_new_cycle(self, path, cycles):
        for c in cycles:
            if set(c).issubset(set(path)):
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
                     edges=set(concat(node_2_edges.values())),
                     nodes_labelled=True, edges_labelled=True,
                     is_directed=False)

    def __len__(self):
        """Returns the number of nodes in the graph."""
        return self.adj_matrix.shape[0]

    def __repr__(self):
        r = ""
        r += f"#nodes;{self.adj_matrix.shape[0]}\n"
        r += f"#edges;{numpy.count_nonzero(self.adj_matrix)}\n"
        r += "Nodes labelled;True\n"
        r += "Edges labelled;True\n"
        r += "Directed graph;False\n"
        r += "\n"
        r += "\n".join([f"{i};{l}" for i, l in enumerate(self.node_labels)])
        r += "\n"
        r += "\n".join([f"{i};{j};{l}"
                        for (i, j), l in numpy.ndenumerate(numpy.tril(self.edge_labels))
                        if l])
        r += "\n"
        return r
