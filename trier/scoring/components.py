from Bio.Phylo.TreeConstruction import DistanceMatrix
from functools import reduce

from ..graph.adjacency import AdjacencyGraph
from ..util.func import uncurry


def __asc_commons(l1, l2):
    """Returns a list of all elements that are in two lists. Lists must be
    sorted in ascending order. Return value will be sorted in descending order.

    For example: __asc_commons([1,2,3,4], [0,2,4]) -> [4,2]"""
    if l1 and l2:
        h1, h1_ = 0, 0
        h2, h2_ = 0, 0

        while l1 or l2:
            if h2 <= h1:
                if not l1:
                    break
                h1_ = l1.pop()
            if h1 <= h2:
                if not l2:
                    break
                h2_ = l2.pop()
            h1, h2 = h1_, h2_
            if h1 == h2:
                yield h1


def __adj_component_signatures_distance(adj_graph1, adj_graph2):
    """Compares two adjacency graphs based on their """
    k1 = list(map(len, adj_graph1.get_cycles()))
    k2 = list(map(len, adj_graph2.get_cycles()))
    k_common = list(_asc_commons(k1, k2))
    t1 = list(map(len, adj_graph1.get_tails()))
    t2 = list(map(len, adj_graph2.get_tails()))
    t_common = list(_asc_commons(t1, t2))
    return (0.5 * (len(k_common) / len(k1) + len(k_common) / len(k2)),    # average number of common cycles
            0.5 * (t_common / len(t1) + t_common / len(t2)))    # average number of common tails


class ComponentScorer:
    def __init__(self, graph_list, cycle_tail_weight=(0.5, 0.5)):
        self.graphs = graph_list
        self.matrix = DistanceMatrix(list(map(lambda g: g.id, graph_list)))
        if uncurry(float.__add__)(cycle_tail_weight) != 1:
            raise ValueError("cycle_tail_weight must be 1.0 summed up")
        self.cycle_tail_weight = cycle_tail_weight

    def calc_scoring(self):
        adj_graphs = list(map(AdjacencyGraph, self.graphs))
        for g in adj_graphs:
            g.decompose()
            g.sub_graphs.sort(key=len)

        for i in range(len(adj_graphs)):
            compare1 = adj_graphs[i]
            for compare2 in adj_graphs[i + 1:]:
                score = __adj_component_signatures_distance(compare1, compare2)
                self.matrix[compare1.id, compare2.id] = reduce(float.__add__, map(
                    uncurry(float.__mul__), zip(self.cycle_tail_weight, score)))

    def get_scoring(self):
        return self.matrix
