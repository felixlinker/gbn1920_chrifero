from Bio import Phylo
from io import StringIO
import re


class GuidedAligning:
    def __init__(self, graph_list, guide_tree):
        self.graph_list = graph_list
        self.guide_tree = guide_tree
        pass



    def calc_aligning(self):

        if self.guide_tree.is_bifurcating():
            print('Alles gut')
        else:
            print('Nicht gut')

        leafs = self.guide_tree.get_terminals()
        root = self.guide_tree.clade

        # for t in root.clades:
        #     if t in leafs:
        #         print('Pair: ', self.guide_tree.clades)
        #     else:
        #         self.get_children(t)

        for t in root.clades:
            while t not in leafs:
                t = t.clades
            print('Pair: ', self.guide_tree.clades)

        pass
