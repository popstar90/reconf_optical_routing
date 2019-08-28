#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:54:24 2019

@author: fatta
"""

import networkx as nx
G = nx.DiGraph(day=5)
d = G.graph
G2 = G.copy()
d2 = G2.graph
G3 = nx.DiGraph(day=d2['day'])
print(d)
print(d2)
print(G3.graph)