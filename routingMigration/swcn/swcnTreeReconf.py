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
        conv_list = nsp.get_convergents(init_tree,end_tree,div_node)
        print(conv_list)
        pair_cg_nodes = None
        print('step 1 end')
        
        print("step 2 begin")
        
        print("step 2 end")
        
        print("Fin algo 1")
        return None,None
        
    
    def reconf_dis_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    
    
    def select_shared_subtree(self, seg0,segzinit_tree=nx.DiGraph(),end_tree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """
    def reconf_shared_subtree(self, init_subtree=nx.DiGraph(),end_subtree=nx.DiGraph()):
        """
    
        Ecrire le commentaire
    
        """