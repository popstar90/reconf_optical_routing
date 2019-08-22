#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module contient des fonctions permettant de construire un arbre des plus courts chemin.

"""
import networkx as nx
from helper.queue import adaptable_heap_priority_queue as hq


def based_dijkstra(G=nx.Graph(), src='',wave=0):

    """

    Extension de l'algo dijkstra pour l'arbre des plus courts chemins à partir de G et de source *src* :
    *Construction des chemins vers chaque destinations
    *Puis creation de l'arbre des plus court chemins en eliminant les liens qui
    se repètent

    Parameters
    ----------
    G:  `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté dont il faut pour construire un arbre
    src: str
        la source de l'arbre
    wave: int
         la longueur d'onde à attribuer à l'arbre
    Returns
    -------
    networkx.classes.digraph.DiGraph
        un arbre orienté enraciné en src et couvrant tout les noeuds de G

    See Also
    --------
    based_bellman



    """
    gcopy = G.copy()
    weight_dict = dict()  # weight_dict[u] est une borne sup de la distance de la source s à u
    cloud_dict = dict()   # la clé est u et la valeur vaut weight_dict[u]
    pq = hq.AdaptableHeapPriorityQueue()  # valeur u et la clé est  weight_dict[u]
    pqlocator_dict = dict()  # Faire correspondre un noeud u à sa position dans pq
    pred_dict = dict()
    nodes = list(gcopy.nodes())
    for i in nodes:
        if i == src:
            weight_dict[i] = 0
        else:
            weight_dict[i] = float('inf')
        pred_dict[i] = None
        pqlocator_dict[i] = pq.add(weight_dict[i], i)
    mytree = nx.DiGraph(wavelength=wave)  # L'arbre à construire)
    nodes_set = set()
    edges_set = set()
    while not pq.is_empty():
        weight, u = pq.remove_min()
        nodes_set.add(u)
        cloud_dict[u] = weight
        del pqlocator_dict[u]
        u_neighbors = list(nx.neighbors(gcopy, u))
        print(u+' neighbors', u_neighbors)
        print("nodes_set", nodes_set)
        for v in u_neighbors:
            if v not in nodes_set:
                if weight_dict[v] > weight_dict[u] + 1:
                    weight_dict[v] = weight_dict[u] + 1
                    pq.update(pqlocator_dict[v], weight_dict[v], v)
                    pred_dict[v] = u
        print("pred_dict current", pred_dict)
        # if len(nodes_set) == len(list(gcopy.nodes())):
            # break
    nodes_list = list(nodes_set)
    mytree.add_nodes_from(nodes_list)
    for key, value in pred_dict.items():
        if key != src and key in nodes_list:  # car pred_dict[src] = None donc on veut pas de edge du style (None, src)
            edges_set.update({(value, key)})
    edges_list = list(edges_set)
    mytree.add_edges_from(edges_list)
    for n in G.nodes():
        if n in mytree.nodes():
            mytree.nodes[n]['node_data'] = G.nodes[n]['node_data']
    for e in edges_list:
        try:
            mytree[e[0]][e[1]]['edge_data'] = G[e[0]][e[1]]['edge_data']
        except:
            try:
                mytree[e[0]][e[1]]['edge_data'] = G[e[1]][e[0]]['edge_data']
            except:
                print("pred_dict", pred_dict)
                print("nodes_tree", nodes_list)
                print("e", e)
                print("edges_tree", edges_list)
                print("G edges", list(G.edges()))
                print("ECHEC DE L'AJOUT DES INFOS DE LIENS APRES DIJKSTRA")
                exit(0)
    print("DIJSKRTA !!!!")
    print("Nodes", mytree.nodes(data=True))
    print('Edges', mytree.edges(data=True))
    print('Wavelength', mytree.graph)
    print("ARBORESCENCE", nx.is_arborescence(mytree))
    return mytree


def based_bellman(G, src):
    """

    Fonction basé  retournant  l'arbre des plus courts chemins basé sur l'algorithme de bellman

    Parameters
    ----------
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté dont il faut pour construire un arbre
    src: str
        la source de l'arbre
    Returns
    -------
    networkx.classes.digraph.DiGraph
        un arbre orienté enraciné en src et couvrant tout les noeuds de G

    See Also
    --------
    based_dijkstra

    """
    tree = nx.DiGraph()
    # Contenu à ajouter
    return tree