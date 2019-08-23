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
                    print(init_subtree, end_subtree)
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
            if not is_fullfil_cond1(init_tree,end_tree,n,div_node) and not is_fullfil_cond2(init_tree,end_tree,n,div_node):
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
        
        #new subtree
        print("step 4 end")

        
        print("Fin algo 1")
        return None,None
        
    
    def reconf_dis_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    
    
    def select_shared_subtree(self, seg0,segz, init_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    def reconf_shared_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """


def is_fullfil_cond1(t0=nx.DiGraph(),tz=nx.DiGraph(),conv_node="0",div_node="0"):
    """
    A écrire
    :param t0:
    :param tz:
    :param conv_node:
    :param div_node:
    :return:
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
                if len(partial_desc_x.difference(set(all_desc_div_node))) > 0:
                    verdict = True
                    print("condition 1 vérifiée")
                    break
    return verdict

def is_fullfil_cond2(t0=nx.DiGraph(), tz=nx.DiGraph(), conv_node="0", div_node="0"):
    """
    A écrire
    :param t0:
    :param tz:
    :param conv_node:
    :param div_node:
    :return:
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
    return verdict
