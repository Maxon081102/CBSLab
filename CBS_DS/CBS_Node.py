import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush

class CBS_Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node // always 0 for Dijkstra
    - F: f-value of the node // always equal to g-value for Dijkstra
    - parent: pointer to the parent-node 

    '''

    def __init__(self, cost=0, constraints=None, solutions=None, parent = None):
        self._cost = cost
        self._constraints = constraints
        self._solutions = solutions
        self.parent = parent
    
    def count_cost(self):
        cost = 0
        for solution in self._solutions.solutions:
            cost += solution.get_cost()
        self._cost = cost
    
    def get_cost(self):
        return self._cost
    
    def get_solutions(self):
        return self._solutions
    
    def get_constraints(self):
        return self._constraints
        
    def find_vertex_conflict(self):
        paths = [solution.get_path() for solution in self._solutions.solutions]
        max_len = max([len(path) for path in paths])
        for t in range(max_len):
            points = {}
            for agent_index, path in enumerate(paths):
                if len(path) > t:
                    if (path[t].i, path[t].j) in points:
                        return (path[t].i, path[t].j), t, points[(path[t].i, path[t].j)], agent_index
                    else:
                        points[(path[t].i, path[t].j)] = agent_index
                else:
                    if (path[-1].i, path[-1].j) in points:
                        return (path[-1].i, path[-1].j), t, points[(path[-1].i, path[-1].j)], agent_index
                    else:
                        points[(path[-1].i, path[-1].j)] = agent_index

        return None, 0, 0, 0

    
    def find_edge_conflict(self):
        paths = [solution.get_path() for solution in self._solutions.solutions]
        max_len = max([len(path) for path in paths])      
        for t in range(1, max_len):
            edges = {}
            for agent_index, path in enumerate(paths):
                if t < len(path):
                    if (path[t].i, path[t].j, path[t - 1].i, path[t - 1].j) in edges:
                        return (
                            (path[t - 1].i, path[t - 1].j), (path[t].i, path[t].j), 
                            t - 1, t, agent_index, edges[(path[t].i, path[t].j, path[t - 1].i, path[t - 1].j)]
                            )
                    else:
                        edges[(path[t - 1].i, path[t - 1].j, path[t].i, path[t].j)] = agent_index

        return None, None, 0, 0, 0, 0

    def find_conflict(self):
        vertex, step, agent_1, agent_2 = self.find_vertex_conflict()
        vertex_1, vertex_2, step_1, step_2, agent_12, agent_21 = self.find_edge_conflict()

        # Can be optized
        if vertex is None and vertex_1 is None:
            return None
        if vertex is None:
            return (vertex_1, vertex_2, step_1, step_2, agent_12, agent_21)
        if vertex_1 is None:
            return (vertex, step, agent_1, agent_2)
        if step <= step_1:
            return (vertex, step, agent_1, agent_2)
        else:
            return (vertex_1, vertex_2, step_1, step_2, agent_12, agent_21)
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        return hash(self._constraints)

    def __lt__(self, other): 
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.
        
        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        return self._cost < other._cost
    
    def __repr__(self) -> str:
        return f"CONSTRAINTS: {self._constraints}; COST: {self._cost}"