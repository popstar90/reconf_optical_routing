#    Copyright (C) 2019-2020 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module est le point d'entrée dans le simulateur.
Ce module est exécuté en ligne de commande en fournissant avec comme argument, le nom de la topologie(obligatoirement)
à utiliser dans chaque cycle de simulation.
D'autres arguments existent tels que le type de réseau(conversion partielle, sans conversion, conversion totale),
le type de routage(arbre mono-optique, arbre multi-optique ou forêt optique) pour la paire , la taille en nombre de processus
à executer dans une simulation(par défaut égal à 5000) et l'algo de reconfiguration(par défaut swcnTreeReconf),

Examples
--------

Le module launcher.py peut se lancer dans la ligne de commande comme suit:

python launcher.py \\\\--topo= topo \\\\--netType= *reseau* \\\\--routeType= *route* \\\\--size= *taille* \\\\--algo= *nom_algo*

- *topo* : le nom de la topologie (ex : nsfnet, geant2012, coronet_usa). Cela suppose que les fichiers nsfnet.gml, geant2012.gml et coronet_usa.gml se trouve dans le package topologies
- *reseau* : pour valeur 0(réseau sans conversion), 0.5(réseau avec conversion partielle) et 1(réseau avec conversion totale)
- *route* : 1(arbre mono-optique), 2(arbre multi-optique) et 3(forêt optique)
- *taille* : le nombre de processus par tour(ex: 5000 par défaut)
- *algo* : par défaut  swcnTreeReconf.

"""
import daiquiri
import logging
import argparse
from reconfRoute import ReconfRoute
import os
import sys


if __name__ == '__main__':

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    directory = os.getcwd()
    daiquiri.setup(level=logging.INFO, outputs=(
        daiquiri.output.File(directory=directory, filename="mylauncher.log"), daiquiri.output.Stream(sys.stdout),
    ))
    logger = daiquiri.getLogger(__name__)
    logger.info("Simulations parameters checking process starting")
    parser = argparse.ArgumentParser(description='Déterminer les paramètres de la simulation')
    # Topologie à charger
    parser.add_argument("-t=", "--topo=", dest="net_topo", type=str, required=True, metavar=" ",  help="nom de la topologie à simuler")

    # 0 = Réseau WDM sans conversion de longueur d'onde
    # 0.5 = Réseau WDM avec propriété de conversion partielle de longueur d'onde(valeur par défaut)
    # 1 = Réseau WDM avec propriété de conversion totale de longueur d'onde
    parser.add_argument("-w=", "--netType=", dest="net_type", type=float, choices=[0, 0.5, 1], metavar=" ",
                        help="Type de réseau WDM à considérer")

    # 1 = Paire d'arbres mono-optiques
    # 2 = Paire d'arbres multi-optiques
    # 3 = Paire de forets optiques
    parser.add_argument("-r=", "--routeType=", dest="paire_route_type", type=int, choices=[1, 2, 3], metavar=" ",
                        help="Type de paires de routage à considérer")
    # Nom de l'algorithme à utiliser.
    # Cet algo doit être rechercher dans un sous-package de routingMigration
    # En fonction de l'option précédemment choisi
    parser.add_argument("-a=", "--algo=", dest="algo", type=str, default="swcnTreeReconf", metavar=" ", help="Algorithme à simuler")

    # Nombre de repétitions de l'expérience de Monte Carlo
    parser.add_argument("-s=", "--size=", dest="size", type=int, default=5000, metavar=" ", help="Nombre de répéitions de l'expérience de Monte Carlo")

    args = parser.parse_args()
    net_topo = args.net_topo
    net_type = args.net_type
    paire_route_type = args.paire_route_type
    algo = args.algo
    N = args.size
    if net_type == 0 and paire_route_type in [2, 3]:
        print("Impossible d'avoir ce type de paire de route pour  un réseau sans convertisseur ")
        logger.error("impossible routing!!!")
        logger.info("Simulations parameters checking process completed with error of imcompatibility in routing parameters")
        exit(-1)
    logger.info("Simulations parameters checking process completed successfully")
    param = {'net_topo': net_topo, 'net_type': net_type, 'paire_route_type': paire_route_type, 'algo': algo, 'size': N}
    logger.info("Cycle of Simulations starting")
    reconf_route = ReconfRoute(param)
    reconf_route.simulate()
    logger.info("Route reconfiguration completed successfully switching process is starting ")

