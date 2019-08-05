#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module permet de nous faire connaitre les noeuds choisis qui pourront effectuer la conversion de
longueur d'onde.

"""


import networkx as nx
from helper import customRandom as cr
import copy


class Placement:

    """

    Classe qui réseau le problème de placement des convertisseurs de longueur d'onde.

    """
    def __init__(self, wcn_min_node_percent=50, wcn_max_node_percent=75, algo="random"):
        self.wcn_min_node_percent = wcn_min_node_percent
        self.wcn_max_node_percent = wcn_max_node_percent
        self.algo = "algo_"+algo

    def assign(self, g=nx.Graph()):
        """

        Affecte les convertisseurs de longueurs d'onde aux noeuds dans une certaine proportion grace à un
        processus aléatoire.

        Parameters
        ----------
        g:  `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
            le graphe du réseau
        Returns
        -------
        networkx.classes.graph.Graph
            retourne ma méthode à utiliser pour le placement des convertissuers.
        """
        graph = copy.deepcopy(g)
        method = getattr(self, self.algo, lambda: self.algo)
        return method(graph)

    def algo_random(self, graph=nx.Graph()):

        """

        Algorithme  permettant de choisir aléatoirement des noeuds pour leur octroyer la capacité de conversion.

        Parameters
        ----------
        g:  `networkx.classes.graph.Graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_
            le graphe du réseau
        Returns
        -------
        networkx.classes.graph.Graph
            retourne un graphe `networkx.classes.graph <https://networkx.github.io/documentation/stable/reference/classes/graph.html>`_

        """

        # Choix du nombre de convertisseurs
        choice_of_wcn_number = 0 #nwcn
        if self.wcn_min_node_percent != self.wcn_max_node_percent: #swcn
            choice_of_wcn_number = cr.pick_one_numbers_uniformly(self.wcn_min_node_percent, self.wcn_max_node_percent)
        elif self.wcn_min_node_percent == 100:
            choice_of_wcn_number = 100
        print('choice_of_wcn_number', choice_of_wcn_number)
        #  Choix des wcn_number noeuds ayant la capacité de conversion de longueur d'onde
        nodes = list(graph.nodes())
        wcn_nodes_list = cr.pick_random_numbers(nodes, choice_of_wcn_number)
        print('wcn list_', wcn_nodes_list)
        attrs = dict()
        for n in nodes:
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            if n in wcn_nodes_list:
                data['wcn'] = True
            attrs[n] = {'node_data': data}
        nx.set_node_attributes(graph, attrs)
        return graph



