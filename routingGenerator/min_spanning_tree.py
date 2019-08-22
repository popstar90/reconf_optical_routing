#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module contient des fonctions permettant de construire un arbre couvrant de poids minimal.

"""

import networkx as nx


def span_tree(g=nx.Graph(), src="", wave=0, algo="prim"):
    """
    Extension de l'algo de prim ou de kruskal pour l'arbre couvrant de poids minimal:

    * construction de l'arbre couvrant de G avec Prim
    * puis créer l'arbre en prenant le chemin entre la sourve et chaque destination sur l'arbre couvrant

    Parameters
    ----------
    g: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté dont il faut pour construire un arbre
    src: str
        la source de l'arbre
    algo: str
        c'est prim ou kruskal
    Returns
    -------
    networkx.classes.digraph.DiGraph
        un arbre couvrant minimal
    """
    tree_edges = []                       # Liste des liens de l'arbre à construire
    tree_nodes = []                        # Liste des noeuds de l'arbre à construire
    # tree_nodes.append(src)
    # tree_nodes.extend(D)
    edges_set = set()
    nodes_set = set()
    min_span_tree = nx.minimum_spanning_tree(g, weight='weight', algorithm=algo)
    D = list(g.nodes())
    for d in D:
        if d != src:
            branch = nx.shortest_path(min_span_tree, src, d)
            branch_edges = []
            for i in range(0, len(branch) - 1):
                branch_edges.append((branch[i], branch[i + 1]))
                nodes_set.update([branch[i], branch[i + 1]])
            edges_set.update(branch_edges)
    tree_edges = list(edges_set)
    tree_nodes = list(nodes_set)
    tree = nx.DiGraph(wavelength=wave)
    tree.add_nodes_from(tree_nodes)
    tree.add_edges_from(tree_edges)
    for n in tree_nodes:
        tree.nodes[n]['node_data'] = g.nodes[n]['node_data']
    for e in tree_edges:
        try:
            tree[e[0]][e[1]]['edge_data'] = g[e[0]][e[1]]['edge_data']
        except:
            tree[e[0]][e[1]]['edge_data'] = g[e[1]][e[0]]['edge_data']
    print("PRIM !!!!")
    print("Nodes", tree.nodes(data=True))
    print('Edges', tree.edges(data=True))
    print('Wavelength', tree.graph)
    print("ARBORESCENCE", nx.is_arborescence(tree))
    return tree
