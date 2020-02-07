from Bio import Phylo
from io import StringIO
import re

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

        # clean up useless information in newick-format:
        newick = (re.sub(":0.00000", "", gt_newickformat))

        pairs = (re.findall(r"\([^,()]+\,[^,()]+\)", newick))

        # interpret newickformat as alignment-guide
        # for g in self.graph_list:
        #     if g
        pass
