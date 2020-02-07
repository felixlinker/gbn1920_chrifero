import numpy
import time

class AdjacencyGraph:
    def __init__(self, graph=None, matrix=None, edge_labels=None, node_labels=None):
        self.adj_matrix = numpy.array([])
        self.edge_labels = numpy.array([])
        self.node_labels = numpy.array([])

        
    def decompose(self):
        '''
        First, size of search area will be reduced to identify cyclic structures:
        '''
        dec_matrix = self.adj_matrix
        is_trimmed = self.has_not_deg_one(dec_matrix)
        
        node_index_dict = {}
        for i in range(0, len(self.adj_matrix)):
            node_index_dict[i] = i
            
        while is_trimmed is not True:     
            for i in range(0, len(dec_matrix[0])):
                if numpy.sum(dec_matrix[i], axis = 0) == 1:
                    dec_matrix = self.remove_node(dec_matrix, node_index=i)
                    node_index_dict = self.update_node_dict(node_index_dict, node_index=i)
                    break
            is_trimmed=self.has_not_deg_one(dec_matrix)
        '''
        Finding cyclic paths:
        NOTE1: Unnoetig, wenn weniger als 5 Knoten.
            
        NOTE2: Die nodes nach Grad zu sortieren waere eine sinnvolle Ergaenzung
        
        NOTE3: Schlaueres Abbruchkriterium finden, auch wenn die tatsaechliche 
        Anzahl an Operationen geringer ist als die Schleifen vermuten lassen.\
        
        NOTE4: Dictionary fuer urspruengliche node_indices.
        '''
        #print(dec_matrix)
        cycles =[]
        assigned_nodes=[]
        class_dict ={}
        
        if len(dec_matrix[0]) > 5:
            
            for i in range(0, len(dec_matrix[0])):
                path_length = 1
                path_list = []
                new_path = []
                new_path.append(i)
                path_list.append(new_path)
                while path_length < 6:
                    path_index = len(path_list)-1
                    
                    for p in range(0, len(path_list)):
                        path = path_list[p]
                        neighbors = self.get_adjacent_nodes(dec_matrix, path[len(path)-1])
                        #print(neighbors)
                        
                        for node in neighbors:
                            if node not in path or path[0]==node:
                                next_path = path
                                next_path.append(node)
                                path_list.append(next_path)
                                #print(next_path)
                                
                                if path[0]==node:
                                    cycle_nodes = self.lookup(path, node_index_dict)
                                    
                                    if self.is_new_cycle(cycle_nodes, cycles):
                                        print("Cycle found: " + str(cycle_nodes))
                                        cycles.append(cycle_nodes)
                                        '''
                                        An sich sollte hier dann noch abgefragt werden ob der 
                                        Cycle lang genug ist, aber vielleicht, faellt uns ja noch
                                        ein Nutzen fuer 4-Zyklen ein...
                                        '''
                                        assigned_nodes = assigned_nodes +cycle_nodes
                                        for n in cycle_nodes:
                                            class_dict[n]= 'cycle'
                                        
                    path_list = path_list[path_index+1:]
                    path_length+=1
                    #print(path_length)
        
        '''
        Naechster Schritt waere, die in cycles enthaltenen Pfade zu markieren - die 
        uebrigen sind dann die fuer die restliche Klassifikation interessanten.
        Dafuer brauchen wir wieder die urspruengliche Matrix.
        
        
        
        for n in range(0, len(self.adj_matrix)):
            if n not in assigned_nodes and self.node_labels[n][n] != 'H':
                node_class, neighbors = self.classify_node(self.adj_matrix, node_index=n)
                class_dict[n]= node_class
                for v in neighbors:
                    if v not in class_dict.keys():
                        class_dict[v] = node_class
                if node_class is not None:
                    assigned_nodes = assigned_nodes+ neighbors
        '''
        return class_dict
    
    def lookup(self, path, node_dict):
        cycle = []
        for node in path:
            cycle.append(node_dict.get(node))
        return cycle
        
    
    def update_node_dict(self, node_dict, node_index):
        for key in node_dict:
            if int(key) >= node_index and int(key)+1 < len(node_dict):
                node_dict[key] = node_dict.get(int(key)+1)
        return node_dict
    
    def has_not_deg_one(self, matrix):
        for i in range(0, len(matrix[0])):
            if numpy.sum(matrix[i], axis = 0) == 1:
                return False
        return True

    def remove_node(self, dec_matrix, node_index):
        matr_del = numpy.delete(dec_matrix, obj=node_index, axis=0)
        matr_del = numpy.delete(matr_del, obj=node_index, axis=1)
        return matr_del
    
    def get_adjacent_nodes(self, matrix, node_index):
        return numpy.where(matrix[node_index] == 1)[0]
    
    def is_new_cycle(self, path, cycles):
        for c in cycles:
            if set(path)==set(c):
                return False
        return True
        
    def classify_node(self, matrix, node_index):
        neighbors = self.get_adjacent_nodes(matrix, node_index)
        inv_neighbors = []
        H_count = 0
        for n in neighbors:
            if self.node_labels[n][n] == 'H':
                H_count +=1
        
        if self.node_labels[node_index][node_index] == 'C':
            if len(neighbors)>= 3 and H_count >= 3:
                for n in neighbors:
                    if self.node_labels[n][n] =='H':
                        inv_neighbors.append(n)
                return 'methyl', inv_neighbors
        
        else:
            pass
        
        '''
        To be continued.
        '''
        
        return None, inv_neighbors

    def to_multivitamin(self):
        pass

'''
Testing:


start = time.time()
test1 = AdjacencyGraph(graph=None, matrix=None, edge_labels=None, node_labels=None)
test1.adj_matrix = numpy.zeros((10, 10))
test1.adj_matrix[1][2] = 1
test1.adj_matrix[2][1] = 1
test1.adj_matrix[2][3] = 1
test1.adj_matrix[3][2] = 1
test1.adj_matrix[4][3] = 1
test1.adj_matrix[3][4] = 1
test1.adj_matrix[5][6] = 1
test1.adj_matrix[6][5] = 1
test1.adj_matrix[6][1] = 1
test1.adj_matrix[1][6] = 1
test1.adj_matrix[5][4] = 1
test1.adj_matrix[4][5] = 1
print(test1.adj_matrix)
test1.decompose()
end = time.time()
print('Time elapsed: ' + str(end -start))
#print(test1.adj_matrix)
'''
