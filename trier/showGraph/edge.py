from vertex import Vertex


class Edge:
    '''
    Edges are represented as objects
    '''
    #In this setup edges are initially treated as directed
    def __init__(self, vertex_a=Vertex, vertex_b=Vertex, label=None, weight=None, directed_graph=bool):
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
        if vertex_b not in vertex_a.successors:             # if bedingung wird momentan benötigt, bin aber unsicher ob sie dauerhaft drin bleiben darf
            self.vertex_a.successors.append(vertex_b)
        if vertex_a not in vertex_b.predecessors:
            self.vertex_b.predecessors.append(vertex_a)
        if directed_graph is False:
            if vertex_a not in vertex_b.successors:             # if bedingung wird momentan benötigt, bin aber unsicher ob sie dauerhaft drin bleiben darf
                self.vertex_b.successors.append(vertex_a)
            if vertex_b not in vertex_a.predecessors:
                self.vertex_a.predecessors.append(vertex_b)
        self.label = label
        self.weight = weight

    def set_weight(self, weight):
        self.weight = weight

    def set_label(self, label):
        self.label = label

    def getlabel(self):
        return self.label

    def __str__(self):
        return '(vertex_a: %s, vertex_b: %s, label: %s, weight: %s)' % (self.vertex_a, self.vertex_b, self.label, self.weight)

        #The following two functions should be called to cleanly remove an edge from an existing graph
    def cut_successors(self):
        if self.vertex_b in self.vertex_a.successors:
            self.vertex_a.successors.remove(self.vertex_b)
        if self.vertex_a in self.vertex_b.successors:
            self.vertex_b.successors.remove(self.vertex_a)
        
    def cut_predecessors(self):
        if self.vertex_b in self.vertex_a.predecessors:
            self.vertex_a.predecessors.remove(self.vertex_b)
        if self.vertex_a in self.vertex_b.predecessors:
            self.vertex_b.predecessors.remove(self.vertex_a)
