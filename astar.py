import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush

from map import Map
from Constraints import Constraints
from CBS_Agent import BaseNode, Agent


def compute_cost(i1, j1, i2, j2):
    '''
    Computes cost of simple moves between cells
    '''
    if abs(i1 - i2) + abs(j1 - j2) == 1: #cardinal move
        return 1
    elif abs(i1 - i2) == 1 and abs(j1 - j2) == 1:
        return np.sqrt(2)
    elif i1 == i2 and j1 == j2:
        return 0
    else:
        raise Exception('Trying to compute the cost of non-supported move! ONLY cardinal moves are supported.')

def distance(i1, j1, i2, j2):
    line = max(abs(i1 - i2), abs(j1 - j2)) - min(abs(i1 - i2), abs(j1 - j2))
    return line + min(abs(i1 - i2), abs(j1 - j2)) * np.sqrt(2)


class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node // always 0 for Dijkstra
    - F: f-value of the node // always equal to g-value for Dijkstra
    - parent: pointer to the parent-node 

    '''
    
    def __init__(self, i, j, g = 0, h = 0, f = None, parent = None, tie_breaking_func = None):
        self.i = i
        self.j = j
        self.node = BaseNode(i, j)
        self.g = g
        self.h = h
        self.time = 0
        self.f = 0
        if parent is not None:
            self.time = parent.time + 1
            self.f = self.time + h
        self.parent = parent

        
    
    def __eq__(self, other):
        '''
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        '''
        return self.i == other.i and self.j == other.j and self.time == other.time
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        ijt = self.i, self.j, self.time
        return hash(ijt)


    def __lt__(self, other): 
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.
        
        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        if self.f == other.f:
            return self.g < other.g
        return self.f < other.f
    
    def __repr__(self) -> str:
        return f"{self.i} {self.j} {self.time}"


class SearchTreePQS: #SearchTree which uses PriorityQueue for OPEN and set for CLOSED
    
    def __init__(self):
        self._open = []
        self._closed = set()      # list for the expanded nodes = CLOSED
        
    def __len__(self):
        return len(self._open) + len(self._closed)
                    
    '''
    open_is_empty should inform whether the OPEN is exhausted or not.
    In the former case the search main loop should be interrupted.
    '''
    def open_is_empty(self):
        return len(self._open) == 0
    
    def add_to_open(self, item):
        heapq.heappush(self._open, item)
    
    def get_best_node_from_open(self):
        best_node = heapq.heappop(self._open)
        while self.was_expanded(best_node) and len(self._open) > 0:
            best_node = heapq.heappop(self._open)     
        return best_node
        
    def add_to_closed(self, item):
        self._closed.add(item)

    def was_expanded(self, item):
        return item in self._closed

    @property
    def OPEN(self):
        return self._open
    
    @property
    def CLOSED(self):
        return self._closed


def astar(grid_map, agent, constraints, heuristic_func = None, search_tree = None):
    ast = search_tree()
    steps = 0
    nodes_created = 0
    found = False
    CLOSED = None
    
    current_point = [agent.start.i, agent.start.j]
    current_node = Node(current_point[0], current_point[1])
    current_base_node = BaseNode(current_point[0], current_point[1])
    nodes_created += 1
    ast.add_to_open(current_node)
    latest_constraint = constraints.get_latest_constraint(agent)

    while not ast.open_is_empty():
        current_node = ast.get_best_node_from_open()
        current_base_node = BaseNode(current_node.i, current_node.j)
        if ast.was_expanded(current_node):
            break

        steps += 1
        ast.add_to_closed(current_node)
        neighbors = grid_map.get_neighbors(current_node.i, current_node.j)
        for point in neighbors:
            nodes_created += 1
            new_node = Node(
                point[0], point[1], g=current_node.g + compute_cost(point[0], point[1], current_node.i, current_node.j), 
                h=heuristic_func(agent.goal.i, agent.goal.j, point[0], point[1]), parent=current_node
            )
            new_base_node = BaseNode(new_node.i, new_node.j)
            if not ast.was_expanded(new_node) and\
                constraints.is_allowed(agent, new_node.time, current_base_node, new_base_node):  
                if new_base_node == agent.goal and new_node.time > latest_constraint:
                    end = new_node
                    found = True
                    return found, end, steps
                ast.add_to_open(new_node)
        
    CLOSED = ast.CLOSED
    return found, None, steps

