from Bio import Phylo
from io import StringIO


class GuidedAligning:
    def __init__(self, graph_list, guide_tree):
        self.graph_list = graph_list
        self.guide_tree = guide_tree
        pass

    def calc_aligning(self):
        # convert tree into newick-format
        handle = StringIO()
        Phylo.write(self.guide_tree, handle, "newick")
        gt_newickformat = handle.getvalue()

        pass
