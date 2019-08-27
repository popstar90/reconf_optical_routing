"""
A écrire
"""
import networkx as nx
import os
import sys
from pathlib import Path

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
        if len(self.my_currdiv_nodes) != 0:
            # Selection et reconfiguration sequentielle de paire de cat�gorie 1
            print('Je cherche paire de cat 1')
            node = self.my_currdiv_nodes[0]
            while node != None:
                print('currdiv', node)
                while True:
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
                        break
                    else:
                        for pair in pairs:
                            print(type(pair),type(pair[0]), type(pair[1]))
                            init_subtree, end_subtree = pair[0], pair[1]
                            if init_subtree == None or end_subtree == None:
                                print("SORCELERRIE PUR de NONE!!!")
                            else:
                                print("CATEGORY 1 GOOD !!!", list(init_subtree.edges()), list(end_subtree.edges()))
                                #Mettre � jour l'arbre courant(ce que l'on assimile � un appel de reconf_dis_subtree pour mettre � jour self.reconf_order
                                self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                                # Mettre � jour la valeur courante de chaque crit�re de performance: A FAIRE ICI
                        # verified if n is again divergent node . If it is not the case then remove n in unvisited divergent nodes
                        if not nsp.is_divergent(self.current_tree, self.final_tree, node):
                            print("Tu n'es plus divergent :", node)
                            self.my_currdiv_nodes.remove(node)
                            if len(self.my_currdiv_nodes) != 0:
                                node = self.my_currdiv_nodes[0]
                            else:
                                node = None
                            break
                        else:
                            print("SORCELERRIE PUR de divergence!!!")
                            
        # Verified if current_tree == final_tree et mettre fin � l'algo
        if self._is_end(self.current_tree, self.final_tree):
            return "FINI" # pour le moment sinon APRES on va retourner la liste des valeurs obtenues pour chaque critere de performance
        else:
            # Pas de paire de cat�gorie 1 possible
            print("PAS OU PLUS DE PAIRE DE CATEGORIE 1")
            # Rechercher les paires de cat�gories 2 et faire la reconfiguration de ses paires de cat�gories 2
            # cr�er la liste des noeuds  dans un ordre decroissant des profondeurs
            topo_sort_current = reversed(list(nx.topological_sort(self.current_tree)))
            conv_node = None
            for n in topo_sort_current:
                if nsp.is_convergent(self.current_tree, self.final_tree, n):
                    conv_node = n
                    break
            while conv_node != None:
                init_subtree, end_subtree = self.select_shared_subtree(conv_node, self.current_tree, self.final_tree)
                if init_subtree != None and end_subtree != None:
                    print("J'ai ma PAIRE DE CATEGORIE 2")
                    # Mettre � jour l'arbre courant
                    self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                    # Mettre � jour la valeur courante de chaque crit�re de performance: A FAIRE ICI
                    topo_sort_current = reversed(list(nx.topological_sort(self.current_tree)))
                    conv_node = None
                    for n in topo_sort_current:
                        if nsp.is_convergent(self.current_tree, self.final_tree, n):
                            conv_node = n
                            break
                # CE ELSE DOIT ETRE ENLEVE SI TOUT VA BIEN CAR C'EST PAS NORMAL
                else:
                    print("TIENS C'EST BIZZARE JE NE TROUVE PAS CAT 2")
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
        print("AVANT enlevement", list(curr.edges()))
        curr.remove_edges_from(init_edges)   # Enlever les liens de l'ancien sous-arbres  � l'arbre courant
        print("APRES enlevement", list(curr.edges()))
        #for n in end_nodes:
            #curr.add_node(n, node_data=end_subtree.nodes[n]['node_data']) # Ajouter les noeuds du nouveau sous-arbre � l'arbre courant
           # curr.add_node(n)
        end_edges = list(end_subtree.edges())
        for e in end_edges:
            curr.add_edges_from([(e[0], e[1])], edge_data=end_subtree.edges[e]['edge_data']) # Ajouter les noeuds du nouveau sous-arbre � l'arbre courant
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
        print("curr final", list(curr.edges()))
        print('A nodes data', curr.nodes(data=True))
        return curr
        
    def select_dis_subtree(self, div_node, init_tree = nx.DiGraph(),end_tree=nx.DiGraph()):
        """
      
        Ecrire le commentaire
    
        """

        print("EXECUTION DE algo 1")
        print('step 1 begin')
        conv_list = []
        conv_list = nsp.get_convergents(init_tree,end_tree,div_node)
        print(conv_list)
        pair_cg_nodes = []
        pair_of_subtrees_list = []
        print('step 1 end')
        
        print("step 2 begin")
        while len(conv_list) != len(pair_cg_nodes):
            # premier element de conv_list non pr�sent dans pair_cg_nodes
            n = "0"
            print("pair_cg_nodes", pair_cg_nodes)
            if len(pair_cg_nodes) == 0:
                n = conv_list[0]
            else:
                for v in conv_list:
                    if v not in pair_cg_nodes:
                        n = v
                        break
            # check des 2 conditions
            if not self._is_fulfil_cond1(init_tree,end_tree,n,div_node) and not self._is_fulfil_cond2(init_tree,end_tree,n,div_node):
                pair_cg_nodes.append(n)
            else:
                desc0 = set(nsp.get_descendants(init_tree, n))
                descz = set(nsp.get_descendants(end_tree, n))
                nodes_to_be_deleted = []
                nodes_to_be_deleted.append(n)
                del0 = desc0.intersection(set(conv_list))
                delz = descz.intersection(set(conv_list))
                nodes_to_be_deleted.extend(list(del0.union(delz)))
                for u in nodes_to_be_deleted:
                    conv_list.remove(u)
        # Pour carantir que les noeuds convergents choisit permettront
        # De d�boucher sur une paire de cat�gorie 1
        print("pair_cg_nodes avant test disjoint", pair_cg_nodes)
        print("test disjoint")
        temp_cg_pair = []
        for n in pair_cg_nodes:
            # Aucun lien du segment div_node----n  sur Tz ne doit appartenir � T0
            print('n', n)
            pathz = nx.shortest_path(end_tree, div_node, n)
            is_good = True
            for i in range(0,len(pathz)-1):
                if (pathz[i],pathz[i+1]) in init_tree.edges():
                    #pair_cg_nodes.remove(n)
                    is_good = False
                    break
             # Et Aucun lien du segment div_node----n  sur T0 ne doit appartenir � Tz
            path0 = nx.shortest_path(init_tree, div_node, n)
            for i in range(0,len(path0)-1):
                if (path0[i],path0[i+1]) in end_tree.edges():
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
        
        print("step 3 end")
        #chercher l'ensemble sous-ensembles de noeuds convergents E1,E2, pouvant appartenir � des paire de sous-arbres differentes
        # mais de m�me racine
        list_list_cg = []
        while len(pair_cg_nodes)!=0:
            conv = pair_cg_nodes[0]
            conv_nodes = []
            conv_nodes.append(conv)
            if len(pair_cg_nodes) > 1:
                for j in range(1,len(pair_cg_nodes)):
                    path1 = nx.shortest_path(init_tree, div_node, conv)
                    path2 = nx.shortest_path(init_tree, div_node, pair_cg_nodes[j])
                    if len(set(path1[1:len(path1)-1]).intersection(set(path2[1:len(path2)-1]))) != 0:
                        conv_nodes.append(pair_cg_nodes[j])
            for n in conv_nodes:
                pair_cg_nodes.remove(n)
            list_list_cg.append(conv_nodes)
        print("step 3 end")
        print("step 4 begin")
        for one_subset in list_list_cg:
            #4.1 old subtree
            # feuilles de st0 : n est feuille de t0 ou si au moins un descendant de n n'ai pas dans pair_cg_nodes
            #alors il sera feuille
            print("step 4.1 begin")
            D0 = []
            for n in one_subset:
                # descendants de n sur t0
                if ntp.is_leaf(init_tree, n) or len(one_subset) == 1 :
                    D0.append(n)
                else:
                    desc_n = set(nsp.get_descendants(init_tree, n))
                    print("desc de n", n, list(desc_n))
                    # pair_cg_nodes priv� de n
                    other_set = set(one_subset).difference(set([n]))
                    print("other_set de n", n, list(other_set))
                    #ensemble des descendants appartenant  � other_set
                    temp_set =desc_n.intersection(other_set)
                    print("temp_set", n, list(temp_set))
                    if len(temp_set) == 0:
                        D0.append(n)
            print("D0", D0)
            st0 = ntp.subtree(init_tree, div_node,D0)   
            print("step 4.1 end")
            print("step 4.2 begin")
            #new subtree
            # feuilles de stn :n est feuille de tz si au moins un descendant de n n'ai pas dans pair_cg_nodes
            #alors il sera feuille
            Dn = []
            for n in one_subset:
                # descendants de n sur t0
                if ntp.is_leaf(end_tree, n) or len(one_subset) == 1 :
                    Dn.append(n)
                else:
                    desc_n = set(nsp.get_descendants(end_tree, n))
                    print("desc de n", n, list(desc_n))
                    # pair_cg_nodes priv� de n
                    other_set = set(one_subset).difference(set([n]))
                    print("other_set de n", n, list(other_set))
                    #ensemble des descendants appartenant  � other_set
                    temp_set =desc_n.intersection(other_set)
                    print("temp_set", n, list(temp_set))
                    if len(temp_set) == 0:
                        Dn.append(n)
            print("Dn", Dn)
            stn = ntp.subtree(end_tree, div_node,Dn)   
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
            nbsc = self.root
            if len(path0) == 2:
                if not conv_node in D:
                    D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set([conv_node]))) > 0]
                else:
                    D_pair = [conv_node]
            elif len(pathz) == 2:
                D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:]))) > 0]
        else:
            ancestors0 = []
            ancestorsz = []
            #ancestors of conv_node on T0 except the root of T0
            ancestors0=  reversed(path0[1:len(path0)-1]) # du plus proche de conv_node au plus distant
            #ancestors of conv_node on Tz except the root of T0
            ancestorsz=  reversed(pathz[1:len(pathz)-1])
            # Garder les ancetres sur chaque arbre qui sont non divergents et qui ont sont dans Vc
            is_wcn0 =nx.get_node_attributes(init_tree,'node_data')
            partial_ancestors0 = [a for a in ancestors0 if not nsp.is_divergent(init_tree,end_tree,a) and is_wcn0[a]['wcn']==True]
            is_wcnz =nx.get_node_attributes(init_tree,'node_data')
            partial_ancestorsz = [a for a in ancestorsz if not nsp.is_divergent(init_tree,end_tree,a) and is_wcnz[a]['wcn']==True]
            if len(partial_ancestors0) != 0 and len(partial_ancestorsz) != 0 and len(set(partial_ancestors0).intersection(set(partial_ancestorsz)))!=0:
                find = False
                #Pour chaque  ancetre non divergent(appartenant � Vc)  de conv_node sur Tz faire
                for n in partial_ancestorsz:
                    #verifier s'il est anc�tre �galement sur l'ancien arbre(donc anc�tre commun non divergent ayant la propri�t� de conversion)
                    if n in partial_ancestors0:
                        # Alors v�rifier que ce noeud va couvrir le m�me sous-ensemble de destinations
                        temp_path0 = nx.shortest_path(init_tree, n, conv_node)
                        #sous-ensemble de D ayant un anc�tre sur le segment n->conv_node de T0
                        D_old = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(temp_path0))) > 0]
                        temp_pathz = nx.shortest_path(end_tree, n, conv_node)
                        # sous-ensemble de D ayant un anc�tre sur le segment n->conv_node de Tz
                        D_new = [d for d in D if len(set(nsp.get_ancestors(end_tree, d)).intersection(set(temp_pathz))) > 0]
                        # si c'est deux sous-ensemble sont identitques alors on tient la bonne racine de notre paire de categorie 2
                        # � cr�er et cette devra couvrir le m^me ensemble de destination D_pair = D_old = D_new
                        if len(D_old) != 0 and len(D_new) != 0 and D_old == D_new:
                            nbsc = n
                            find = True
                            D_pair = D_old
                            break
                if not find:
                    # Si une racine ne respecte pas les critiques alors prendre la racine de (T0,Tz) comme racine
                    nbsc = self.root
                    # et prendre comme ensemble de destinations:
                    # les elements de D ayant un anc�tre sur le segment root->conv_node hormis root
                    D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:]))) > 0]
            else:
                # Si une racine ne respecte pas les critiques alors prendre la racine de (T0,Tz) comme racine
                nbsc = self.root
                # et prendre comme ensemble de destinations:
                # les elements de D ayant un anc�tre sur le segment root->conv_node hormis root
                D_pair = [d for d in D if len(set(nsp.get_ancestors(init_tree, d)).intersection(set(path0[1:]))) > 0]
        print("step 1 end")
        print("D_pair", D_pair)
        print("Root", nbsc)
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
        #ancetres sur To de conv_node situ� sur div_node->conv_node
        path1 = nx.shortest_path(t0,div_node,conv_node)
        if len(path1) > 2:
            ancestors1=  path1[1:len(path1)-1]
            #garder ceux qui n'appartiennent pas � tz
            final_ancestors = []
            tz_nodes = list(tz.nodes())
            for a in ancestors1:
                if a not in tz_nodes:
                    final_ancestors.append(a)
                if len(final_ancestors) != 0:
                    for x in final_ancestors:
                    # rechercher la liste des descendants de x qui ne sont pas ancestre de
                        print(x)
                        all_desc_x = nsp.get_descendants(t0,x)
                        path2 = nx.shortest_path(t0, x, conv_node)
                        ancestors2 = path2[1:len(path2) - 1]
                        partial_desc_x = set(all_desc_x).difference(set(ancestors2))
                        all_desc_div_node = nsp.get_descendants(tz,div_node)
                        print(type(partial_desc_x))
                        if len(partial_desc_x.difference(set(all_desc_div_node))) > 0:
                            verdict = True
                            print("condition 1 verified")
                            break
        return verdict
    
    def _is_fulfil_cond2(self, t0=nx.DiGraph(), tz=nx.DiGraph(), conv_node="0", div_node="0"):
        """
        A ecrire
        """
        verdict = False
        # ancetres sur To de conv_node situ� sur div_node->conv_node
        path1 = nx.shortest_path(t0, div_node, conv_node)
        if (len(path1)>2):
            ancestors1 = path1[1:len(path1) - 1]
            tz_nodes = set(list(tz.nodes()))
            # garder ceux qui appartiennent � tz
            partial_ancestors = set(ancestors1).intersection(tz_nodes)
            if len(partial_ancestors) != 0:
                all_desc_div_node = nsp.get_descendants(tz, div_node)
                # De partial_ancestors garde ceux qui sont pas descendants de div_node sur tz
                final_ancestors = partial_ancestors.difference(set(all_desc_div_node))
                if len(final_ancestors) != 0:
                    verdict = True
                    print("condition 2 verified")
        return verdict

    def test1(self):
        "Permet de tester l'algo 1 : select_dis_subTree sur l'instance de la figure 2"
        T0 = nx.DiGraph()
        Tz = nx.DiGraph()
        #premier cas : aucune condition d'interruption verifi�e
        T0.add_nodes_from(['s', 'a', 'b', 'd', 'e', 'f', 'g', 'h'])
        T0.add_edges_from([('s', 'a'), ('a', 'b'), ('b', 'd'), ('d', 'e'), ('d','f'),('e','g'), ('f','h')])
        Tz.add_nodes_from(['s', 'a', 'k', 'e', 'f', 'g', 'h'])
        Tz.add_edges_from([('s', 'a'), ('a', 'k'), ('k', 'f'), ('f', 'e'), ('e', 'g'), ('f', 'h')])
        # deuxi�me cas : condition 1 d'interruption verifi�e
        #T0.add_nodes_from(['s', 'a', 'b', 'd', 'e', 'f', 'g', 'h', 'y'])
        #T0.add_edges_from([('s', 'a'), ('a', 'b'), ('b', 'd'), ('d', 'e'), ('d', 'f'), ('e', 'g'), ('f', 'h'), ('b', 'y')])
        #Tz.add_nodes_from(['s', 'a', 'k', 'e', 'f', 'g', 'h', 'y'])
        #Tz.add_edges_from([('s', 'a'), ('a', 'k'), ('k', 'f'), ('f', 'e'), ('e', 'g'), ('f', 'h'), ('s', 'y')])
        # troisi�me  cas : condition 2 d'interruption verifi�e
        #T0.add_nodes_from(['s', 'a', 'b', 'd', 'e', 'f', 'g', 'h'])
        #T0.add_edges_from([('s', 'a'), ('a', 'b'), ('b', 'd'), ('d', 'e'), ('d','f'),('e','g'), ('f','h')])
        #Tz.add_nodes_from(['s', 'a', 'k', 'e', 'f', 'g', 'h', 'd'])
        #Tz.add_edges_from([('s', 'a'), ('a', 'k'), ('k', 'f'), ('f', 'e'), ('e', 'g'), ('f', 'h'),('s', 'd')])
        wcn_nodes_list = ['a','d']
        attrs = dict()
        print('TEST1')
        for n in T0.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            print(' b n', n)
            if n in wcn_nodes_list:
                print('n', n)
                data['wcn'] = True
            attrs[n] = {'node_data': data}
            print('attrs', attrs[n])
        nx.set_node_attributes(T0, attrs)
        attrs = dict()
        for n in Tz.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            if n in wcn_nodes_list:
                data['wcn'] = True
            attrs[n] = {'node_data': data}
        nx.set_node_attributes(Tz, attrs)
        self.root = 's'
        self.current_tree = T0.copy()
        self.final_tree = Tz.copy()
        nodes = nsp.get_divergents(self.current_tree, self.final_tree, self.root)
        #print("DIV_NODES", nodes)
        div = 'a'
        #for div in nodes:
        pairs = self.select_dis_subtree(div, self.current_tree, self.final_tree)
        if len(pairs) == 0 :
            print("Select category 1 retourne rien avec ce noeud")
        else:
            for pair in pairs:
                init_subtree, end_subtree = pair[0], pair[1]
                if init_subtree != None and end_subtree != None:
                    self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                    print("TEST DE TREE UPDATE")
                    print(list(self.current_tree.edges()))
                    print(list(self.current_tree.nodes(data=True)))
                    print(list(self.final_tree.edges()))
                    print(list(self.final_tree.nodes(data=True)))
                    if self._is_end(self.current_tree, self.final_tree):
                        print("c'est fini!!!")
                    else:
                        print("ca bug un peu!!!")
                else:
                    print("c'est pas fini!!! CATE 2 NOW")
            #print(set(list(init_subtree.edges())).difference(set(list(end_subtree.edges()))))
    def test2(self):
        "Permet de tester l'algo3 : select_shared_subTree sur l'instance de la figure 3"
        T0 = nx.DiGraph()
        Tz = nx.DiGraph()
        T0.add_nodes_from(['s', 'i', 'k', 'a', 'b','l', 'c', 'd', 'e','h', 'g', 'f'])
        T0.add_edges_from([('s', 'i'), ('s', 'k'), ('k','a'), ('a', 'b'), ('b', 'l'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('d','h'),('e','g'), ('g','f')])
        Tz.add_nodes_from(['s', 'i', 'k', 'a', 'b','l', 'c', 'd', 'h', 'g', 'f'])
        Tz.add_edges_from([('s', 'i'), ('s', 'k'), ('k', 'l'), ('k','a'), ('a', 'b'), ('b', 'g'), ('b', 'c'), ('c', 'd'), ('d','h'), ('g','f')])
        wcn_nodes_list = ['a','k', 'd', 'g']
        attrs = dict()
        print('TEST2')
        for n in T0.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            print(' b n', n)
            if n in wcn_nodes_list:
                print('n', n)
                data['wcn'] = True
            attrs[n] = {'node_data': data}
            print('attrs', attrs[n])
        nx.set_node_attributes(T0, attrs)
        attrs = dict()
        for n in Tz.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            if n in wcn_nodes_list:
                data['wcn'] = True
            attrs[n] = {'node_data': data}
        nx.set_node_attributes(Tz, attrs)
        #node_data = nx.get_node_attributes(T0,'node_data')
        #print("data", node_data)
        #for key, value in node_data.items():
            #print("wave", key, value['wcn'])
        #exit(0)
        self.root = 's'
        self.current_tree = T0.copy()
        self.final_tree = Tz.copy()
        # Rechercher les paires de cat�gories 2 et faire la reconfiguration de ses paires de cat�gories 2
        # cr�er la liste des noeuds  dans un ordre decroissant des profondeurs
        topo_sort_current = reversed(list(nx.topological_sort(self.current_tree)))
        conv_node = None
        for n in topo_sort_current:
            if nsp.is_convergent(self.current_tree, self.final_tree, n):
                conv_node = n
                break
        while conv_node != None:
            init_subtree, end_subtree = self.select_shared_subtree(conv_node, self.current_tree, self.final_tree)
            #print("TEST CATE 2")
            #print(list(init_subtree.edges()))
            #print(list(init_subtree.nodes(data=True)))
            #print(list(end_subtree.edges()))
            #print(list(end_subtree.nodes(data=True)))
            #exit(0)
            if init_subtree != None and end_subtree != None:
                    print("J'ai ma PAIRE DE CATEGORIE 2")
                    # Mettre � jour l'arbre courant
                    self.current_tree = self.tree_update(self.current_tree, init_subtree, end_subtree)
                    print("TEST DE TREE UPDATE")
                    print(list(self.current_tree.edges()))
                    print(list(self.current_tree.nodes(data=True)))
                    print(list(self.final_tree.edges()))
                    print(list(self.final_tree.nodes(data=True)))
                    # Mettre � jour la valeur courante de chaque crit�re de performance: A FAIRE ICI
                    topo_sort_current = reversed(list(nx.topological_sort(self.current_tree)))
                    conv_node = None
                    for n in topo_sort_current:
                        if nsp.is_convergent(self.current_tree, self.final_tree, n):
                            conv_node = n
                            break
            else:
                print("1-ca bug un peu!!!")
                exit(0)
        if self._is_end(self.current_tree, self.final_tree):
            print("c'est fini!!!")
        else:
            print("2-ca bug un peu!!!")
    
    def test_run(self):
        """
        Permet de tester l'algo5 : swcn_ltree_reconf sur une instance contenant :
        - La paire de categorie 2 de la figure 3;
        - Une paire de categorie 1 ({s{i{j}}},{s{i}} ) 
        """
        T0 = nx.DiGraph()
        Tz = nx.DiGraph()
        T0.add_nodes_from(['s', 'i', 'j', 'k', 'a', 'b','l', 'c', 'd', 'e','h', 'g', 'f','m','n'])
        T0.add_edges_from([('s', 'm'), ('m', 'n'), ('s', 'i'), ('i', 'j'), ('s', 'k'), ('k','a'), ('a', 'b'), ('b', 'l'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('d','h'),('e','g'), ('g','f')])
        Tz.add_nodes_from(['s', 'j', 'k', 'a', 'b','l', 'c', 'd', 'h', 'g', 'f', 'n'])
        Tz.add_edges_from([('s', 'n'), ('s', 'j'), ('s', 'k'), ('k', 'l'), ('k','a'), ('a', 'b'), ('b', 'g'), ('b', 'c'), ('c', 'd'), ('d','h'), ('g','f')])
        wcn_nodes_list = ['a','k', 'd', 'g']
        attrs = dict()
        for n in T0.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            print(' b n', n)
            if n in wcn_nodes_list:
                print('n', n)
                data['wcn'] = True
            attrs[n] = {'node_data': data}
            print('attrs', attrs[n])
        nx.set_node_attributes(T0, attrs)
        attrs = dict()
        for n in Tz.nodes():
            data = {'wcn': False, 'switch_table': None, 'neighbors': dict()}
            if n in wcn_nodes_list:
                data['wcn'] = True
            attrs[n] = {'node_data': data}
        nx.set_node_attributes(Tz, attrs)
        self.current_tree = T0.copy()
        self.final_tree = Tz.copy()
        self._initialize()
        self.run()