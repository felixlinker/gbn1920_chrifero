import os
from .matrix import *
from multivitamin.utils.multalign import Multalign
from multivitamin.utils.parser import parse_graph



class Symmetric:
    def __init__(self, graph_list):
        graphs = []
        with os.scandir('./../../graphs/352/graph') as entries:
            for entry in entries:
                print(entry.name)
                graphs.append(parse_graph("./../graphs/352/graph/"+entry.name))
        # print(graphs)
        self.graph_list = graphs

    def calc_scoring(self):
        score = ScoringMatrix()
        g = self.graph_list()
        for g1 in range(0, len(g)):
            for g2 in range(g1+1, len(g)):
                alignment = Multalign(
                    # input_files is a magical global constant set by benchmark.py
                    graph_list=(g[g1], g[g2]),
                    algorithm='SUBVF2',
                    method='GREEDY',
                    save_all=False
                )
                al_graph = alignment.multalign()
                print(len(al_graph.nodes))
                # s = len(al_graph.nodes)
                # score.set_scoring('g'+str(g1), 'g'+str(g2), s)

    def get_scoring(self):
        pass
