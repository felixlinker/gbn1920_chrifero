from .matrix import *
from multivitamin.algorithms.vf2_subsub import subVF2



class Symmetric:
    def __init__(self, graph_list):
        self.graph_list = graph_list

    def calc_scoring(self):
        score = ScoringMatrix()
        g = self.graph_list
        for g1 in range(0, len(g)):
            for g2 in range(g1+1, len(g)):
                alignment = subVF2(g[g1], g[g2])
                alignment.match()
                al_graph = alignment.result_graphs[0]
                countmatches = 0
                for node in al_graph.nodes:
                    # print('id: ', node.id, ' label: ', node.label)
                    if len(node.label) > 1:
                        countmatches += 1
                score.set_scoring('g'+str(g1), 'g'+str(g2), countmatches)

    def get_scoring(self):
        pass
