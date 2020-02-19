from Bio import Phylo
from io import StringIO
from multivitamin.algorithms.vf2_subsub import subVF2
from functools import reduce


def get_parent(tree, node):
    path = tree.get_path(node)
    # wenn Pfad die laenge 1 hat, ist die Wurzel der Parent-Knoten
    if len(path) <= 1:
        return tree.clade
    else:
        return path[-2]


class GuidedAligning:
    def __init__(self, graph_list, guide_tree):
        self.graph_list = graph_list
        self.guide_tree = guide_tree
        self.parents = []
        self.results = {}
        for graph in graph_list:
            self.results[graph.id] = graph

    def calc_aligning(self):
        leafs = self.guide_tree.get_terminals()

        # Alle Eltern-Knoten, der Blaetter bestimmen
        for leaf in leafs:
            self.parents.append(get_parent(self.guide_tree, leaf))

        self.rec()
        return self.results

    def rec(self):
        new_parents = []
        # wieder nach Eltern-Knoten schauen
        for p in self.parents:
            all_leafs_in_result = True
            for leaf in p.clades:
                if leaf.name not in self.results:
                    all_leafs_in_result = False
                    break
            if p.name not in self.results:
                if all_leafs_in_result:
                    self.results[p.name] = reduce(self.aggregator, p.clades[1:], self.results[p.clades[0].name])
                    new_parents.append(get_parent(self.guide_tree, p))
                else:
                    new_parents.append(p)

        if len(new_parents):
            self.parents = new_parents
            self.rec()

    def aggregator(self, aggr, v):
        instance = subVF2(aggr, self.results[v.name])
        instance.match()
        return instance.get_real_result_graph()
