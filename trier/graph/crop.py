import numpy as np
from .adjacency import AdjacencyGraph, SubGraph
from scipy.sparse.csgraph import dijkstra


# This function maps a matrix returned by dijkstra to an adjacency matrix that
# represents the transitive closure of the original matrix where there is an
# edge between any reachable nodes
_map_transitive_closure = np.vectorize(
    lambda x: int(0 < x and x < float('inf')))


def crop_graph(graph: AdjacencyGraph):
    components = graph.get_tails() + graph.get_cycles()
    new_adj = np.zeros((len(components), len(components)))
    for i, comp in enumerate(components):
        base = _map_transitive_closure(
            dijkstra(comp.adj_matrix + graph.adj_matrix, directed=False))
        for j, other in enumerate(components[i + 1:]):
            adj = base + _map_transitive_closure(dijkstra(other.adj_matrix))
            reachable_closure = _map_transitive_closure(
                dijkstra(adj, directed=False))
            is_adj = int(np.any(adj < reachable_closure))
            new_adj[i][i + 1 + j] = is_adj
            new_adj[i + 1 + j][i] = is_adj
    return AdjacencyGraph(gid=graph.id + '_reduced', matrix=new_adj,
                          edge_labels=np.full(new_adj.shape, ''),
                          node_labels=list(map(str, components)))
