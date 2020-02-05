import os
from benchmarks import bm_multivitamin
from .matrix import *
from multivitamin.utils.multalign import Multalign



class Symmetric:
    def __init__(self, graph_list):
        count = 1
        graphs = []
        with os.scandir('./../graphs/352/graph') as entries:
            for entry in entries:
                print(entry.name)
                g = "g" + str(count)
                # g1 = parse("./../graphs/352/graph/"+entry.name)
                graphs.append(g)
                count += 1
        print(graphs)
        self.graph_list = graphs
        pass

    def calc_scoring(self):
        score = ScoringMatrix()
        g = self.graph_list()
        for g1 in range(0, len(g)):
            for g2 in range(1, len(g)):
                alignment = Multalign(
                    # input_files is a magical global constant set by benchmark.py
                    graph_list=(g[g1], g[g2]),
                    algorithm='SUBVF2',
                    method='GREEDY',
                    save_all=False
                )
                alignment.multalign()
                # s = alignment.countmatches()
                # score.set_scoring('g'+str(g1), 'g'+str(g2), s)
        pass

    def get_scoring(self):
        pass
