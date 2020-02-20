from multivitamin.algorithms.vf2_subsub import subVF2
from Bio.Phylo.TreeConstruction import DistanceMatrix


class Symmetric:
    def __init__(self, graph_list):
        self.graph_list = graph_list
        self.matrix = DistanceMatrix(list(map(lambda g: g.id, graph_list)))

    def calc_scoring(self, scoring_matrix=None):
        g = self.graph_list
        for g1 in range(0, len(g)-1):
            for g2 in range(g1+1, len(g)):
                alignment = subVF2(g[g1], g[g2], scoring_matrix=scoring_matrix)
                alignment.match()
                al_graph = alignment.result_graphs[0]
                countmatches = 0
                for node in al_graph.nodes:
                    # print('id: ', node.id, ' label: ', node.label)
                    if len(node.label) > 1:
                        countmatches += 1
                self.matrix[self.graph_list[g1].id, self.graph_list[g2].id] = countmatches

    def get_scoring(self):
        return self.matrix
