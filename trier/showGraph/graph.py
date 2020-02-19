class Graph:
    '''
    Graph object consisting of vertices and edges
    '''

    def __init__(self, vertices: [] = None, edges: [] = None,\
                 no_of_vertices = None, no_of_edges = None,\
                 vertices_labelled = None, edges_labelled = None, directed_graph = None, name = None):
        self.vertices = vertices    # list of vertex objects
        self.edges = edges          # list of edge objects
        if vertices is None:
            self.vertices = []
        if edges is None:
            self.edges = []
        self.no_of_vertices = no_of_vertices
        self.no_of_edges = no_of_edges
        self.vertices_labelled = vertices_labelled
        self.edges_labelled = edges_labelled
        self.directed_graph = directed_graph
        self.name = name

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edges(self, edge):
        self.edges.append(edge)

    def get_edges(self):
        return self.edges
    
    def get_vertex_names(self):
        names = []
        for vertex in self.vertices:
            names.append(vertex.name)
        return names
    
    def remove_edge(self, e):
        if e in self.edges:
            e.cut_predecessors()
            e.cut_successors()
            self.edges.remove(e)
        else:
            print("The edge to remove is not in the given graph.")
    # def __str__(self):
    #     return '(vertices: %s, edges: %s)' % (self.vertices, self.edges)
    
