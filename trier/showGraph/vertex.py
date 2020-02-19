class Vertex:
    '''
    Vertices are represented as objects
    '''
    def __init__(self, name, label=None, successors = None, predecessors = None):
        self.name = name
        self.label = label
        
        self.successors = []
        self.predecessors = []

    def set_node_label(self, label):
        self.label = label

    def __str__(self):
        return '(name: %s, label: %s)' % (self.name, self.label)

    
class ModularVertex:
    def __init__(self, name, vertex1, vertex2, label=None, successors = None, predecessors = None):
        self.name = name
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.label = label

        self.successors = []
        self.predecessors = []

    def get_vertex1(self):
        return self.vertex1

    def get_name(self):
        return self.name

    def get_vertex2(self):
        return self.vertex2

    def set_node_label(self, label):
        self.label = label

    def __str__(self):
        return '(name: %s, label: %s)' % (self.name, self.label)
