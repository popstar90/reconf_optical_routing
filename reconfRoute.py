#    Copyright (C) 2019-2025 by
#    ATTA Amanvon Ferdinand <amanvon238@gmail.com>
#    All rights reserved.
#    BSD license.
#
# Author:   ATTA Amanvon Ferdinand (amanvon238@gmail.com)

"""

Ce module recoit les paramètres utiles aux cycles de  simulation .
Ces paramètres lui servent à créer la topologie à utiliser dans chaque cycle de simulation. Ce nom sera utiliser par la classe Topology
du package topologies pour créer le graphe du réseau.
Un cycle de simulation qui est contient 5000 Processus.
Un processus se presente comme suit :

* Choisir les noeuds considérés comme ayant la capacité de conversion de longueur d'onde
* Génération des routages initial et final
* Migration du routage initial et final

Après un cycle de simulation, les mesures de performation(nombres d'interruption de flux,
nombres de longueurs d'ondes additionnelles utilisées et la durée d'interruption) sont evualuées
en terme de moyenne et de variance.

L'exécution de ce module  effectue 3 cycles de simulation.
Chaque cycle de simulation concerne une plage de nombres de noeuds ayant la capacité de conversion à considérer.
3 plages étant considérer dans le

"""


from topologies.topo import Topology
from topologies.wc_placement import Placement
import os
import sys
import logging
import daiquiri


