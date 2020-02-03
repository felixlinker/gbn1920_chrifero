# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:52:41 2019
@author: Arctandra
"""
from bronk_pivot import add_supergraph_nodes
from vertex import Vertex
from edge import Edge
from graph import Graph


def build_mcis_graph(vlist, graph):
    # erstellt Graphen-Objekt aus Liste gematchter Knoten

    new_graph = Graph()
    neighbor_list = []  # speichert alle im new_graph benötigten edges
    for edge in graph.edges:
        neighbor_list.append("("+edge.vertex_a.name+","+edge.vertex_b.name+")")

    # aus der Vlist(enthaelt strings) werden Vertex_objekt erstellt, durch abgleich mit Ursprungsgraphen
    for gv in range(0, len(graph.vertices)):
        if graph.vertices[gv].label is not None and graph.vertices[gv].name in vlist:
            o_vertex = Vertex(name=graph.vertices[gv].name, label=graph.vertices[gv].label)  # TODO: Labels noch nicht getestet
            new_graph.add_vertex(o_vertex)
        elif graph.vertices[gv].label is None and graph.vertices[gv].name in vlist:
            o_vertex = Vertex(name=graph.vertices[gv].name)
            new_graph.add_vertex(o_vertex)

    # Fuer jede Kombination aus Vertices aus New_graph wird durch Abgleich mit der neighbor_list getestet, ob eine
    # Kante erstellt werden soll. ACHTUNG: bisher nur ungerichteter Fall behandelt!
    for v1 in range(0, len(new_graph.vertices)):
        for v2 in range(1, len(new_graph.vertices)):
            if "("+new_graph.vertices[v1].name+","+new_graph.vertices[v2].name+")" in neighbor_list \
                    or "("+new_graph.vertices[v2].name+","+new_graph.vertices[v1].name+")" in neighbor_list:
                new_edge = Edge(new_graph.vertices[v1], new_graph.vertices[v2])
                new_graph.add_edges(new_edge)

    return new_graph


def create_output_table(s1, s2, g_1, g_2, g1, g2, supergraph = False):
    # Last things first: This function creates an output table from the matched nodes after completing the program, which contains
    # the original node names.

    vlist = [] # Liste zum Speichern von gemappten Vertices eines Graphen zur Erstellung eines MCIS-Graphen

    print("The following pairs were found (Graph 1 node; Graph 2 node):")
    if None not in s1:
        for i in range(0, len(s1)):
            if g_1[i] is None or s1[i] is None:
                break
            print("Matching nodes: " + str(g_1[i]) + ' ; ' + str(g_2[s1[i]]))
            vlist.append(g_1[i])
        new_graph = build_mcis_graph(vlist, g1)
        if supergraph == True:
            new_graph = add_supergraph_nodes(new_graph, g1, g2)
        return new_graph

    else:
        for i in range(0, len(s2)):
            if g_1[i] is None or s2[i] is None:
                break
            print("Matching nodes: " + g_1[s2[i]] + ' ; ' + g_2[i])
            vlist.append(g_2[i])
        new_graph = build_mcis_graph(vlist, g2)
        if supergraph == True:
            new_graph = add_supergraph_nodes(new_graph, g1, g2)
        return new_graph


def build_dict(Graph):
    vertex_dict = {}
    for vertex1 in Graph.vertices:  # dict um über den Namen auf das Objekt zugreifen zu können
        vertex_dict.update({vertex1.name: vertex1})

    return vertex_dict


# The next two functions just attempt to compile all followup or preceding nodes of a given vertex into one list.
# This uses the suggested changes to the edge and vertex classes (i.e. keeping a list of following and preceding nodes
# for every given node).
def find_successors(v):
    out = []

    if len(v.successors) != 0:
        for i in range(0, len(v.successors)):

            if v.successors[i].name not in out and v.successors[i].name != v.name:
                # Circular structures in graphs are a thing...I guess? So better keep this in to prevent adding the same index
                # several times.
                out.append(v.successors[i].name)
                #out += find_successors(v.successors[i])

        out2 = []
        for i in range(0, len(out)):
            if out[i] not in out2:
                out2.append(out[i])

        return out2

    else:

        return []


def find_predecessors(v):
    in_ = []

    if len(v.predecessors) != 0:
        for i in range(0, len(v.predecessors)):

            if v.predecessors[i].name not in in_ and v.predecessors[i].name != v.name:
                in_.append(v.predecessors[i].name)
                #in_ += find_predecessors(v.predecessors[i])

        in_2 = []
        for i in range(0, len(in_)):
            if in_[i] not in in_2:
                in_2.append(in_[i])

        return in_2

    else:

        return []


# The next function is mainly used for the alignment of chemical graphs - it ensures that only nodes representing the same type of
# nuclei are mapped onto each other. Can be ignored for other graphs, since their node labels are "None".
def atomic_identity(x, y, g1, g2):
    if g1.vertices[x].label == g2.vertices[y].label:
        return True
    else:
        return False


# The following is the Feasibility function of the Cordella algorithm, required to check, if a proposed matching results in branches,
# that are not mutually exclusive.
def F(s, n, m, g1, g2, v, checklabels):
    depth = get_depth(s)
    if n in s[1] or m in s[0]:
        restore_Datatyp(s, v, depth)
    n_successors = []
    n_predecessors = []
    m_successors = []
    m_predecessors = []
    vertex_dict1 = build_dict(g1)
    vertex_dict2 = build_dict(g2)

    n_successors.append(find_successors(vertex_dict1[n]))  # nachfolger und vorfolger werden gesucht
    n_predecessors.append(find_predecessors(vertex_dict1[n]))
    m_successors.append(find_successors(vertex_dict2[m]))
    m_predecessors.append(find_predecessors(vertex_dict2[m]))
    n_successors = sum(n_successors, [])  # Braucht es, damit keine Listen in Listen gibt
    n_predecessors = sum(n_predecessors, [])
    m_successors = sum(m_successors, [])
    m_predecessors = sum(m_predecessors, [])
    count_n_succ = False  # Booleanwerte
    count_m_succ = False
    count_n_pred = False
    count_m_pred = False
    n_neighbors = n_predecessors + n_successors
    m_neighbors = m_predecessors + m_successors
    n_bool = False
    m_bool = False
    for i in n_neighbors:           # wird geprüft, ob eine Verbindung zwischen m oder n ins Matching besteht
        if i in s[1]:
            n_bool = True
            break
    for q in m_neighbors:
        if q in s[0]:
            m_bool = True
            break
    Tin_n = 0
    Tout_n = 0
    M_n = 0
    Tin_m = 0
    Tout_m = 0
    M_m = 0




    if n_bool or m_bool:    # es wird geprüft, ob eine Verbindung zum Matching besteht

            for x in n_successors:  # guckt, ob alle Nachfolger von n auch ein Äquivalten in m haben
                if s[0][x] is not None:
                        if s[0][x] in m_successors:
                            count_n_succ = True
                        else:
                            count_n_succ = False
                            break
                else:
                        count_n_succ = True

            for y in m_successors:  # guckt, ob alle Nachfolger von m auch ein Äquivalten in n haben
                    if s[1][y] is not None:
                        if s[1][y] in n_successors:
                            count_m_succ = True
                        else:
                            count_m_succ = False
                            break
                    else:
                        count_m_succ = True

            for x in n_predecessors:  # same same
                    if s[0][x] is not None:
                        if s[0][x] in m_predecessors:
                            count_n_pred = True
                        else:
                            count_n_pred = False
                            break
                    else:
                        count_n_pred = True

            for y in m_predecessors:  # same same
                    if s[1][y] is not None:
                        if s[1][y] in n_predecessors:
                            count_m_pred = True
                        else:
                            count_m_pred = False
                            break
                    else:
                        count_m_pred = True

            if len(n_successors) == 0:    #falls es keine Succesoren oder Predecessoren gibt, werden die BolleanCounter
                count_n_succ = True         # auch auf True gesetzt.
            if len(n_predecessors) == 0:
                count_n_pred = True
            if len(m_successors) == 0:
                count_m_succ = True
            if len(m_predecessors) == 0:
                count_m_pred = True

            if count_m_pred and count_n_pred and count_n_succ and count_m_succ:
                if checklabels == False:
                    return True
                elif vertex_dict1[n].label == vertex_dict2[m].label:
                    return True
                else:
                    return False
    else:
            for i in range(0, len(s[0])):  # Berechnet die Knoten im Matching und in T_in und T_out
                    if s[0][i] is not None:
                        M_n += 1
                    if s[2][i] != 0 and s[0][i] is None:
                        Tout_n += 1
                    if s[4][i] != 0 and s[0][i] is None:
                        Tin_n += 1

            for i in range(0, len(s[1])): # same same für M2
                    if s[1][i] is not None:
                        M_m += 1
                    if s[3][i] != 0 and s[1][i] is None:
                        Tout_m += 1
                    if s[5][i] != 0 and s[1][i] is None:
                        Tin_m += 1

            N_n = (len(g1.vertices) - M_n - Tin_n - Tout_n)
            N_m = (len(g2.vertices) - M_m - Tin_m - Tout_m)

            if Tout_n >= Tout_m and Tin_n >= Tin_m and N_n >= N_m:
                if checklabels == False:
                    return True
                elif vertex_dict1[n].label == vertex_dict2[m].label:
                    return True
                else:
                    return False


    return False

def restore_Datatyp(s, v, depth): # es werden s, v (das zuletzt hinzugefügte Paar und die Tiefe übergeben
    s_restored = s
    if v[0] in s_restored[0]:           # es wird das letzte Paar wieder auf None gesetzt
        s_restored[0][s_restored[0].index(v[0])] = None

    if v[1] in s_restored[1]:           # same
        s_restored[1][s_restored[1].index(v[1])] = None

    if depth in s_restored[2]:    # es werden alle Werte, die hinzugefügt werden über die Depth wieder auf Null gesetzt
        for i in range(0, len(s)):  #für alle Vektoren s[2]-s[5]
            if s_restored[2][i] == depth:
                s_restored[2][i] = 0

    if depth in s_restored[3]:    #same
        for i in range(0, len(s)):
            if s_restored[3][i] == depth:
                s_restored[3][i] = 0

    if depth in s_restored[4]:    #same
        for i in range(0, len(s)):
            if s_restored[4][i] == depth:
                s_restored[4][i] = 0

    if depth in s_restored[5]:    #same
        for i in range(0, len(s)):
            if s_restored[5][i] == depth:
                s_restored[5][i] = 0

    return s_restored

# A function that generates potential matching candidates from the remaining unmapped parts of the graph.
def P(s, g1, g2):
    T1_out = []
    T2_out = []
    T1_in = []
    T2_in = []
    for i in range(0, len(s[2])): # gibt nur die Kandidaten aus die in den Vektoren s[2]-s[5] und nicht im Mtaching sind
        if s[2][i] is not 0 and s[0][i] is None:
            T1_out.append(i)

    for i in range(0, len(s[3])):   #same
        if s[3][i] is not 0 and s[1][i] is None:
            T2_out.append(i)

    for i in range(0, len(s[4])):   #same
        if s[4][i] is not 0 and s[0][i] is None:
            T1_in.append(i)

    for i in range(0, len(s[5])):   #same
        if s[5][i] is not 0 and s[1][i] is None:
            T2_in.append(i)

    # Empty lists are considered False in python.
    if len(T1_out) != 0 and len(T2_out) != 0:
        return [T1_out, min(T2_out)]
    # Reminder that the node names have to be parsed to indices (as integers) for this to work.
    elif len(T1_in) != 0 and len(T2_in) != 0:
        return [T1_in, min(T2_in)]

    else:
        N1 = []
        N2 = []

    for n in g1.vertices:
        if n.name not in s[1]:
            N1.append(n.name)

    for m in g2.vertices:
        if m.name not in s[0]:
            N2.append(m.name)

    return [N1, min(N2)]

def get_depth(s):       # gibt die Tiefe zurück aka die Anzahl der gemachten Paare
    depth = 0
    for n in range(0, len(s[0])):
        if s[0][n] is not None:
            depth += 1
    return depth

# The core function of the Cordella algorithm - loops until one graph is successfully mapped onto the other.
def match(s, g1, g2, v, checklabels):
    # First we have to fill the predecessor and successor vectors.
    match_return = [None, None, False]
    depth = get_depth(s)
    match_made = False

    # print("Start matching round.")
    if None not in s[0] or None not in s[1]:
        # Since we assume a graph-graph or a graph-subgraph isomorphism, if either core_1 or core_2 are completely filled,
        # we can consider the matching process to be complete. Furthermore, one of the two has to be filled by the end.
        t = True
        return [s[0], s[1], t]

    else:
        # If someone has an idea how to do this without dragging g1, g2 into every new function, let me know.
        p = P(s, g1, g2)
        # I propose for simplicity to save the candidates returned by P(s) in two vectors (one containing all values of n,
        # one containing the value of m), which are then saved in the two-dimensional vector p. This way, we do not have
        # to save the carthesian product, because it implicitly follows from looping over all values n (m seems to always
        # be one value anyways). Careful, these have to be indices.
        for n in p[0]:
            if None not in s[0] or None not in s[1]:
                break
            if F(s, n, p[1], g1, g2, v, checklabels):
                # The following just adds the indices of the newly matched nodes in the right positions in the core_1, core_2
                # vectors...
                s[0][n] = p[1]
                s[1][p[1]] = n
                v = [p[1], n]
                depth = get_depth(s)
                match_made = True
                # Now we have to update the lists of successors and predecessors, that is we add all successors and
                # predecessors
                # of the newly matched nodes that are not themselves matched:
                for a in find_successors(g1.vertices[n]):
                    if s[0][a] == None and a not in s[2]:
                        s[2][a] = depth

                for a in find_successors(g2.vertices[p[1]]):
                    if s[1][a] == None and a not in s[3]:
                        s[3][a] = depth

                for a in find_predecessors(g1.vertices[n]):
                    if s[0][a] == None and a not in s[4]:
                        s[4][a] = depth

                for a in find_predecessors(g2.vertices[p[1]]):
                    if s[1][a] == None and a not in s[5]:
                        s[5][a] = depth

                match_return = match(s, g1, g2, v, checklabels)

        if match_return[2] is not True: # prüft, ob ein Graph vollständig auf den anderen gemacht worden ist.
            if match_made: # Falls im letzen Schritt ein Match gemacht worden ist, wird dieser Rückgängig gemacht
                return restore_Datatyp(s, v, depth)
            else:
                return s
        else:
            return match_return


# def initialize_match(s, g1, g2):
#     # Basically, to save computation time later on, we have the program identify the first pair of matching nodes and then
#     # immediately calculate all predecessors and successors of these two nodes. These lists will then be updated with each
#     # future addition to the core_1 and core_2 vectors by removing the new matching nodes from the in_1, in_2, ou_1, out_2 vectors.
#     print("Initialize first match...")
#     found = False
#     v = []
#     for n in g1.vertices:
#         if found:
#             break
#         for m in g2.vertices:
#
#             if F(s, n.name, m.name, g1, g2, v):
#
#                 # Here, the nodes that are predecessors or successors of a matched node are added to the respective vectors
#                 print("Found one")
#                 s[0][n.name] = g2.vertices[0].name
#                 s[1][g2.vertices[0].name] = n.name
#
#                 succ_n = find_successors(n)  # Vektoren s[2]-[5] werden mit 1 befüllt falls es ein Nachbar ist.
#                 for i in range(0, len(succ_n)):
#                     s[2][succ_n[i]] = 1
#
#                 succ_m = find_successors(m)
#                 for i in range(0, len(succ_m)):
#                     s[3][succ_m[i]] = 1
#
#                 pred_n = find_predecessors(n)
#                 for i in range(0, len(pred_n)):
#                     s[4][pred_n[i]] = 1
#
#                 pred_m = find_predecessors(m)
#                 for i in range(0, len(pred_m)):
#                     s[5][pred_m[i]] = 1
#                 found = True
#                 v = [g2.vertices[0].name, n.name]
#                 break
#
#     if found:
#         return match(s, g1, g2, v)
#     else:
#         print("No initial match found.")


def Cordella(g1, g2, supergraph = False, checklabels=False):
    # For...."Implementation reasons"....if the graphs are not equal in size, the first one must be the bigger one. Otherwise, the
    # Feasibility function will act up. Therefore, if g1 is smaller than g2, their positions are swapped.
    if len(g1.vertices) < len(g2.vertices):
        g1_temp = g1
        g1 = g2
        g2 = g1_temp

    # This should probably be changed later on, but we have to give our nodes unifiying names for comparability. But if we need
    # the names later on (for chemical graphs), here they are:
    hold_g1 = []
    hold_g2 = []
    # hold_g1.append(None)
    # hold_g2.append(None)

    for i in range(0, len(g1.vertices)):
        hold_g1.append(g1.vertices[i].name)
        g1.vertices[i].name = int(i)

    for i in range(0, len(g2.vertices)):
        hold_g2.append(g2.vertices[i].name)
        g2.vertices[i].name = int(i)

    # Initialize core_1, core_2 where indices of corresponding matched node is saved
    print("Initialize...")
    print(len(g1.vertices))
    core_1 = [None] * len(g1.vertices)
    core_2 = [None] * len(g2.vertices)
    # Initialize in_1, out_1 and in_2, out_2 as empty - since there are no nodes matched right now, it is impossible
    # to define predecessor or successor nodes at initialization.
    in_1 = [0] * len(g1.vertices)
    in_2 = [0] * len(g2.vertices)
    out_1 = [0] * len(g1.vertices)
    out_2 = [0] * len(g2.vertices)

    # We shall save these 6 vectors as a list to simplify the assignment of values. It would be paramount to
    # never change their order, please. As in, never ever.
    s = [core_1, core_2, out_1, out_2, in_1, in_2]
    print("Initialize complete.")
    v = []
    # Call the Matching function
    cord = match(s, g1, g2, v, checklabels)

    # Make use of the output:
    if cord == None:
        print("Invalid pairs - no isomorphism could be found.")
    else:
        for i in range(0, len(g1.vertices)):
            g1.vertices[i].name = hold_g1[i]

        for i in range(0, len(g2.vertices)):
            g2.vertices[i].name = hold_g2[i]

        return create_output_table(cord[0], cord[1], hold_g1, hold_g2, g1, g2, supergraph)
