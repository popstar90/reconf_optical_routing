"""
A Ã©crire
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
        self.initialize()

    def initialize(self):
        print("sayHello")
        self.root = list(nx.topological_sort(self.current_tree))[0] #or nx.topological_sort(final_tree)
        print(self.root)
        if nsp.is_divergent(self.current_tree,self.final_tree,self.root):
            self.my_currdiv_nodes.append(self.root)
        div = nsp.get_divergents(self.current_tree,self.final_tree,self.root)
        self.my_currdiv_nodes.extend(div)
        self.my_currconv_nodes = nsp.get_convergents(self.current_tree,self.final_tree,self.root)
    
    def run(self):
        print("migrated")
        print("div_list",self.my_currdiv_nodes)
        print("conv_list",self.my_currconv_nodes)
        if len(self.my_currdiv_nodes) != 0:
            for node in self.my_currdiv_nodes:
                while True:
                    init_subtree,end_subtree = self.select_dis_subtree(node, self.current_tree, self.final_tree)
                    print("CATE 1", init_subtree, end_subtree)
                    break # A enlever
                    if init_subtree == None or end_subtree == None:
                        #Enlever node de self.my_currdiv_nodes(grace sel.my_currdiv_nodes.remove(node))
                        break
                    else:
                        pass
                        #call reconf_dis_subtree pour mettre à jour self.reconf_order
                        #Mettre à jour l'arbre courant
        # verifier si l'arbre courant égale à l'arbre final.
        # Si oui alors retourner self.reconf_order sinon gérer les catégories 2
        #Pour ce faire rechercher les noeuds convergents de current_tree 
        # et construire à partir du plus profond dans l'arbre seg0 puis segz
        # ensuite call select_shared_subtree puis reconf_shared_subtree
        
        
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
        print('step 1 end')
        
        print("step 2 begin")
        while len(conv_list) != len(pair_cg_nodes):
            # premier element de conv_list non prsent dans pair_cg_nodes
            n = "0"
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

        print("step 2 end")

        print("step 3 begin")
        
        if len(pair_cg_nodes) == 0:
            return None,None
        
        print("step 3 end")

        print("step 4 begin")
        #old subtree
        # feuilles de st0 :si au moins un descendant de n n'ai pas dans pair_cg_nodes
        #alors il sera feuille
        D0 = []
        for n in pair_cg_nodes:
            # descendants de n sur t0
            desc_n = set(nsp.get_descendants(init_tree, n))
            # pair_cg_nodes privé de n
            other_set = set(pair_cg_nodes).difference(set([n]))
            #ensemble des descendants de n n'appartenant pas à other_set
            temp_set =desc_n.difference(other_set)
            if len(temp_set) == 0:
                D0.append(n)
        st0 = ntp.subtree(init_tree, div_node,D0)   
        
        print("step 4 end")
        
        #new subtree
        print('step 5 begin')
        #new subtree
        # feuilles de stn :si au moins un descendant de n n'ai pas dans pair_cg_nodes
        #alors il sera feuille
        Dn = []
        for n in pair_cg_nodes:
            # descendants de n sur t0
            desc_n = set(nsp.get_descendants(end_tree, n))
            # pair_cg_nodes privé de n
            other_set = set(pair_cg_nodes).difference(set([n]))
            #ensemble des descendants de n n'appartenant pas à other_set
            temp_set =desc_n.difference(other_set)
            if len(temp_set) == 0:
                Dn.append(n)
        stn = ntp.subtree(end_tree, div_node,Dn)  

        print("step 5 end")
         
        print("Fin algo 1")
        
        return st0,stn
    

        
        
    
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
        
        if len(path0) == 2 or len(pathz)==2 or len(set(path0).intersection(set(pathz)))==0:
            nbsc = self.root
        else:
            ancestors0 = []
            ancestorsz = []
            #ancestors of conv_node on T0
            ancestors0=  reversed(path0[1:len(path0)-1]) # du plus proche de conv_node au plus distant
            #ancestors of conv_node on Tz
            ancestorsz=  reversed(pathz[1:len(pathz)-1])
            # Garder ceux qui sont non divergents et qui ont sont dans Vc
            is_wcn0 =nx.get_node_attributes(init_tree,'wcn')
            is_wcnz =nx.get_node_attributes(init_tree,'wcn')
            partial_ancestors0 = [a for a in ancestors0 if not nsp.is_divergent(init_tree,end_tree,a) and is_wcn0[a]==True]
            is_wcnz =nx.get_node_attributes(init_tree,'wcn')
            partial_ancestorsz = [a for a in ancestorsz if not nsp.is_divergent(init_tree,end_tree,a) and is_wcnz[a]==True]
            if len(partial_ancestors0) !=0 and len(partial_ancestorsz) != 0 and len(set(partial_ancestors0).intersection(set(partial_ancestorsz)))!=0:
                for n in partial_ancestorsz:
                    pass
                    
            else:
                nbsc = self.root

            
        print("step 1 end")
        
        
        
    def reconf_shared_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    def _is_fulfil_cond1(self,t0=nx.DiGraph(),tz=nx.DiGraph(), conv_node="0", div_node="0"):
        """
        A Ecrire
        """ 
        verdict = False
        #ancetres sur To de conv_node situé sur div_node->conv_node
        path1 = nx.shortest_path(t0,div_node,conv_node)
        if len(path1) > 2:
            ancestors1=  path1[1:len(path1)-1]
            #garder ceux qui n'appartiennent pas à tz
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
        # ancetres sur To de conv_node situé sur div_node->conv_node
        path1 = nx.shortest_path(t0, div_node, conv_node)
        if (len(path1)>2):
            ancestors1 = path1[1:len(path1) - 1]
            tz_nodes = set(list(tz.nodes()))
            # garder ceux qui appartiennent à tz
            partial_ancestors = set(ancestors1).intersection(tz_nodes)
            if len(partial_ancestors) != 0:
                all_desc_div_node = nsp.get_descendants(tz, div_node)
                # De partial_ancestors garde ceux qui sont pas descendants de div_node sur tz
                final_ancestors = partial_ancestors.difference(set(all_desc_div_node))
                if len(final_ancestors) != 0:
                    verdict = True
                    print("condition 2 verified")
        return verdict