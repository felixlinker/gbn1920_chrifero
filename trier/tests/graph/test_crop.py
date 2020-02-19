from .util import set_up
from ...graph.crop import crop_graph


def test_crop(graph):
    g = set_up(graph)
    cropped = crop_graph(g)
    nc = graph['cropped_nodes']
    assert cropped.adj_matrix.shape == (nc, nc)
