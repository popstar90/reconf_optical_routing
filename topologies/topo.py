#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module permet d'avoir une vue topologique du réseau en se basant sur le package ` networkx <https://networkx.github.io>`_  écrit en python

"""

from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt


class Topology:
    """

    Classe permet de créer une topologie réseau.

    Parameters
     ----------
     topo_name: str
         nom de la topologie réseau à charger. Cette topologie devant être à l'interieur du package topologies

     Examples
     -------
     Supposons que la topologie réseau à créer est la topologie nsfnet.
     Cela suppose que le fichier nsfnet.gml contenant la structure du réseau se trouve à l'intérieur du package topologies.

     >>> topo_name= 'nsfnet'
     >>> topology = Topology(topo_name)
    """

    def __init__(self, topo_name=""):
        """
        Constructeur de la classe.
        """
        self.topo_name = topo_name

    def create_topo(self):
        """

         Crée la topologie réseau à utiliser pour la simulation

         Returns
         -------
         networkx.readwrite.gml
             le graphe du réseau rendu par ` networkx <https://networkx.github.io>`

        """
        path = Path(__file__).resolve().with_name(self.topo_name+'.gml')
        gml_graph = nx.read_gml(str(path))
        plt.figure()
        nx.draw(gml_graph, with_labels=True, font_weight='bold')
        path = Path(__file__).resolve().with_name(self.topo_name + ".png")
        plt.savefig(str(path))
        plt.close()
        return gml_graph

