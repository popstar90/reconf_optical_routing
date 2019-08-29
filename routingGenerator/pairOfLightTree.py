#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module contient des fonctions permettant de construire une paire d'arbres mono-optiques.

"""

import random
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from pathlib import Path
from helper import nodeTreeProperty as ntp
from helper import customRandom as cr
from routingGenerator import shortest_path_tree as spt
from routingGenerator import min_spanning_tree as mst

class PairOfLightTree:

    """

    Classe chargée de créer une paire d'arbres mono-optiques

    Parameters
     ----------
     g: `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
        le graphe du réseau

     Examples
     --------

     >>> net = nx.Graph() # net devra etre le graphe obtenu après avoir chargé le fichier gml adéquat en realité
     >>> route_pair = PairOfLightTree(net)
    """

    def __init__(self, g=nx.Graph()):

        """
         constructeur de la classe

        """
        self.graph = g


    def generate(self):

        """

        Génère une  paire d'arbres mono-optiques.

        Returns
        -------
        tuple
            paire d'arbres mono-optiques
        """
        # 1.Choisir la source de la paire d'arborescences par loi uniforme
        nodes_list = list(self.graph.nodes())  # Liste des noeuds
        source_index = str(cr.pick_one_numbers_uniformly(int(min(nodes_list)), int(max(nodes_list))))
        #print("src", source_index)
        #choisir aléatoirement la longueur d'onde à affecter aux liens
        wave = cr.pick_one_numbers_uniformly(0, 15)
        # 2 Construire l'arbre initial avec dijkstra
        # 2.1. Construire l'arbre des plus courts chemins de source_index vers les autres noeuds du graphe
        temp_initial_route = spt.based_dijkstra(self.graph, source_index,wave)
        # 2.2 Construire l'arbre minimum de steiner avec prim pour le graphe entier avec pour source source_index
        temp_final_route = mst.span_tree(self.graph, source_index,wave)
        # 2.2 Rechercher l'ensemble des feuilles de  l'arbre initial D1
        D1 = ntp.all_leafs(temp_initial_route)
        #print("D1", D1)
        # 2.3  Rechercher l'ensemble des feuilles D2 de  l'arbre final
        D2 = ntp.all_leafs(temp_final_route)
        #print("D2", D2)
        # Choisir aléatoirement au moins 50% des feuilles appartenant à D1 et D2 noté D comme destinations de la paire d'arbres
        D_intersec = list(D1.intersection(D2))
        # choisir uniformément au moins 50% de D comme destinations de la paire
        #print("INF", int(200/len(D_intersec)))
        Dpercent = cr.pick_one_numbers_uniformly(int(200/len(D_intersec)), 100)
        D = cr.pick_random_numbers(D_intersec, Dpercent)
        D = [str(i) for i in D]
        #print("DESTINATIONS SET", D)
        # for (i,j) in coproute.edges():
        # if i
        initial_route = ntp.subtree(temp_initial_route, source_index, D)
        #print('INIT', list(initial_route.edges(data=True)), nx.is_tree(initial_route))
        # for n in nodes:
        # initial_route.nodes[n]['node_data'] = temp_initial_route.nodes[n]['node_data']
        final_route = ntp.subtree(temp_final_route, source_index, D)
        #print('FINAL', list(final_route.edges(data=True)), nx.is_tree(final_route))
        #print("nodes data PairOflightTree")
        #for (n, data) in initial_route.nodes(data=True):
            #print(n,data)
        #colors = [n+'gray' if data['node_data']['wcn'] == True else n+'white' for (n, data) in initial_route.nodes(data=True)]
        t0 = nx.drawing.nx_pydot.to_pydot(initial_route)
        #for i, node in enumerate(t0.get_nodes()):
            #for i in range(0,len(colors)):
                #arret = False
                #if colors[i][0] == node:
                    #node.set_color(colors[i][1:])
                    #arret = True
                    #break
            #if arret:
                #break
            #node.set_color(colors[col])
        t0.write_png('initial.png')
        #plt.figure()
        #pos_initial =graphviz_layout(initial_route, prog='dot')
        #nx.draw(initial_route, pos_initial, node_color=colors, with_labels=True, font_weight='bold')
        #path = Path(__file__).resolve().with_name("initial.png")
        #plt.savefig(str(path))
        #plt.close()
        #colors = ['gray' if data['node_data']['wcn'] == True else 'white' for (n, data) in final_route.nodes(data=True)]
        #plt.figure()
        tz = nx.drawing.nx_pydot.to_pydot(final_route)
        tz.write_png('final.png')
        #pos_final = graphviz_layout(final_route, prog='dot')
        #nx.draw(final_route, pos_final, node_color=colors, with_labels=True, font_weight='bold')
        #path = Path(__file__).resolve().with_name("final.png")
        #plt.savefig(str(path))
        #plt.close()
        print(" paire_of_lightree_generated")
        return initial_route, final_route