#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module contient des fonctions permettant de construire un arbre minimal de steiner.

"""


import matplotlib.pyplot as plt
import networkx as nx
import copy


def based_chen(G,src,D):

    """

    Algorithme de Yen Hung Chen(An Improved Approximation Algorithm for the Terminal Steiner Tree Problem,2011):

    * Utiliser la fonction base_kou pour généer l'arbre de Steiner S, s'il ne convient(presence de noeud destination non feuille) pas alors
    * Utiliser l'algorithme 1(de transformation de l'arbre de steiner S en un arbre de Steiner terminal(tout noeud destination est feuille)

    Parameters
    ----------
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté dont il faut pour construire un arbre
    src: str
        la source de l'arbre
    D: list
        liste des noeuds terminaux
    Returns
    -------
    networkx.classes.graph.Graph
        l'arbre de Steiner terminal ou None

    """
    # Chen considère que le graphe ne contient pas de lien entre noeuds destination
    # Donc supprimons ces liens eventuels
    copyG = G.copy()
    gCopy_edges = copyG.edges()
    for i in range(0, len(D)):
        for j in range(0, len(D)):
            if (D[i] != D[j]) and (D[i], D[j]) in gCopy_edges:
                copyG.remove_edge(D[i], D[j])
    print("copyG CHEN", copyG.nodes(True))
    S = based_kou(copyG, src, D)
    if S is not None:
        D_not_lead = terminal_not_leaf(S, D)
        if len(D_not_lead) == 0:
            print("ARBRE DE STEINER GENERAL", S.edges())
            return S
        else:
            print("ARBRE DE STEINER GENERAL", S.edges())
            S = make_tst(S, src, D_not_lead, G)
            plt.figure()
            nx.draw(S, with_labels=True, font_weight='bold')
            plt.savefig("TfinalS.png")
            plt.close()
            print("ARBRE DE STEINER TERMINAL", S.edges())
            return S
    else:
        return None


def terminal_not_leaf(S, D):

    """

    Permet de tester si un arbre de Steiner est un arbre de steiner terminal. Autrement dit, est-ce que tous
    les noeuds terminaux ppartenant à D sont des noeuds feuilles de S

    Parameters
    ----------
    S: str
        source de l'arbre de steiner à tester
    D: list
        liste des noeuds terminaux
    Returns
    -------
    list
        liste des noeuds terminaux non feuille
    """
    # Récupérer la liste des noeuds terminaux non feuilles(donc de degré supérieur à 1)
    # Le dégré du noeud est son nombre de voisins ou nombre de liens adjacents à ce noeud
    return [node for (node, degree) in S.degree() if node in D and degree > 1]


def make_tst(S, src, not_leaf_set, G):
    """

    Implementation de l'algoritme 1 de Chen  permettant de transformer un arbre de steiner non terminal
    en arbre de steiner terminal

    Parameters
    ----------
    S: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté qu'il faut rendre en arbre de steiner terminal
    src: str
        la source de l'arbre à construire
    not_leaf_set: list
        liste des noeuds terminaux non feuilles
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté qu'il faut rendre en arbre de steiner terminal
    Returns
    -------
    networkx.classes.graph.Graph
        Un arbre

    """

    s_edges = S.edges()
    # Pour chaque noeud terminal non feuille r de S :
    print("not_leaf_set", not_leaf_set)
    for r in not_leaf_set:
        # 1. Supprimer tout les liens de S entre r et ses voisins sauf celui entre r et sont plus proche voisin nr
        ns_r = list(S.neighbors(r)) # liste des voisins de r
        # Liste des liens de adjacents à r dans S
        star_r = [edge if edge[0] == r and edge[1] in ns_r else (edge[1], edge[0])if edge[1] == r and edge[0] in ns_r else 'no edge of star_r' for edge in  s_edges]
        while 'no edge of star_r' in star_r: star_r.remove('no edge of star_r')
        print("star de r", r, star_r)
        # Choisir le plus proche voisin de r au sens d'une metrique donnée
        # Supposons que tous les liens du graphe ont la même valuation
        # nr sera la source src ou le premier voisin de r different de src
        nr = ''
        if src in ns_r:
            nr = src
        else:
            nr = ns_r[0]
        print("nr", nr)
        # Supprimer les liens de star_r ne contenant pas un lien reliant nr et r
        star_r_subset = [edge for edge in star_r if edge != (nr, r) and edge != (r, nr)]
        S.remove_edges_from(star_r_subset)
        print("star de r subset", r, star_r_subset)
        # 2. Achever la construction de S
        # 2-1. Constuire le sous-graphe induit Gns_r de G
        Gns_r = G.subgraph(ns_r)
        print("Sous graphe depuis r ", r, Gns_r.edges())
        subgraph = nx.Graph()
        subgraph.add_nodes_from(ns_r)
        subgraph.add_edges_from(Gns_r.edges())
        # 2-2. Construire l'arbre couvrant minimum au sens de prim de Gns_r
        min_span_tree_Gns_r = nx.minimum_spanning_tree(subgraph, weight='weight', algorithm='prim')
        print("Tree de r", r, min_span_tree_Gns_r.edges())
        # 2-3. Ajouter tous les liens de min_span_tree_Gns_r à S
        S.add_edges_from(min_span_tree_Gns_r.edges())
    return S


def based_kou(G, src, D, algo ="prim"):

    """

    modification de l'algo de Kou et al (Fast Algorithm for Steiner Trees,1981)
    afin de garantir que tous les noeuds destiantaires sont des neouds feuilles de l'arbres.
    Nous utilisons l'algo de prim par défaut  pour la recherche d'arbre couvrant

    Parameters
    ----------
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté dont il faut pour construire un arbre
    src: str
        la source de l'arbre
    D: list
        liste des noeuds terminaux
    algo: str
        c'est prim ou kruskal
    Returns
    -------
    networkx.classes.digraph.DiGraph
        un arbre minimal de steiner

    """

    # 1. construction du graphe complet
    G1_nodes = []
    G1_nodes.append(src)
    G1_nodes.extend(D)
    print(G1_nodes)
    # 1-1. Creation du graphe complet
    G1 = complete_graph(G1_nodes)
    print("Avant", G1.edges())
    if G1 is not None:
        plt.figure()
        nx.draw(G1, with_labels=True, font_weight='bold')
        plt.savefig("comp_graph.png")
        # 1-2. Les plus courts chemins de G entre les liens de G1
        all_paths = dict()
        for edge in G1.edges():
            copy_nodes_G1 = copy.deepcopy(G1_nodes)
            copy_nodes_G1.remove(edge[0])
            copy_nodes_G1.remove(edge[1])
            all_paths[(edge[0], edge[1])] = nx.shortest_path(G, edge[0], edge[1])
        print(all_paths)
        # 1-3. Ajouter  un poids à chaque arc de G1
        for key, value in all_paths.items():
            print(key)
            G1[key[0]][key[1]]['weight'] = len(value)
        plt.figure()
        nx.draw(G1, with_labels=True, font_weight='bold')
        plt.savefig("comp_graph2.png")
        print("Apres", G1.edges())
        #for e in G1.edges():
            #print(e, G1.get_edge_data(e[0],e[1]))
        # 2. Construction d'un arbre couvrant à l'aide de prim
        #D_is_leaf = True
        T1 = nx.minimum_spanning_tree(G1, weight='weight', algorithm=algo)
        print("MONT1", T1.edges())
        plt.figure()
        nx.draw(T1, with_labels=True, font_weight='bold')
        plt.savefig("T1.png")
        # 3. Initialisation de l'arbre
        T = nx.Graph()  # L'arbre à construire
        set_nodes_T = set()
        set_edges_T = set()
        # 4. Ajout des noeuds intermédaires
        # 4-1. Pour chaque lien de T1 faire
        for edge in T1.edges():
            shortest_path = []
            try:
                # Source probable de bug
                shortest_path = all_paths[edge] #trouver le plus court chemin dans G reliant edge[0] et edge[1]
            except KeyError :
                print("FAUSSE CLE DONC L'INVERSE EST DANS ALL_PATHS")
                shortest_path = all_paths[(edge[1], edge[0])]  # trouver le plus court chemin dans G reliant edge[0] et edge[1]
            print("short", shortest_path)
            #print(edge, shortest_path)
            if len(set_nodes_T) == 0: #Si l'arbre est vide alors on ajoute tout les noeuds à l'arbre
                print("vide")
                set_nodes_T.update(shortest_path)
                for i in range(0,len(shortest_path) -1):
                    #Ajout des liens de shortest Path aux liens de T
                    set_edges_T.add((shortest_path[i], shortest_path[i+1]))
                print("set_edges", set_edges_T)
            else:
                set_p = set(shortest_path)
                print("t",set_nodes_T)
                print("p", set_p)
                print("Intersection", set_p.intersection(set_nodes_T))
                # 4-2. Si shortest path ne contient pas moins de 2 noeuds dans T alors ajouter le chemin à T
                if len(set_p.intersection(set_nodes_T)) < 2:
                    print("<2")
                    set_nodes_T.update(shortest_path)      #Ajouter les noeuds non présent encore dans T
                    for i in range(0, len(shortest_path) - 1):
                        if ((shortest_path[i], shortest_path[i + 1]) not in set_edges_T) and ((shortest_path[i+1], shortest_path[i]) not in set_edges_T):
                            set_edges_T.add((shortest_path[i], shortest_path[i + 1]))    # Ajout des liens de shortest Path aux liens de T
                    print("set_edges", set_edges_T)
                else:
                    print(">=2")
                    set_nodes_T.update(shortest_path)
                    #Sinon soit pi et pj respectivement le premier et le dernier element de shortest Path dans T
                    pi = ''
                    for i in range(1, len(shortest_path) - 1):
                        if shortest_path[i] in set_nodes_T:
                            pi = shortest_path[i] #pi doit être different de shortest_path[0]
                            print("pi", pi)
                            break
                    pj = ''
                    l = [] #shortest path ren
                    l = copy.deepcopy(shortest_path)
                    l.reverse()
                    for j in l:
                        if j in set_nodes_T and j != shortest_path[-1]:
                            pj = j                           #pj doit être different de shortest_path[-1]
                            print("pj", pj)
                            break
                    #Ajout du sous-chemin de shortest_path[0] à pi
                    for i in range(0, len(shortest_path) - 1):
                        # Ajout des liens de shortest Path aux liens de T
                        if ((shortest_path[i], shortest_path[i + 1]) not in set_edges_T) and ((shortest_path[i+1], shortest_path[i]) not in set_edges_T):
                            set_edges_T.add((shortest_path[i], shortest_path[i + 1]))
                            if shortest_path[i + 1] == pi:
                                break
                    # Ajout du sous-chemin de pj à shortest_path[-1] l
                    for i in range(0, len(l) - 1):
                        # Ajout des liens de shortest Path aux liens de T
                        if ((l[i+1], l[i]) not in set_edges_T) and ((l[i], l[i+1]) not in set_edges_T):
                            set_edges_T.add((l[i+1], l[i]))
                            if l[i + 1] == pj:
                                break
                    print("set_edges", set_edges_T)
        # 5. Construire T
        print("set_nodes", set_nodes_T)
        print("set_edges", set_edges_T)
        T.add_nodes_from(list(set_nodes_T))
        for n in list(set_nodes_T):
            T.nodes[n]['is_wcn'] = G.nodes[n]['is_wcn']
        T.add_edges_from(list(set_edges_T))
        plt.figure()
        nx.draw(T, with_labels=True, font_weight='bold')
        plt.savefig("TfinalT.png")
        return T
    else:
        return None


def complete_graph(nodes=[]):

   """

   Créer un graphe complet entre les noeuds de nodes

   Parameters
    ----------
    nodes : list
        les noeuds du graphe complet à construire
    Returns
    -------
    networkx.classes.graph.Graph
        Un graphe complet

   """
   comp_graph = nx.Graph()
   comp_graph.add_nodes_from(nodes)
   edges_list = []
   try:
       for source in nodes:
           for target in nodes:
               if source != target:
                   if (source, target) not in edges_list and (target, source) not in edges_list:
                       edges_list.append((source, target))
       comp_graph.add_edges_from(edges_list)
       return  comp_graph
   except Exception as exc:
       print(exc.__cause__)
       return  None


def based_Takahashi(G, src, D):
    """
     modification de l'algo de Takahashi et al (An approximate solution
      for the Steiner problem in graphs,1980)

    Parameters
    ----------
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté qu'il faut rendre en arbre de steiner terminal
    src: str
        source de l'arbre de steiner à construire
    D: list
        liste des noeuds terminaux
    Returns
    -------
    networkx.classes.graph.Graph
        arbre de steiner

    """
    pass


def based_Smith(G, src, D):

    """
    modification de l'algo de Takahashi et al(The computation of nearly minimal Steiner trees in graphs,1983)

     Parameters
    ----------
    G: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        Le graphe non orienté qu'il faut rendre en arbre de steiner terminal
    src: str
        source de l'arbre de steiner à construire
    D: list
        liste des noeuds terminaux
    Returns
    -------
    networkx.classes.graph.Graph
        arbre de steiner

    """
    pass