class ReconfRoute:

    """

     Classe chargée de recueillir la topologie réseau,  les routes initial et final
     puis lancer d'initer le processus de reconfiguration.

     Parameters
     ----------
     param: dict
         Paramètres de simulation  contenus dans une structure de données dictionnaire.
         Ces paramètres sont la topologie réseau(param['net_topo']), le type de réseau(param['net_type']),
         le nombre de processus par simulation(param['size']), le type de routage à considérer(param['paire_route_type'])
         et l'algorithme à utiliser lors des simulations(param['algo'])

     Examples
     -------
     Supposons que la topologie réseau fournit par la ligne de commande est nsfnet.
     Le type de réseau est un réseau avec conversion partielle.
     la nombre de processus est 5000. Le type de routage considérée est l'arbre mono-optique
     et l'algorithme utilisé est swcnTreeReconf. on a alors

     >>> param = {'net_topo': 'nsfnet', 'net_type': 0.5, 'size':5000, 'paire_route_type': 1, 'algo': 'swcnTreeReconf'}
     >>> reconfRoute = ReconfRoute(param)

    """

    def __init__(self, param=dict()):
        """

        Constructeur de la classe.

        """
        self.param = param

    def simulate(self):
        """

        Cette fonction permet de lancer un cycle de simulation en fonction des paramètres de simulation.
        Elle recoltera les resultats de la simuation afin d'une analyse ultérieurs de ces resultats.

        Returns
        -------
        None
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        directory = os.getcwd()
        daiquiri.setup(level=logging.INFO, outputs=(
            daiquiri.output.File(directory=directory, filename="mylauncher.log"), daiquiri.output.Stream(sys.stdout),
        ))
        logger = daiquiri.getLogger(__name__)
        # 1. Détermination de la topologie,
        # 1.1 Création de la topologie
        topo = Topology(self.param['net_topo'])
        graph = topo.create_topo()
        logger.info("Topology was created")
        #exit(-1)
        d = dict()
        if self.param['net_type'] == 0.5:
            d = {0: {'min': 50, 'max': 75}, 1: {'min': 25, 'max': 50},
                 2: {'min': 0, 'max': 25}}  # Liste des plages de pourcentages de swcn choisies
        elif self.param['net_type'] == 0:
            d = {0: {'min': 0, 'max': 0}}
        else:
            d = {0: {'min': 100, 'max': 100}}
        logger.info("Cycle of 3 Simulations starting")
        #Pour chaque topologie virtuelle faire
        for key, item in d.items():
            # Faire une simulation : une simulation contient N processus
            N = self.param['size']
            min_value = item['min']
            max_value = item['max']
            logger.info("Simulation " + str(key))
            for i in range(0, N):
                # Pour chaque processus faire
                print("TOUR :", i)
                # Définition du processus
                # 1.2 Choix des noeuds ayant la capacité  de conversion de longueur d'onde
                logger.info("Wavelength converter placement ")
                place_wcn = Placement(min_value, max_value)
                net = place_wcn.assign(graph)
                # 1.3 Initialisation du flux
                # Pour marquer que le flux est transporté par un lien on ajoute un attribut flow au lien avec pour valeur 1. Sinon 0
                # On suppose qu'au debut l'attribut flow a pour valeur 0 sur chaque lien du graphe.
                # Autrement dit, aucun flux ne circule sur les liens du graphe
                for e in net.edges():
                    net[e[0]][e[1]]['edge_data'] = {'flow': 0}
                # On suppose que les liens(fibres) ont une capacité de 16 longueurs distinctes
                #wavelengths_list = list(range(0, 16))
                # 2. Generation du routage initial et du routage final
                logger.info("Routing generation process is starting ")
                routing_class = load_class(package_name="routingGenerator", algo=route_pair(self.param['paire_route_type']))
                route_generator = routing_class(net)
                initial_route, final_route = route_generator.generate()
                logger.info("Routing generation process completed successfully ")
                # Génération du flux
                #Simuler ici une circulation du flux sur l'arbre initial
                # 3. Migration de routage
                migration_class = load_class(package_name="routingMigration", sub_package_name=migrate_net(self.param['net_type']),
                                             algo=self.param['algo'])
                migrate_route = migration_class(initial_route, final_route)
                logger.info("Routing switching process is starting ")
                migrate_route.run()
                #break
            break        #  # A enlever lorsqu'on aura fini


def migrate_net(argument=0.5):
    """

    La fonction retourne le type de réseau

    Parameters
    ----------
    argument: int
        donnée  representant un type de réseau
    Returns
    -------
    str
        net_type: le type de réseau(sans conversion(nwcn), conversion partielle(swcn) ou conversion totale(fwcn))
    """
    switcher = {
        0: "nwcn",
        0.5: "swcn",
        1: "fwcn"
    }
    net_type = switcher[argument]
    return net_type


def route_pair(argument=1):
    """

    La fonction retourne le type de routage

    Parameters
    ----------
    argument: int
        donnée  representant un type de routage
    Returns
    -------
    str
        le type de routage à utiliser pour la paire(pairOfLightTree, pairOfSemiLightTree ou pairOfLightForest)
    """
    switcher = {
        1: "pairOfLightTree",
        2: "pairOfSemiLightTree",
        3: "pairOfLightForest"
    }
    return switcher[argument]


def load_class(package_name, sub_package_name="",algo=""):
    """

    Permet de retourner la classe adéquate à exécuter en fonction des paramètres fournis en entrées

    Parameters
    ----------
    package_name: str
        le nom du package parent du "sous-package" devant contenir l'algorithme
    sub_package_name: str
        le nom du "sous-package" contenant le module de l'algorithme
    algo: str
        l'algorithme à executer
    Returns
    -------
    classeType
        Le type de la  classe à instancier

    """
    # print(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    algo_dir = os.getcwd()+os.sep+package_name+os.sep+sub_package_name
    paths = list(sys.path)
    print("BEFORE", sys.path)
    sys.path.insert(0, algo_dir)
    print("AFTER", sys.path)
    print('algo_dir', algo_dir)
    print('algo', algo)

    module = ""
    try:
        module = __import__(algo)
        # print("BON")
    except:
        print("Module inexistant!")
    finally:
        sys.path[:] = paths
    try:
        # print(algo[0].upper()+algo[1:])
        #classname = module.__getitem__(algo[0].upper() + algo[1:])
        classname = getattr(module, algo[0].upper() + algo[1:])
        print("SUPER!!!")
        return classname
    except:
        print('classe non trouvée')
        exit(-1)

