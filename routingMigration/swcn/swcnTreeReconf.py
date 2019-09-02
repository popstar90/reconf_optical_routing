"""
A Ã©crire
"""
import networkx as nx
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
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
        self.reconf_order = []
        self.root = ""
        self.criteria_value = {'add_cost': 0,'dure': 0, 'interrupt_dure': 0}
        #self.test1()
        #self.test2()
        #self.test_run()
        #exit(0)
        self._initialize()

    def _initialize(self):
        print("sayHello")
        self.root = list(nx.topological_sort(self.current_tree))[0] #or nx.topological_sort(final_tree)
        if nsp.is_divergent(self.current_tree,self.final_tree,self.root):
            self.my_currdiv_nodes.append(self.root)
        div = nsp.get_divergents(self.current_tree,self.final_tree,self.root)
        self.my_currdiv_nodes.extend(div)
        self.my_currconv_nodes = nsp.get_convergents(self.current_tree,self.final_tree,self.root)

    #ALGO 5
    def run(self):
        print(" begin migration")
        print("div_list",self.my_currdiv_nodes)
        print("conv_list",self.my_currconv_nodes)
        print("current_tree edges", self.current_tree.edges())
        print("final_tree_edges", self.final_tree.edges())
        if len(self.my_currdiv_nodes) != 0:
            # Selection et reconfiguration sequentielle de paire de catï¿½gorie 1
            print('Je cherche paire de cat 1')
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
                            #Mettre ï¿½ jour l'arbre courant(ce que l'on assimile ï¿½ un appel de reconf_dis_subtree pour mettre ï¿½ jour self.reconf_order
                            self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                            if not  nx.is_arborescence(self.current_tree):
                                #print("IL Y A PROBLEME AVEC LE RESPECT DE LA PROPRIETE D'ARBRE cat1")
                                print("last_init_edges1", init_subtree.edges())
                                print("last_end_edges1", end_subtree.edges())
                                cur = nx.drawing.nx_pydot.to_pydot(self.current_tree)
                                cur.write_png('current.png')
                                exit(0)
                                return None
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
                    
                            
        # Verified if current_tree == final_tree et mettre fin ï¿½ l'algo
        if self._is_end(self.current_tree, self.final_tree):
            return "FINI" # pour le moment sinon APRES on va retourner la liste des valeurs obtenues pour chaque critere de performance
        else:
            # Pas de paire de catï¿½gorie 1 possible
            print("PAS OU PLUS DE PAIRE DE CATEGORIE 1")
            #return None
            # Rechercher les paires de catï¿½gories 2 et faire la reconfiguration de ses paires de catï¿½gories 2
            # Parcourir la liste des noeuds convergents et prendre le premier noeud qui permettra
            # de garantir la propriété d'arbre au futur arbre. Soit n ce noeud.
            # n ne doit pas avoir pour ancêtre sur Tz un noeud convergent x qui n'est pas son ancêtre sur T0

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
                    self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                    # Mettre ï¿½ jour la valeur courante de chaque critï¿½re de performance: A FAIRE ICI
                    if not nx.is_arborescence(self.current_tree):
                        print("IL Y A PROBLEME AVEC LE RESPECT DE LA PROPRIETE D'ARBRE cat2")
                        print("last_init_edges2", init_subtree.edges())
                        print("last_end_edges2", end_subtree.edges())
                        exit(0)
                        return None
                    conv_node = self._conv_node_for_cat2()
                # CE ELSE DOIT ETRE ENLEVE SI TOUT VA BIEN CAR C'EST PAS NORMAL
                else:
                    print("TIENS C'EST BIZZARE JE NE TROUVE PAS CAT 2")
                    exit(0)
            if self._is_end(self.current_tree, self.final_tree):
                return "FINI"  # pour le moment sinon APRES on va retourner la liste des valeurs des criteres de performances
            else:
                print("IL Y A PROBLEME")
            # retourner Reconf_order lorsque current_tree = final_tree
        print(" end  migration")

    def _is_end(self, current = nx.DiGraph(), final = nx.DiGraph()):

        if len((set(list(current.edges())).difference(set(list(final.edges()))))) == len((set(list(final.edges())).difference(set(list(current.edges()))))) == 0:
            print("Fin Reconfiguration")
            return True
        else:
            print("PAS ENCORE LA FIN !!!")
            return False

    def tree_update(self, current=nx.DiGraph(), init_subtree=nx.DiGraph(), end_subtree=nx.DiGraph()):
        """
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
        curr.remove_edges_from(init_edges)   # Enlever les liens de l'ancien sous-arbres  ï¿½ l'arbre courant
        print("APRES enlevement", list(curr.edges()))
        end_edges = list(end_subtree.edges())
        for e in end_edges:
            curr.add_edges_from([(e[0], e[1])], edge_data=end_subtree.edges[e]['edge_data']) # Ajouter les noeuds du nouveau sous-arbre ï¿½ l'arbre courant
            #curr.add_edges_from([(e[0], e[1])])
        node_to_delete = []
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
        
    def select_dis_subtree(self, div_node, init_tree = nx.DiGraph(),end_tree=nx.DiGraph()):
        """
      
        Ecrire le commentaire
    
        """

        print("EXECUTION DE algo 1")
        print('step 1 begin')
        #conv_set = set()
        conv_list = nsp.get_convergents(init_tree,end_tree,div_node)
        #print(conv_set)
        pair_cg_nodes = []
        pair_of_subtrees_list = []
        print('step 1 end')
        
        print("step 2 begin")
        conv_nodes_visited = []
        
        while len(conv_nodes_visited) != len(conv_list):
            # premier element de conv_list non prï¿½sent dans pair_cg_nodes
            n = "0"
            print("pair_cg_nodes", pair_cg_nodes)
            print("conv_list",conv_list)
            print("pair_cg",pair_cg_nodes)
            if len(conv_nodes_visited) == 0:
                n = conv_list[0]
            else:
                for v in conv_list:
                    if v not in conv_nodes_visited:
                        n = v
                        break
            # check des 2 conditions
            if not self._is_fulfil_cond1(init_tree,end_tree,n,div_node) and not self._is_fulfil_cond2(init_tree,end_tree,n,div_node) and not self._is_fulfil_notree_cond(init_tree,end_tree,n,div_node):
                pair_cg_nodes.append(n)
            conv_nodes_visited.append(n)
            #else:
                #desc0 = set(nsp.get_descendants(init_tree, n))
                #descz = set(nsp.get_descendants(end_tree, n))
                #nodes_to_be_deleted = []
                #conv_nodes_visited.append(n)
                ##vis0 = desc0.intersection(conv_set)
                #print('vis0',vis0)
                #print('desc0', desc0)
                #visz = descz.intersection(set(conv_list))
                #conv_nodes_visited.extend(list(vis0.union(visz)))
                #if len(vis0)!= 0:
                #conv_nodes_visited.update(vis0)
                #print('visited', conv_nodes_visited)
                #print("conv_set",conv_set)
                #exit(0)
                #for u in nodes_to_be_deleted:
                    #conv_list.remove(u)
        # Pour carantir que les noeuds convergents choisit permettront
        # De dï¿½boucher sur une paire de catï¿½gorie 1
        print("pair_cg_nodes avant test disjoint", pair_cg_nodes)
        print("test disjoint")
        temp_cg_pair = []
        for n in pair_cg_nodes:
            # Aucun lien du segment div_node----n  sur Tz ne doit appartenir ï¿½ T0
            print('n', n)
            pathz = nx.shortest_path(end_tree, div_node, n)
            is_good = True
            for i in range(0,len(pathz)-1):
                edge =(pathz[i],pathz[i+1])
                opposite_edge = (pathz[i+1],pathz[i])
                if edge in init_tree.edges() or opposite_edge in init_tree.edges():
                    #pair_cg_nodes.remove(n)
                    is_good = False
                    break
             # Et Aucun lien du segment div_node----n  sur T0 ne doit appartenir ï¿½ Tz
            path0 = nx.shortest_path(init_tree, div_node, n)
            for i in range(0,len(path0)-1):
                edge =(path0[i],path0[i+1])
                opposite_edge = (path0[i+1],path0[i])
                if edge in end_tree.edges() or opposite_edge in end_tree.edges():
                    #pair_cg_nodes.remove(n)
                    is_good = False
                    break
            if is_good:
                temp_cg_pair.append(n)
            print("temp pair_cg_nodes", temp_cg_pair)
        pair_cg_nodes = temp_cg_pair 
        print("pair_cg_nodes", pair_cg_nodes)
        #exit(0)
        print("step 2 end")

        print("step 3 begin")
        
        if len(pair_cg_nodes) == 0:
            return pair_of_subtrees_list
        # Ranger les noeuds convergents par ordre de profondeur(sur Tz) decrioissante par rapport à div_node
        for i in range(0,len(pair_cg_nodes)-1):
            pathzi = nx.shortest_path(self.final_tree, div_node, pair_cg_nodes[i])
            for j in range(i+1,len(pair_cg_nodes)):
                pathzj = nx.shortest_path(self.final_tree, div_node, pair_cg_nodes[j])
                if len(pathzj) > len(pathzi):
                    temp = pair_cg_nodes[j]
                    pair_cg_nodes[j] = pair_cg_nodes[i]
                    pair_cg_nodes[i] = temp 
        print("step 4 begin")
        # construire des paires de catégorie 1 en parcourant cette liste de noeuds  convergents
        #visited = 
        for i in range(0,len(pair_cg_nodes)):
            #4.1 old subtree
            print("step 4.1 begin")
            n = pair_cg_nodes[i]
            D0 = [n]
            print("D0", D0)
            st0 = ntp.subtree(init_tree, div_node,D0)   
            print("step 4.1 end")
            print("step 4.2 begin")
            #new subtree
            Dn = [n]
            print("Dn", Dn)
            stn = ntp.subtree(end_tree, div_node,Dn)   
            ensemble = True
            for i in range(0,len(pair_of_subtrees_list)):
                pair = pair_of_subtrees_list[i]
                stn_pair = pair[1]
                st0_pair = pair[0]
                if len(set(list(stn_pair.edges())).intersection(set(list(stn.edges()))))!=0 or len(set(list(st0_pair.edges())).intersection(set(list(st0.edges()))))!=0:
                    ensemble = False
                    break    
            if ensemble:
                pair_of_subtrees_list.append((st0,stn))
            print("step 4.2 end")
            
        print("Fin algo 1")
        
        return pair_of_subtrees_list

    def reconf_dis_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """

    # def select_shared_subtree(self, seg0,segz, init_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
    def select_shared_subtree(self,conv_node, init_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
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
                        #sous-ensemble de D ayant un ancï¿½tre sur le segment n->conv_node de T0
                        D_old = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(temp_path0))) > 0]
                        temp_pathz = nx.shortest_path(end_tree, n, conv_node)
                        # sous-ensemble de D ayant un ancï¿½tre sur le segment n->conv_node de Tz
                        D_new = [d for d in D if len(set(nsp.get_ancestors(end_tree, d)).intersection(set(temp_pathz))) > 0]
                        # si c'est deux sous-ensemble sont identitques alors on tient la bonne racine de notre paire de categorie 2
                        # ï¿½ crï¿½er et cette devra couvrir le m^me ensemble de destination D_pair = D_old = D_new
                        
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
        if (len(path1)>2):
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
                