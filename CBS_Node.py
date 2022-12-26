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
        
    def find_conflict(self):
        paths = [solution.get_path() for solution in self._solutions.solutions]
        max_len = max([len(path) for path in paths])
        for t in range(max_len):
            points = {}
            there_are_conflict = False
            for agent_index, path in enumerate(paths):
                if len(path) > t:
                    if (path[t].i, path[t].j) in points:
                        points[(path[t].i, path[t].j)].append(agent_index)
                        there_are_conflict = True
                    else:
                        points[(path[t].i, path[t].j)] = [agent_index]
                else:
                    if (path[-1].i, path[-1].j) in points:
                        points[(path[-1].i, path[-1].j)].append(agent_index)
                        there_are_conflict = True
                    else:
                        points[(path[-1].i, path[-1].j)] = [agent_index]
           
            if there_are_conflict:
                return points, t
            
        for i in range(1, max_len):
            points = {}
            prev_points = set()
            for j in range(len(paths)):
                if len(paths[j]) > i - 1:
                    prev_points.add(paths[j][i - 1])
            count_paths = 0
            for j in range(len(paths)):
                if len(paths[j]) > i:
                    count_paths += 1
                    current_point = paths[j][i]
                    prev_point = paths[j][i - 1]
                    
                    if current_point.i < prev_point.i:
                        current_point, prev_point = prev_point, current_point
                    elif current_point.i == prev_point.i:
                        if current_point.j < prev_point.j:
                            current_point, prev_point = prev_point, current_point

                    if f"{(prev_point.i, prev_point.j)} {(current_point.i, current_point.j)}" in points:
                        points[f"{(prev_point.i, prev_point.j)} {(current_point.i, current_point.j)}"].append(j)
                    else:
                        points[f"{(prev_point.i, prev_point.j)} {(current_point.i, current_point.j)}"] = [j]
            if len(points) != count_paths:
                return points, i

        return None, 0
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        return hash((self._cost, self._constraints))

    def __lt__(self, other): 
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.
        
        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        return self._cost < other._cost
    
    def __repr__(self) -> str:
        return f"CONSTRAINTS: {self._constraints}; COST: {self._cost}"