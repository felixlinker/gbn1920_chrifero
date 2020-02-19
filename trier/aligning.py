from Bio import Phylo
from io import StringIO
from multivitamin.algorithms.vf2_subsub import subVF2


class GuidedAligning:
    def __init__(self, graph_list, guide_tree):
        self.graph_list = graph_list
        self.guide_tree = guide_tree
        self.alignment_pairs = []
        self.parents = []
        self.results = {}
        for graph in graph_list:
            self.results[graph.id] = graph

    def calc_aligning(self):
        print(self.guide_tree)
        if self.guide_tree.is_bifurcating():
            print('Baum. Gut.')
        else:
            print('Nicht gut, Tree is not bifurcating')

        leafs = self.guide_tree.get_terminals()

        # Alle Eltern-Knoten, der Blaetter bestimmen
        for leaf in leafs:
            leaf_path = self.guide_tree.get_path(leaf)
            # wenn Pfad die laenge 1 hat, ist die Wurzel der Parent-Knoten
            if len(leaf_path) == 1:
                parent = self.guide_tree.clade
            else:
                parent = leaf_path[-2]
            self.parents.append(parent)

        # Wenn zwei Eltern-Knoten uebereinstimmen, sollen ihr Kinder-Knoten aligniert werden.
        for p1 in range(0, len(self.parents)-1):
            for p2 in range(p1+1, len(self.parents)):
                if self.parents[p1] == self.parents[p2]:
                    self.alignment_pairs.append(self.parents[p1])
                    #graphen bestimmen
                    g1 = self.parents[p1].clades[0].name
                    g2 = self.parents[p1].clades[1].name
                    print(type(self.results))
                    # Aligniere Paar mit subVF2
                    instance = subVF2(self.results[g1], self.results[g2])
                    instance.match()
                    result_graph = instance.get_real_result_graph()
                    # Speichere Result in dict
                    self.results[self.parents[p1].name] = result_graph

        # Testen ob es einen noch nicht gematchten Leaf gibt, der muss auch in pairs
        for p1 in range(0, len(self.parents)):
            if self.parents[p1] not in self.alignment_pairs:
                self.alignment_pairs.append(self.parents[p1])
        # Rekursiv schauen, welche Eltern-Knoten aligniert werden sollen
        self.rec(self.alignment_pairs)
        return self.results

    def rec(self, list_of_pairs):
        self.parents = []

        # wieder nach Eltern-Knoten schauen
        for p in list_of_pairs:
            leaf_path = self.guide_tree.get_path(p)
            if len(leaf_path) <= 1:
                parent = self.guide_tree.clade
            else:
                parent = leaf_path[-2]
            self.parents.append(parent)

        test_root = self.guide_tree.clade
        # wieder nach Ubereinstimmungen schauen, damit Kinder-Knoten in alignier-Liste aufgenommen werden
        for p1 in range(0, len(self.parents)-1):
            for p2 in range(p1+1, len(self.parents)):
                if self.parents[p1] == self.parents[p2]:
                    self.alignment_pairs.append(self.parents[p1])
                    # graphen bestimmen
                    g1 = self.parents[p1].clades[0].name
                    g2 = self.parents[p1].clades[1].name
                    print(type(self.results))
                    # Aligniere Paar mit subVF2
                    instance = subVF2(self.results[g1], self.results[g2])
                    instance.match()
                    result_graph = instance.get_real_result_graph()
                    # Speichere Result in dict
                    self.results[self.parents[p1].name] = result_graph
                    test_root = self.parents[p1]

        # wenn beide Eltern-Knoten die Wurzel des baums sind, ist Rekursion beendet
        if test_root == self.guide_tree.clade:# and test_root2 == self.guide_tree.clade:
            return self.alignment_pairs
        else:
            self.rec(self.alignment_pairs)
