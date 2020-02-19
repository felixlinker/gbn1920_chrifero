from ...graph.adjacency import AdjacencyGraph


def set_up(graph):
    g = AdjacencyGraph(graph=graph['mv_graph'])
    g.decompose()
    return g

def test_tails_num(graph):
    g = set_up(graph)
    tails = len(list(g.get_tails()))
    assert tails == graph['tails']

def test_cycles_num(graph):
    g = set_up(graph)
    cycles = len(list(g.get_cycles()))
    assert cycles == graph['cycles']
