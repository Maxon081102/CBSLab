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
    

    def __init__(self, cost, constraints=None, solutions=None, parent = None):
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
        for i in range(max_len):
            points = {}
            count_paths = 0
            for j in range(len(paths)):
                if len(paths[j]) > i:
                    count_paths += 1
                    if paths[j][i] in points:
                        points[paths[j][i]].append(j)
                    else:
                        points[paths[j][i]] = [j]
            if len(points) != count_paths:
                return points, i
            
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

                    if f"{prev_point} {current_point}" in points:
                        points[f"{prev_point} {current_point}"].append(j)
                    else:
                        points[f"{prev_point} {current_point}"] = [j]
            if len(points) != count_paths:
                print("RETURN CONFLICT ", points, i)
                return points, i

        return None, 0
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        s = f"{self._cost} {self._constraints.__hash__()}"
        return hash(s)


    def __lt__(self, other): 
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.
        
        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        return self._cost < other._cost
    
    def __repr__(self) -> str:
        return f"{self._constraints} {self._cost}"