from Bio import Phylo
from io import StringIO

class GuidedAligning:
    def __init__(self, graph_list, guide_tree):
        # convert tree into newick-format
        handle = StringIO()
        Phylo.write(guide_tree, handle, "newick")
        gt_newickformat = handle.getvalue()


        pass

    def calc_aligning(self):
        pass
