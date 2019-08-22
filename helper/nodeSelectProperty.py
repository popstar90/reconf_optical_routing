#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 08:25:39 2019

@author: fatta
"""
import networkx as nx
import networkx.algorithms.dag as dag
import nodeTreeProperty as ntp

def get_descendants(T=nx.DiGraph(), node=""):
    """
    Recupérer Tous les descendants du noeud node sur l'arbre T
    Parameters
    ----------
    T: nx.DiGraph()
      Le graphe orienté
    node: str
         Le noeud dont on recherche les descendants
    Returns
    -------
    list
        La liste des descendants
    """
    
    return list(dag.descendants(T,node))

def get_childs(T=nx.DiGraph(), node="0"):
    """
    Recupérer Tous les noeuds enfants du noeud node sur l'arbre T
   
    Parameters
    ----------
    T: nx.DiGraph()
      Le graphe orienté
    node: str
         Le noeud dont on recherche les enfants
    Returns
    -------
    list
        La liste des enfants
    """
    
    childs = []
    itere = T.successors(node)
    for n in itere:
        childs.append(n)
    return childs
     
def get_ancestors(T=nx.DiGraph(), node="0"):
    """
    Recupérer Tous les ascendants du noeud node sur l'arbre T
    Parameters
    ----------
    T: nx.DiGraph()
      Le graphe orienté
    node: str
         Le noeud dont on recherche les ascendants
    Returns
    -------
    list
        La liste des ascendants
    """

    return list(dag.ancestors(T,node))

def get_parent(T=nx.DiGraph(), node="0"):
    """
    Recupérer le parent du noeud node sur l'arbre T
    Parameters
    ----------
    T: nx.DiGraph()
      Le graphe orienté
    node: str
         Le noeud dont on recherche le parent
    Returns
    -------
    list
        la liste de parent(s): avec un seul element tant que T est une arbrorescene(arbre enraciné)
    """
    
    parent = []
    itere = T.predecessors(node)
    for n in itere:
        parent.append(n)
    return parent

def is_convergent(T0=nx.DiGraph(),Tz=nx.DiGraph(),node="0"):
    """
    Tester si un noeud est convergent ou pas
    Parameters
    ----------
    T0: nx.DiGraph()
       un  graphe orienté
    Tz:
       un graphe orienté
    node: str
         Le noeud dont on veut tester la convergence
    Returns
    -------
    bool
        True s'il est convergent et False dans le cas contraire
    """
    
    parent0 = get_parent(T0,node)
    parentz = get_parent(Tz,node)
    verdict = False
    if len(parent0) == len(parentz)== 1:
        if parent0[0]==parentz[0]:
            verdict = True
    return verdict

def is_divergent(T0=nx.DiGraph(),Tz=nx.DiGraph(),node="0"):
    """
    Tester si un noeud est divergent ou pas 
    Parameters
    ----------
    T0: nx.DiGraph()
       un  graphe orienté
    Tz:
       un graphe orienté
    node: str
         Le noeud dont on veut tester la divergence
    Returns
    -------
    bool
        True s'il est divergent et False dans le cas contraire
    """
    verdict = False
    if not ntp.is_leaf(T0,node) and not ntp.is_leaf(Tz,node="0"):
        childs0 = get_childs(T0,node)
        childsz = get_childs(Tz,node)
        for n in childs0:
            if n not in childsz:
                verdict = True
                break
    return verdict

def get_convergents(T0=nx.DiGraph(),Tz=nx.DiGraph(),node="0"):
    """
    Recupérer tous les noeuds convergents descendants du noeud node sur T0 et Tz
    Parameters
    ----------
    T0: nx.DiGraph()
       un  graphe orienté
    Tz:
       un graphe orienté
    node: str
         Le noeud dont on recherche les descendants convergents
    Returns
    -------
    list
        liste de noeuds convergents
    """
    descTz = get_descendants(Tz,node)
    descT0 = get_descendants(T0,node)
    convList = []
    for n in descTz:
        if n in descT0 and is_convergent(T0,Tz,n):
            convList.append(n)
    return convList

def get_divergents(T0=nx.DiGraph(),Tz=nx.DiGraph(),node="0"):
    """
    Recupérer tous les noeuds divergents descendants du noeud node sur T0 et Tz
    Parameters
    ----------
    T0: nx.DiGraph()
       un  graphe orienté
    Tz:
       un graphe orienté
    node: str
         Le noeud dont on recherche les descendants divergents
    Returns
    -------
    list
        liste de noeuds divergents
    """
    descTz = get_descendants(Tz,node)
    descT0 = get_descendants(T0,node)
    divList = []
    for n in descTz:
        if n in descT0 and is_divergent(T0,Tz,n):
            divList.append(n)
    return divList