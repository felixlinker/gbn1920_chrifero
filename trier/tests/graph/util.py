from ...graph.adjacency import AdjacencyGraph


def set_up(graph):
    g = AdjacencyGraph(graph=graph['mv_graph'])
    g.decompose()
    return g
