NEG_INF = float('-inf')

class ScoringMatrix:
    def __init__(self):
        self.matrix = dict()

    def set_scoring(self, g1, g2, score):
        """Add a scoring for two graphs to the matrix.
        Graphs must be hashable but might also be some index."""
        self.matrix.setdefault(g1, dict())[g2] = score
        self.matrix.setdefault(g2, dict())[g1] = score

    def get_scoring(self, g1, g2, strict=False):
        """Retrieve a scoring for two graphs. Returns negative infinity if one
        of the graph has not been scored.

        Alternatively, strict can be set to True and a KeyError will be raied if
        one of the graph has not been scored."""
        if strict:
            return self.matrix[g1][g2]
        else:
            return self.matrix.get(g1, dict()).get(g2, NEG_INF)
