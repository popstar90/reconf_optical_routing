"""
Propriétés de noeuds de graphe
"""

import networkx as nx


def is_leaf(g=nx.DiGraph(), node=""):
    """
    Un noeud différent de la source est un noeud feuille si son dégré vaut 1
    :param g:
    :param node:
    :return:
    """
    #if len(nx.predecessor(g, node)) == g.degree(node) == 1:
    if g.out_degree(node)  == 0 and g.in_degree(node)==1:
        return True
    else:
        return False


def all_leafs(g=nx.DiGraph):
    leafs_set = set()
    for n in g.nodes():
        if is_leaf(g, n):
            leafs_set.add(n)
    return leafs_set


def subtree(T=nx.DiGraph(), src="", D=[] ):
    """
    Sous arbre 
    :param T:
    :param src:
    :param D:
    :return:
    """
    tcopy = T.copy()
    w = tcopy.graph
    #mytree = nx.DiGraph(wavelength=w['wavelength'])  # L'arbre à construire) A remetrre à la fin de mes tests
    mytree = nx.DiGraph()  # L'arbre à construire) # aa enlever à la fin de mes tests
    nodes_set = set([src]+D)
    edges_set = set()
    for i in D:
        path = nx.shortest_path(tcopy, src, i)
        edges_i_set = set()
        for i in range(0, len(path) - 1):
            edges_i_set.update({(path[i], path[i+1])})
        edges_set.update(edges_i_set)
    nodes_list = list(nodes_set)
    edges_list = list(edges_set)
    print(edges_list)
    mytree.add_nodes_from(nodes_list)
    mytree.add_edges_from(edges_list)
    #for n in mytree.nodes():
        #if n in T.nodes():
            #mytree.nodes[n]['node_data'] = T.nodes[n]['node_data']
    #for e in edges_list:
        #try:
            #mytree[e[0]][e[1]]['edge_data'] = T[e[0]][e[1]]['edge_data']
        #except:
            #print("ERREUR!!!")
    print("Nodes", mytree.nodes(data=True))
    print('Edges', mytree.edges(data=True))
    #print('Wavelength', mytree.graph)
    print("ARBORESCENCE", nx.is_arborescence(mytree))
    return mytree


