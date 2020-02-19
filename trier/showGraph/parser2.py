'''
Uses a graph-file as input and creates a Graph-Object out of Vertex and Edge Objects
'''
from vertex import Vertex
from edge import Edge
from graph import Graph
from mendeleev import element


def parse(filename):

    # Properties of the graph. Characterized in the first block of a graph-file
    n_of_nodes = 0
    n_of_edges = 0
    nodes_label = False
    edges_label = False
    directed_graph = False

    # Vertex list is characterized in the 2nd block of a graph-file
    vertex_list = []

    # Edge list is characterized in the 3rd block of a graph-file
    edge_list = []

    # c is a counter to know in which block of the graph-file we are
    c = 0

    # dict für das Zugreifen auf die Vertices über ihre Namen
    vertex_dict = {}
    with open(filename, 'r') as file:
        file_content = file.readlines()
        for i in range(0, len(file_content)):
            temp = file_content[i].replace('\n', '').split(';')
            if temp == ['']:
                c += 1
            elif temp != '' and c == 0:
                if temp[0] == '#nodes':
                    n_of_nodes = temp[1]
                elif temp[0] == '#edges':
                    n_of_edges = temp[1]
                elif temp[0] == 'Nodes labelled':
                    if temp[1] == 'True':
                        nodes_label = True
                    else:
                        nodes_label = False
                elif temp[0] == 'Edges labelled':
                    if temp[1] == 'True':
                        edges_label = True
                    else:
                        edges_label = False
                elif temp[0] == 'Directed graph':
                    if temp[1] == 'True':
                        directed_graph = True
                    else:
                        directed_graph = False
            elif c == 1:
                v = Vertex(temp[0])
                if nodes_label:
                     v.set_node_label(temp[1])
                vertex_list.append(v)
                vertex_dict.update({v.name: v})  # Vertex wird für Edges-Initialiserung gespeichert (Name=Key)
            elif c == 2:
                e = Edge(vertex_dict.get(temp[0]), vertex_dict.get(temp[1]), None, None, directed_graph)
                if edges_label:
                    e.set_label(temp[2])
                edge_list.append(e)

    graph = Graph(vertex_list, edge_list, n_of_nodes, n_of_edges, nodes_label, edges_label, directed_graph)
    return graph


def reverse_parser(g):
    '''
    :param g: Graph Object
    :return: .graph text
    USAGE run in terminal: python3 main.py >> newgraph.graph
    '''
    number_of_vertices = len(g.vertices)
    number_of_edges = len(g.edges)
    labelled_vertices = g.vertices_labelled
    labelled_edges = g.edges_labelled
    directed_graph = g.directed_graph

    Block2 = []
    Block3 = []

    # if-function is necessary because graph-Objects which were randomly created don't have labels
    if labelled_vertices != None:

        for vertex in g.vertices:
            if vertex.label != None:
                Block2.append(str(vertex.name)+';'+str(vertex.label))
            else:
                Block2.append(str(vertex.name)+';')

        for edge in g.edges:
            if edge.label != None:
                Block3.append(str(edge.vertex_a.name)+';'+str(edge.vertex_b.name)+';'+str(edge.label))
            else:
                Block3.append(str(edge.vertex_a.name)+';'+str(edge.vertex_b.name))

    else:

        labelled_vertices = False
        labelled_edges = False
        directed_graph = False

        for vertex in g.vertices:
            Block2.append(str(vertex.name) + ';')

        for edge in g.edges:
            Block3.append(str(edge.vertex_a.name) + ';' + str(edge.vertex_b.name))

    print('#nodes;',number_of_vertices,'\n',\
          '#edges;',number_of_edges,'\n',\
          'Nodes labelled;',labelled_vertices,'\n',\
          'Edges labelled;', labelled_edges,'\n',\
          'Directed graph;',directed_graph,'\n', sep='')

    for word in Block2:
        print(word)
    print()
    for word in Block3:
        print(word)



def parse_chem(filename):
    # Properties of the graph. Characterized in the first block of a graph-file
    n_of_nodes = 0
    n_of_edges = 0
    nodes_label = True
    edges_label = True
    directed_graph = False

    #Booleans to check in which part of the Chem-Graph we are
    into_vertices = False
    into_vertex_labels = False
    into_edges_one = False
    into_edges_two = False
    into_edges_label = False

    #Lists to save all vertices, edges and teh respective labels to then create the graph-object from
    vertices_all = []
    vertex_labels_all = []
    edges_one_all = []
    edges_two_all = []
    edges_labels_all = []


    # Vertex list is characterized in the 2nd block of a graph-file
    vertex_list = []

    # Edge list is characterized in the 3rd block of a graph-file
    edge_list = []

    # dict for accessing the vertices via their names
    vertex_dict = {}

    with open(filename, 'r') as file:
        file_content = file.readlines()
        for i in range(0, len(file_content)):
            temp: str = file_content[i].replace('\n', '')
            temp = temp.replace(' ', '')
            #finish reading the file after the important first few blocks
            if temp == '"coords":[':
                break
            if temp == '"aid":[':
                into_vertices = True
            elif temp == '"element":[':
                into_vertex_labels = True
            elif temp == '"aid1":[':
                into_edges_one = True
            elif temp == '"aid2":[':
                into_edges_two = True
            elif temp == '"order":[':
                into_edges_label = True
            elif temp == '],' and into_edges_one:
                into_edges_one = False
            elif temp == '],' and into_edges_two:
                into_edges_two = False
            elif temp == ']' and into_edges_label:
                into_edges_label = False
            elif into_vertices and temp == '],':
                into_vertices = False
            elif into_vertex_labels and temp == ']':
                into_vertex_labels = False
            elif into_vertices:
                temp2 = temp.split(',')
                vertices_all.append(temp2[0])
            elif into_vertex_labels:
                temp2 = temp.split(',')
                vertex_labels_all.append(temp2[0])
            elif into_edges_one:
                temp2 = temp.split(',')
                edges_one_all.append(temp2[0])
            elif into_edges_two:
                temp2 = temp.split(',')
                edges_two_all.append(temp2[0])
            elif into_edges_label:
                temp2 = temp.split(',')
                edges_labels_all.append(temp2[0])
        # creating graph-object after finishing reading the file
        for i in range(0,len(vertices_all)):
            v = Vertex(vertices_all[i])
            e = element(int(vertex_labels_all[i]))
            v.set_node_label(e.symbol)
            vertex_list.append(v)
            vertex_dict.update({v.name: v})

        for i in range(0,len(edges_one_all)):
            e = Edge(vertex_dict.get(edges_one_all[i]), vertex_dict.get(edges_two_all[i]))
            e.set_label(edges_labels_all[i])
            edge_list.append(e)

        n_of_nodes = len(vertices_all)
        n_of_edges = len(edges_one_all)


    graph = Graph(vertex_list, edge_list, n_of_nodes, n_of_edges, nodes_label, edges_label, directed_graph)
    return graph

