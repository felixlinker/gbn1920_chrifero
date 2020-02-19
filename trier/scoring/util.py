import numpy as np
from Bio.Phylo.TreeConstruction import DistanceMatrix


def score_to_distance(score_matrix):
    np_score = np.array(list(score_matrix))
    max_score = np.max(np_score)

    map_flip = np.vectorize(lambda v: v + max_score - 2 * v)
    flipped = map_flip(np_score)
    return DistanceMatrix(score_matrix.names,
                          matrix=[list(map(int, sl[:i+1]))
                                  for i, sl in enumerate(flipped)])
