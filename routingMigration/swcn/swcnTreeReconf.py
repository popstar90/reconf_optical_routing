"""
A Ã©crire
"""
import networkx as nx
import os
import sys
#from pathlib import Path
#import matplotlib.pyplot as plt
import copy as cp
sim_dir = os.getcwd()+os.sep+"helper"
paths = list(sys.path)
#print("BEFORE", sys.path)
sys.path.insert(0, sim_dir)
nsp = __import__("nodeSelectProperty")
ntp = __import__("nodeTreeProperty")
#print(nsp)
sys.path[:] = paths

class SwcnTreeReconf:
    """
    Ecrire
    """
    def __init__(self, initial_tree=nx.DiGraph(), final_tree=nx.DiGraph()):
        self.initial_tree = initial_tree
        self.current_tree = initial_tree.copy()
        self.final_tree = final_tree
        self.my_currconv_nodes = []
        self.my_currdiv_nodes = []
        #self.reconf_order = []
        self.root = ""
        self.leafs = []
        self.criteria_value = {'add_cost': 0,'duration': 0, 'interrupt_duration': 0}
        #self.test1()
        #self.test2()
        #self.test_run()
        #exit(0)
        #self._initialize()

    def set_pair(self, initial_tree, final_tree):
        """
        Prend de "setter" la paire d'arbres qu'il faut reconfigurer
        """
        self.initial_tree = initial_tree
        self.final_tree = final_tree
        self.current_tree = self.initial_tree.copy()
        self._initialize()
        self.leafs = ntp.all_leafs(self.initial_tree)

    def _initialize(self):
        """
        Initialise les attributs de la classe
        """
        print("sayHello")
        self.root = list(nx.topological_sort(self.current_tree))[0] #or nx.topological_sort(final_tree)
        if nsp.is_divergent(self.current_tree,self.final_tree,self.root):
            self.my_currdiv_nodes.append(self.root)
        div = nsp.get_divergents(self.current_tree,self.final_tree,self.root)
        self.my_currdiv_nodes.extend(div)
        self.my_currconv_nodes = nsp.get_convergents(self.current_tree,self.final_tree,self.root)

    def _finalize(self):
        
        """
        Donne des valeurs par défaut pour des attributs
        """
        self.my_currconv_nodes = []
        self.my_currdiv_nodes = []
        #self.reconf_order = []
        self.root = ""
        self.leafs = []
        self.criteria_value = {'add_cost': 0,'duration': 0, 'interrupt_duration': 0}
    #ALGO 5
    def run(self):
        """
        L'équivalent de l'algorithme 5 du dernier draft
        """
        print(" begin migration")
        print("div_list",self.my_currdiv_nodes)
        print("conv_list",self.my_currconv_nodes)
        print("current_tree edges", self.current_tree.edges())
        print("final_tree_edges", self.final_tree.edges())
        if len(self.my_currdiv_nodes) != 0:
            # Selection et reconfiguration sequentielle de paire de catégorie 1
            print('Je cherche paire de cat 1')
            #On prend comme racine le premier noeud divergent(le plus proche de la racine des 2 arbres) de la pire d'arbres
            node = self.my_currdiv_nodes[0]
            while node != None:
                print('currdiv', node)
                pairs = self.select_dis_subtree(node, self.current_tree, self.final_tree)
                if len(pairs) == 0 :
                    #Enlever node de self.my_currdiv_nodes(grace self.my_currdiv_nodes.remove(node))
                    # Car aucune paire de cat 1 ne peut avoir pour racine ce dernier
                    self.my_currdiv_nodes.remove(node)
                    print("Select category 1 retourne rien avec ce noeud")
                    if len(self.my_currdiv_nodes) != 0:
                        node = self.my_currdiv_nodes[0]
                    else:
                        node = None
                        #break
                else:
                    print("len pairs", len(pairs))
                    for pair in pairs:
                        print(type(pair),type(pair[0]), type(pair[1]))
                        init_subtree, end_subtree = pair[0], pair[1]
                        if init_subtree == None or end_subtree == None:
                            print("SORCELERRIE PUR de NONE!!!")
                            exit(0)
                        else:
                            print("CATEGORY 1 GOOD !!!", list(init_subtree.edges()), list(end_subtree.edges()))
                            current = self.tree_update(self.current_tree, init_subtree, end_subtree)
                            if not  nx.is_arborescence(current):
                                # Utile pour le débogage
                                #print("IL Y A PROBLEME AVEC LE RESPECT DE LA PROPRIETE D'ARBRE cat1")
                                print("last_init_edges1", init_subtree.edges())
                                print("last_end_edges1", end_subtree.edges())
                                cur = nx.drawing.nx_pydot.to_pydot(self.current_tree)
                                cur.write_png('current.png')
                                exit(0)
                                #return None
                            else:
                                #Evaluation de performance
                                #1.duration : une paire de catégorie 1 à besoin de 5 étapes
                                self.criteria_value['duration'] = self.criteria_value['duration'] + 5
                                #2. Une paire de catégorie 1 n'utilise pas de ressource additionnelle
                                # Donc pas de mise à jour de add_cost
                                #3.durée d'interruption
                                interrupt = self._compute_interrupt(current)
                                self.criteria_value['interrupt_duration'] = self.criteria_value['interrupt_duration'] + interrupt
                                #Mis à jour de l'arbre courant
                                self.current_tree = current.copy()

                    self.root = list(nx.topological_sort(self.current_tree))[0] #or nx.topological_sort(final_tree)
                    self.my_currdiv_nodes = []
                    if nsp.is_divergent(self.current_tree,self.final_tree,self.root):
                        self.my_currdiv_nodes.append(self.root)
                    div = nsp.get_divergents(self.current_tree,self.final_tree,self.root)
                    self.my_currdiv_nodes.extend(div)
                    if len(self.my_currdiv_nodes) != 0:
                        node = self.my_currdiv_nodes[0]
                    else:
                        node = None
                        print("Plus de noeuds divergents!!!")
                        #break    
                    
                            
        # Après la reconfiguration des paires de catégorie 1 si l'arbre 
        # courant équivaut à l'arbre final alors 
        # la reconfiguration prend fin et on retourne la valeur de chaque critère 
        # de performance
        if self._is_end(self.current_tree, self.final_tree):
            print("FINI") 
            criteria = cp.deepcopy(self.criteria_value)
            self._finalize()
            return criteria
        else:
            print("PAS OU PLUS DE PAIRE DE CATEGORIE 1")
            #Dans le cas contraire
            # Rechercher les paires de catégories 2 et faire la reconfiguration de ses paires de catégories 2
            # Parcourir la liste des noeuds convergents et prendre le premier noeud qui permettra
            cur = nx.drawing.nx_pydot.to_pydot(self.current_tree)
            cur.write_png('current.png')
            conv_node = self._conv_node_for_cat2()
            if conv_node == None:
                print("select conv for cat2 n'est pas encore au point")
                exit(0)
            while conv_node != None:
                init_subtree, end_subtree = self.select_shared_subtree(conv_node, self.current_tree, self.final_tree)
                if init_subtree != None and end_subtree != None:
                    print("J'ai ma PAIRE DE CATEGORIE 2")
                    # Mettre ï¿½ jour l'arbre courant
                    current = self.tree_update(self.current_tree, init_subtree, end_subtree)
                    # Mettre ï¿½ jour la valeur courante de chaque critï¿½re de performance: A FAIRE ICI
                    if not nx.is_arborescence(current):
                        # Utile pour le débogage
                        print("last_init_edges2", init_subtree.edges())
                        print("last_end_edges2", end_subtree.edges())
                        # Evaluation de performance
                        #1.duration : une paire de catégorie 2 à besoin de 6 étapes
                        self.criteria_value['duration'] = self.criteria_value['duration'] + 6
                        #2. Mise à jour de add_cost avec le nombre de liens de STn
                        links_number = len(list(self.final_tree.edges()))
                        self.criteria_value['add_cost'] = self.criteria_value['add_cost'] + links_number
                        #3.durée d'interruption
                        interrupt = self._compute_interrupt(current)
                        self.criteria_value['interrupt_duration'] = self.criteria_value['interrupt_duration'] + interrupt
                        self.current_tree = self.final_tree.copy()
                        
                    else:
                        # Evaluation de performance
                        #1.duration : une paire de catégorie 2 à besoin de 6 étapes
                        self.criteria_value['duration'] = self.criteria_value['duration'] + 6
                        #2. Mise à jour de add_cost avec le nombre de liens de STn
                        links_number = len(list(end_subtree.edges()))
                        self.criteria_value['add_cost'] = self.criteria_value['add_cost'] + links_number
                        #3.durée d'interruption
                        interrupt = self._compute_interrupt(current)
                        self.criteria_value['interrupt_duration'] = self.criteria_value['interrupt_duration'] + interrupt
                        self.current_tree = current.copy()
                    conv_node = self._conv_node_for_cat2()
                # CE ELSE DOIT ETRE ENLEVE SI TOUT VA BIEN CAR C'EST PAS NORMAL
                else:
                    print("TIENS C'EST BIZZARE JE NE TROUVE PAS CAT 2")
                    exit(0)
            if self._is_end(self.current_tree, self.final_tree):
                print("FINI")  # pour le moment sinon APRES on va retourner la liste des valeurs des criteres de performances
                criteria = cp.deepcopy(self.criteria_value)
                self._finalize()
                return criteria 
            else:
                print("IL Y A PROBLEME")
            # retourner Reconf_order lorsque current_tree = final_tree
        print(" end  migration")

    def _is_end(self, current = nx.DiGraph(), final = nx.DiGraph()):
        """
        Teste si les 2 arbres sont identiques
        """

        if len((set(list(current.edges())).difference(set(list(final.edges()))))) == len((set(list(final.edges())).difference(set(list(current.edges()))))) == 0:
            print("Fin Reconfiguration")
            return True
        else:
            print("PAS ENCORE LA FIN !!!")
            return False

    def tree_update(self, current=nx.DiGraph(), init_subtree=nx.DiGraph(), end_subtree=nx.DiGraph()):
        """
        Permet de mettre à jour l'arbre courant en ajoutant et retranchant les liens et/ou noeuds 
        requis
        current_tree = current_tree - init_subtree - end_subtree
        :param current:
        :param init_subtree:
        :param end_subtree:
        :return:
        """
        curr = current.copy()
        print('B nodes data', curr.nodes(data=True))
        init_edges = list(init_subtree.edges())
        ex_end = list(set(list(end_subtree.nodes())).difference(set(list(curr.nodes()))))
        print("AVANT enlevement", list(curr.edges()))
        curr.remove_edges_from(init_edges)   # Enlever les liens de l'ancien sous-arbres  à l'arbre courant
        print("APRES enlevement", list(curr.edges()))
        end_edges = list(end_subtree.edges())
        # Ajouer les liens du nouveau sous-arbre
        for e in end_edges:
            curr.add_edges_from([(e[0], e[1])], edge_data=end_subtree.edges[e]['edge_data']) # Ajouter les noeuds du nouveau sous-arbre ï¿½ l'arbre courant
            #curr.add_edges_from([(e[0], e[1])])
        node_to_delete = []
        # enlever les noeuds qui ne
        # font partie d'aucun lien de l'arbre courant
        for n in list(curr.nodes()):
            in_edge = False
            for e in list(curr.edges()):
                if e[0] == n or e[1]== n:
                    in_edge = True
                    break
            if not in_edge:
                node_to_delete.append(n)
        curr.remove_nodes_from(node_to_delete)
        for n in ex_end:
            curr.nodes[n]['node_data'] = end_subtree.nodes[n]['node_data'] # Ajouter les propriï¿½tï¿½s des noeuds ï¿½ l'arbre courant
           # curr.add_node(n)
        print("curr final", list(curr.edges()))
        print('A nodes data', curr.nodes(data=True))
        return curr
    
    def _compute_interrupt(self, tree = nx.DiGraph()):
        """
        Une destination non  couverte est pris en compte  comme une interruption
        """
        count = 0
        for d in self.leafs:
            try:
                path_d = nx.shortest_path(tree, self.root, d)
            except:
                count = count + 1
        return count
        
        
    def select_dis_subtree(self, div_node, init_tree = nx.DiGraph(),end_tree=nx.DiGraph()):
        """
      
        Fonction retournant une paire de sous-arbre de catégorie 1
        L'algorithme recherche dans toutes les branches du sous-arbre de init_tree enraciné en div_node
        Toute les paires de sous-arbres de catégorie 1
    
        """

        print("EXECUTION DE algo 1")
        print('step 1 begin')
        # rechercher l'ensemble des enfants de div_node sur init_tree
        div_node_childs = nsp.get_childs(init_tree, div_node)
        conv_cdt = []
        pair_of_subtrees_list = []
        for c in div_node_childs:
            # Pour le moment je vais prendre qu'une seule paire à la fois pour faire simple
            print("child c", c)
            if len(pair_of_subtrees_list) == 1:
                #print()
                break
            # si le lien div_node-c est sur l'arbre final alors pas de cat1 possible
            # car il y a au moins un lien partagé
            if (div_node, c) in end_tree.edges() or (c, div_node) in end_tree.edges():
                continue
            print("Debut de recherche de garantie de non interruption du flux avec l'enfant", c)
            # on va parcourir l'ensemble des branches du sous-arbre de init_tree enraciné en div_node

            conv_list_root = nsp.get_convergents(init_tree, end_tree, self.root)
            #les noeuds convergents qui sont descendants de div_node sur l'arbre courant
            conv_list_init_tree = [convg for convg in conv_list_root if convg in nsp.get_descendants(init_tree, div_node)]
            #les noeuds convergents qui sont descendants de div_node sur le nouvel arbre
            conv_list_end_tree = [convg for convg in conv_list_root if convg in nsp.get_descendants(end_tree, div_node)]
            if conv_list_init_tree != conv_list_end_tree:
                # s'il ne sont pas égaux c'est pas la peine car st0 et stn doivent couvrir le meme ensemble
                # de noeuds convergents
                continue

            # rechercher les éléments de conv_list_init_tree  ayant c pour ancêtre sur init_tree. 
            # on recherche les noeuds convergents atteignable par la branche issu de div_node
            # sur laquelle se trouve l'enfant c
            conv_c_ancestors = []
            for conv in conv_list_init_tree:
                if c in nsp.get_ancestors(init_tree, conv):
                    conv_c_ancestors.append(conv)
            conv_cdt = [] # ensemble des noeuds convergents devant appartenir à notre paire de catégorie 1
            # tout élément conv de conv_c_ancestors doit-être de sorte que
            # div_node->conv sur init_tree est à liens disjoints de end_tree et div_node->conv sur end_tree est à liens disjoints de init_tree
            # Par définition de la paire de catégorie 1
            ensemble = True
            for conv in conv_c_ancestors:
                path0 = nx.shortest_path(init_tree,div_node,conv)
                pathz = nx.shortest_path(end_tree,div_node,conv)
                # Test div_node->conv sur init_tree est à liens disjoints de end_tree
                for i in range(0, len(path0) - 1):
                    edge = (path0[i], path0[i + 1])
                    opposite_edge = (path0[i + 1], path0[i])
                    if edge in end_tree.edges() or opposite_edge in end_tree.edges():
                        # pair_cg_nodes.remove(n)
                        ensemble = False
                        break
                # Test div_node->conv sur end_tree est à liens disjoints de init_tree
                for i in range(0, len(pathz) - 1):
                    edge = (pathz[i], pathz[i + 1])
                    opposite_edge = (pathz[i + 1], pathz[i])
                    if edge in init_tree.edges() or opposite_edge in init_tree.edges():
                        # pair_cg_nodes.remove(n)
                        ensemble = False
                        break
                # Si un seul n'est pas de catégorie 1 alors pas possible de les ajouter eux tous
                if not ensemble:
                    break
            if ensemble:
                conv_cdt.extend(conv_c_ancestors)
            # verifier si le fils courant c de div_node est convergent
            # l'ajouter à la liste des noeuds convergents devant appartenir 
            # à notre paire de catégorie 1
            if nsp.is_convergent(init_tree, end_tree, c):
                conv_cdt.append(c)
            print("Fin de recherche de garantie de non interruption du flux avec l'enfant", c)
            print("conv_cdt", conv_cdt)
            # Si aucune paire de catégorie 1 n'est trouvé passé à une autre branche
            if len(conv_cdt)==0:
                continue
            else:
                #verifier la condition de non conservation de la propriété d'arbre
                # Elle ne doit etre vérifié pour aucun élément de con_cdt
                print("Debut de recherche de garantie de continuite d'arbre")
                goodcat1 = True
                for n in conv_cdt:
                    if self._is_fulfil_notree_cond(init_tree,end_tree,n,div_node):
                        goodcat1 = False
                        break
                print("Fin de recherche de garantie de continuite d'arbre")
                if  not goodcat1:
                    continue
                else:
                    # construire la paire de catégorie 1 avec les éléments de conv_cdt
                    print("construire st0")
                    D0 = []
                    for n in conv_cdt:
                        print("n", n)
                        if ntp.is_leaf(init_tree, n):
                            print("n est feuille")
                            D0.append(n)
                        else:
                            desc_n = set(nsp.get_descendants(init_tree, n))
                            print("desc de n", n, list(desc_n))
                            # les autres noeuds convergents
                            other_set = set(conv_cdt).difference(set([n]))
                            print("other_set de n", n, list(other_set))
                            # ensemble des descendants appartenant  ï¿½ other_set
                            temp_set = desc_n.intersection(other_set)
                            print("temp_set", n, list(temp_set))
                            if len(temp_set) == 0:
                                D0.append(n)
                    st0 = ntp.subtree(init_tree, div_node, D0)
                    print("construire stn")
                    Dn = []
                    for n in conv_cdt:
                        print("n", n)
                        if ntp.is_leaf(end_tree, n):
                            print("n est feuille")
                            Dn.append(n)
                        else:
                            desc_n = set(nsp.get_descendants(end_tree, n))
                            print("desc de n", n, list(desc_n))
                            # les autres noeuds convergents
                            other_set = set(conv_cdt).difference(set([n]))
                            print("other_set de n", n, list(other_set))
                            # ensemble des descendants appartenant  ï¿½ other_set
                            temp_set = desc_n.intersection(other_set)
                            print("temp_set", n, list(temp_set))
                            if len(temp_set) == 0:
                                Dn.append(n)
                    stn = ntp.subtree(end_tree, div_node, Dn)
                    pair_of_subtrees_list.append((st0,stn))
        print("Fin algo 1")
        
        return pair_of_subtrees_list

    def reconf_dis_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """

    # def select_shared_subtree(self, seg0,segz, init_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
    def select_shared_subtree(self,conv_node, init_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
        """
    
        Fonction retournant une paire de sous-arbre de categorie 2
        L'algorithme prend un noeud convergent  puis recherche le premier ancetre commun aux deux arbres:
        Le plus jeune appartenant aux deux arbres qui peut effectuer la conversion 
        de longueur d'onde sinon le noeud racine de la paire d'arbres.
        A partir de là on construit une paire de sous-arbres couvrant 
        les destinations descendantes d'un noeud du segment allant de la racine à 
        conv_node
    
        """
        print("step 1 begin")
        nbsc = "0"
        path0 = nx.shortest_path(init_tree, self.root, conv_node)
        pathz = nx.shortest_path(end_tree, self.root, conv_node)
        D_pair = []
        D = ntp.all_leafs(init_tree)
        st0, stn = None, None
        
        if len(path0) == 2 or len(pathz) == 2:
            print("len(path0) == 2 or len(pathz) == 2")
            nbsc = self.root
            # Ensemble des des destinations ayant un ancêtre sur nbsc->conv_node(hormis nbsc mais conv_node y compris) de T0
            D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:])))>0]
            if ntp.is_leaf(init_tree, conv_node) and conv_node not in D_pair:
                D_pair.append(conv_node)
                
        else:
            ancestors0 = []
            ancestorsz = []
            print("len(path0) != 2 and len(pathz) != 2")
            #ancestors of conv_node on T0 except the root of T0
            ancestors0=  reversed(path0[1:len(path0)-1]) # du plus proche de conv_node au plus distant
            #ancestors of conv_node on Tz except the root of T0
            ancestorsz=  reversed(pathz[1:len(pathz)-1])
            # Garder les ancetres sur chaque arbre qui sont dans Vc
            is_wcn0 =nx.get_node_attributes(init_tree,'node_data')
            partial_ancestors0 = [a for a in ancestors0 if is_wcn0[a]['wcn']==True]
            is_wcnz =nx.get_node_attributes(end_tree,'node_data')
            partial_ancestorsz = [a for a in ancestorsz if is_wcnz[a]['wcn']==True]
            print("partial_ancestorsz", partial_ancestorsz)
            print("partial_ancestors0", partial_ancestors0)
            if len(partial_ancestors0) != 0 and len(partial_ancestorsz) != 0 and len(set(partial_ancestors0).intersection(set(partial_ancestorsz)))!=0:
                find = False
                #Pour chaque  ancetre (appartenant à Vc)  de conv_node sur Tz faire
                for n in partial_ancestorsz:
                    #verifier s'il est ancetre aussi sur l'ancien arbre(donc ancetre commun ayant la propriete de conversion)
                    if n in partial_ancestors0:
                        # Alors verifier que ce noeud va couvrir le meme sous-ensemble de destinations
                        temp_path0 = nx.shortest_path(init_tree, n, conv_node)
                        #sous-ensemble de D ayant un ancêtre sur le segment n->conv_node de T0
                        D_old = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(temp_path0))) > 0]
                        temp_pathz = nx.shortest_path(end_tree, n, conv_node)
                        # sous-ensemble de D ayant un ancêtre sur le segment n->conv_node de Tz
                        D_new = [d for d in D if len(set(nsp.get_ancestors(end_tree, d)).intersection(set(temp_pathz))) > 0]
                        # si c'est deux sous-ensemble sont identitques alors on tient la bonne racine de notre paire de categorie 2
                        if len(D_old) != 0 and len(D_new) != 0 and D_old == D_new:
                            nbsc = n
                            find = True
                            D_pair = D_old
                            break
                if not find:
                    # Si une racine ne respecte pas les critiques alors prendre la racine de (T0,Tz) comme racine
                    nbsc = self.root
                    D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:])))>0]
            else:
                # Si une racine ne respecte pas les critiques alors prendre la racine de (T0,Tz) comme racine
                nbsc = self.root
                D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:])))>0]
        print("step 1 end")
        print("D_pair", D_pair)
        print("Root, nbsc", self.root, nbsc)
        print("step 2 begin")
        st0 = ntp.subtree(init_tree, nbsc, D_pair) 
        print("step 2 end")
        print("step 3 begin")
        stn = ntp.subtree(end_tree, nbsc, D_pair)
        print("step 3 end")
        return st0, stn
        
        
        
    def reconf_shared_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    def _is_fulfil_cond1(self,t0=nx.DiGraph(),tz=nx.DiGraph(), conv_node="0", div_node="0"):
        """
        A Ecrire
        """ 
        verdict = False
        #ancetres sur To de conv_node situï¿½ sur div_node->conv_node
        path1 = nx.shortest_path(t0,div_node,conv_node)
        if len(path1) > 2:
            ancestors1=  path1[1:len(path1)-1]
            #garder ceux qui n'appartiennent pas ï¿½ tz
            final_ancestors = []
            tz_nodes = list(tz.nodes())
            for a in ancestors1:
                if a not in tz_nodes:
                    final_ancestors.append(a)
            if len(final_ancestors) != 0:
                for x in final_ancestors:
                    childs0 = nsp.get_childs(t0, x)
                    if len(childs0) >= 2:
                        #x est un noeud de branchement
                        childs0.remove(conv_node)
                        for n in range(0, len(childs0)):
                            #tout autre noeud dans une autre branche(descendant) du sommet initial x qui
                            #appartient aussi à tz doit êyre descendante d'un noeud de div_node->conv_node
                            verdict = True
                            print("condition 1 verified with node", conv_node)
                            break
        return verdict
    
    def _is_fulfil_cond2(self, t0=nx.DiGraph(), tz=nx.DiGraph(), conv_node="0", div_node="0"):
        """
        A ecrire
        """
        verdict = False
        # ancetres sur To de conv_node situï¿½ sur div_node->conv_node
        path1 = nx.shortest_path(t0, div_node, conv_node)
        if len(path1)>2:
            ancestors1 = path1[1:len(path1) - 1]
            tz_nodes = set(list(tz.nodes()))
            # garder ceux qui appartiennent ï¿½ tz
            partial_ancestors = set(ancestors1).intersection(tz_nodes)
            if len(partial_ancestors) != 0:
                all_desc_div_node = nsp.get_descendants(tz, div_node)
                # De partial_ancestors garde ceux qui sont pas descendants de div_node sur tz
                final_ancestors = partial_ancestors.difference(set(all_desc_div_node))
                if len(final_ancestors) != 0:
                    verdict = True
                    print("condition 2 verified with node", conv_node)
        return verdict

    def _is_fulfil_notree_cond(self, t0=nx.DiGraph(), tz=nx.DiGraph(), conv_node="0", node="0"):
        """
         Condition de non conservation de structure d'arbre rempli:
         Il existe un noeud convergent x ancetre  de conv_node sur node->conv_node de Tz qui
         n'est pas ancetre de conv_node sur node->conv_node de T0
        :param t0:
        :param tz:
        :param conv_node:
        :param node:
        :return:
        """
        verdict = False
        print("tree cond", conv_node)
        pathz = nx.shortest_path(tz, node, conv_node)
        # ancetres convergents  de conv_node situÃ© sur node->conv_node de Tz
        #conv_list = nsp.get_convergents(t0,tz,self.root)
        ancestorsz_conv = set(pathz[1:len(pathz)-1]).intersection(nsp.get_convergents(t0,tz,self.root))
        print("ancestorz_conv", ancestorsz_conv)
        if len(ancestorsz_conv) != 0:
            path0 = nx.shortest_path(t0, node, conv_node)
            ancestors0 = set(path0[1:len(path0)-1])
            print("ancestors0", ancestors0)
            # ancetres convergents  de conv_node situÃ© sur node->conv_node de Tz qui ne sont
            # pas sur node->conv_node de T0
            final_ancestors = ancestorsz_conv.difference(ancestors0)
            print("final_ancestors", final_ancestors)
            if len(final_ancestors) != 0:
                verdict = True
                print(" no tree condition verified with node", conv_node)
                
        return verdict
    def _conv_node_for_cat2(self):
        
        # Parcourir la liste des noeuds convergents et prendre le premier noeud qui permettra
        # de garantir la propriété d'arbre au futur arbre. Soit n ce noeud.
        # n ne doit pas avoir pour ancêtre sur Tz un noeud convergent x qui n'est pas son ancêtre sur T0
        conv_list = nsp.get_convergents(self.current_tree,self.final_tree,self.root)
        #Ranger la liste par ordre de hauteur dans l'arbre courant
        for i in range(0,len(conv_list)-1):
            path0i = nx.shortest_path(self.current_tree, self.root, conv_list[i])
            for j in range(i+1,len(conv_list)):
                path0j = nx.shortest_path(self.current_tree, self.root, conv_list[j])
                if len(path0i) > len(path0j):
                    temp = conv_list[j]
                    conv_list[j] = conv_list[i]
                    conv_list[i] = temp 
        myconv = None
        for i in range(0,len(conv_list)):
            curr_conv = conv_list[i]
            if not self._is_fulfil_notree_cond(self.current_tree, self.final_tree, curr_conv, self.root):
                myconv = curr_conv
                break
        return myconv