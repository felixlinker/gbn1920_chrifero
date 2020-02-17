from .components import ComponentScorer
from .symmetric import Symmetric
from ..graph.crop import crop_graph
from ..util.func import uncurry


def _subgraph_distance(sg1, sg2):
    d = sg1.get_chem_label()
    d.update([(k, abs(v - d.get(k, 0)))
              for k, v in sg2.get_chem_label().items()])
    vs = d.values()
    # Score is 1/2^(avg_label_distance)
    return 1 / 2 ** (sum(vs) / len(vs))


def _scoring_matrix(graphs):
    matrix = {('-', '-'): -1}
    for g1, i in enumerate(graphs):
        for g2 in enumerate(graphs[i + 1:]):
            label_score = _subgraph_distance(g1, g2)
            matrix[(str(g1), str(g2))] = label_score
            matrix[(str(g2), str(g1))] = label_score
    return matrix


class CroppingScorer(ComponentScorer):
    def __init__(self, graph_list,  crop_component_weight=(0.5, 0.5),
                 cycle_tail_weight=(0.5, 0.5)):
        super().__init__(graph_list, cycle_tail_weight=cycle_tail_weight)
        if uncurry(float.__add__)(crop_component_weight) != 1:
            raise ValueError("crop_component_weight must be 1.0 summed up")
        self.crop_component_weight = crop_component_weight

    def calc_scoring(self):
        super().calc_scoring()
        cropped = list(map(crop_graph, self.graphs))
        symmetric_cropped = Symmetric(cropped)
        symmetric_cropped.calc_scoring(scoring_matrix=_scoring_matrix(cropped))
        crop_weight, component_weight = self.crop_component_weight
        self.matrix *= component_weight
        self.matrix += crop_weight * symmetric_cropped.get_scoring()

    def get_scoring(self):
        return self.matrix
