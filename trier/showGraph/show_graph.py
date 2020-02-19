import networkx as nx
import matplotlib.pyplot as plt

def get_color_dict():
    color_dict = {'0':'black','H':'b','O':'r','C':'g','N':'pink', 'S':'yellow'}
    return color_dict

def show_graph(g):
    
    graph = nx.Graph()
    color_dict = get_color_dict()
    pos=nx.spring_layout(graph)
    
    # generates nodelist which is readable by networkx
    color_map = []
    node_labels = {}
    for v in g.vertices:
        graph.add_node(v.name)
        node_labels[v.name] = v.label 
        #node_list.append(v.name)
        if v.label in color_dict.keys():
            color = color_dict.get(v.label)
        else:
            color = color_dict.get('0')
        color_map.append(color)
    
    # generate and add edges to graph
    edge_label_list = []
    edge_tuple_list = []
    for edge in g.get_edges():
            edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
            edge_tuple_list.append(edge_tuple)
            edge_label_list.append(edge.label)
  
    graph.add_edges_from(edge_tuple_list, width =1)
    
    #set graph parameters for layout, labels, coloring
    pos=nx.spring_layout(graph)
    nx.draw(graph, pos, node_color= color_map, with_labels=False, node_size=800)
    nx.draw_networkx_labels(graph, pos, labels =node_labels, font_size=11)
    #nx.draw_networkx_edge_labels(graph, pos, labels =edge_label_list, font_size=10)
    plt.axis('equal')
    plt.show()


def show_two_graphs(g1, g2):
    #generating edgelists readably by networkx
    g1edge_tuple_list = []
    for edge in g1.get_edges():
        edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
        g1edge_tuple_list.append(edge_tuple)
    g2edge_tuple_list = []
    for edge in g2.get_edges():
        edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
        g2edge_tuple_list.append(edge_tuple)

    #generating networkx graphs
    graph1 = nx.Graph()
    graph1.add_edges_from(g1edge_tuple_list)
    graph2 = nx.Graph()
    graph2.add_edges_from(g2edge_tuple_list)
    plt.clf()

    plt.subplot(121)
    plt.title('Graph1')
    nx.draw(graph1, node_color='lightblue', node_size=800, with_labels=True)
    plt.subplot(122)
    plt.title('Graph2')
    nx.draw(graph2, node_color='lightblue', node_size=800, with_labels=True)
    plt.axis('equal')
    plt.show()


def show_graph_comparable(g1, g2, g3):
    #generating edgelists readably by networkx
    g1edge_tuple_list = []
    for edge in g1.get_edges():
        edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
        g1edge_tuple_list.append(edge_tuple)
    g2edge_tuple_list = []
    for edge in g2.get_edges():
        edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
        g2edge_tuple_list.append(edge_tuple)
    g3edge_tuple_list = []
    for edge in g3.get_edges():
        edge_tuple = (edge.vertex_a.name, edge.vertex_b.name)
        g3edge_tuple_list.append(edge_tuple)

    #generating networkx graphs
    graph1 = nx.Graph()
    graph1.add_edges_from(g1edge_tuple_list)
    graph2 = nx.Graph()
    graph2.add_edges_from(g2edge_tuple_list)
    graph3 = nx.Graph()
    graph3.add_edges_from(g3edge_tuple_list)
    plt.clf()

    plt.subplot(221)
    plt.title('Graph1')
    nx.draw(graph1, node_color='lightblue', node_size=800, with_labels=True)
    plt.subplot(222)
    plt.title('Graph2')
    nx.draw(graph2, node_color='lightblue', node_size=800, with_labels=True)
    plt.subplot(223)
    plt.title('Graph3')
    nx.draw(graph3, node_color='lightblue', node_size=800, with_labels=True)
    plt.axis('equal')
    plt.show()

