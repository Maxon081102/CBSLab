import math


from time import time
from heapq import heappop, heappush

from map import Map
from Constraints import Constraint_step, Constraints

import typing as tp


def compute_cost(i1: int, j1: int, i2: int, j2: int) -> float:
    '''
    Computes cost of simple moves between cells
    '''
    if abs(i1 - i2) + abs(j1 - j2) == 1:  # cardinal move
        return 1
    elif i1 == i2 and j1 == j2:
        return 0
    else:
        raise Exception(
            'Trying to compute the cost of non-supported move! ONLY cardinal moves are supported.')


def distance(i1: int, j1: int, i2: int, j2: int) -> float:
    return abs(i1 - i2) + abs(j1 - j2)

class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node // always 0 for Dijkstra
    - F: f-value of the node // always equal to g-value for Dijkstra
    - parent: pointer to the parent-node 

    '''

    def __init__(self, i, j, g=0, h=0, f=None, parent=None, tie_breaking_func=None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        self.time = 0
        self.f = 0
        if parent is not None:
            self.time = parent.time + 1
            self.f = self.time + h
        # if f is None:
        #     self.f = self.g + h
        # else:
        #     self.f = f
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
        ijt = self.i, self.j, self.time, self.parent.__hash__()
        return hash(ijt)

    def __lt__(self, other):
        '''
        Comparing the keys (i.e. the f-values) of two nodes,
        which is needed to sort/extract the best element from OPEN.

        This comparator is very basic. We will code a more plausible comparator further on.
        '''
        if self.f == other.f:
            return self.time <= other.time
        return self.f < other.f

    def __repr__(self) -> str:
        return f"{self.i} {self.j} t={self.time} f={self.f}"


class SearchTreePQS:  # SearchTree which uses PriorityQueue for OPEN and set for CLOSED

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
        return not self._open

    def add_to_open(self, item):
        heappush(self._open, item)

    def get_best_node_from_open(self):
        while self._open:
            item = heappop(self._open)
            if not self.was_expanded(item):
                return item
        return None

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


def astar(
        grid_map: Map,
        start_i: int,
        start_j: int,
        goal_i: int,
        goal_j: int,
        agent_index: int,
        constraints: Constraints,
        heuristic_func: tp.Callable,
        search_tree: tp.Type[SearchTreePQS],
        get_all_path=False):
    ast = search_tree()
    steps = 0
    found = False
    last = None

    current_node = Node(start_i, start_j)
    ast.add_to_open(current_node)
    max_constraint_path = constraints.get_max_step(agent_index)
    while not ast.open_is_empty():
        if found and not get_all_path:
            break
        current_node = ast.get_best_node_from_open()
        # print("BEST NODE: ", current_node)
        if current_node is None:
            break

        steps += 1
            # else: # what
                # pass

        for (i, j) in grid_map.get_neighbors(current_node.i, current_node.j):
            new_node = Node(i, j, parent=current_node)

            in_contraints = False
            for node in constraints.get_constraints(agent_index, new_node.time):
                if node.i == new_node.i and node.j == new_node.j:
                    in_contraints = True
                    break
            if not in_contraints and not ast.was_expanded(new_node):
                new_node.g = current_node.g + \
                    compute_cost(current_node.i, current_node.j, i, j)
                new_node.h = heuristic_func(i, j, goal_i, goal_j)
                new_node.time = current_node.time + 1
                new_node.f = new_node.time + new_node.h
                if new_node.i == goal_i and new_node.j == goal_j and new_node.time > max_constraint_path and not get_all_path:
                    found = True
                    last = new_node
                    break
                ast.add_to_open(new_node)

        if current_node.i == goal_i and current_node.j == goal_j:
            if current_node.time > max_constraint_path:
                found = True
                last = current_node
                # print("LAST OPEN: ", ast.OPEN)
                break
        
        ast.add_to_closed(current_node)
        # print("END OPEN: ", ast.OPEN)


    nobodyRemembersThem = [last]

    if not get_all_path:
        return found, last, steps, nobodyRemembersThem
        
    if found:
        while True:
            leftover = ast.get_best_node_from_open()
            # print("leftover: ", leftover)
            if last != leftover: break
            assert last.f == leftover.f
            nobodyRemembersThem.append(leftover)

    # print("nobodyRemembersThem: ", nobodyRemembersThem)
    # print("OPEN: ", ast.OPEN)
    return found, last, steps, nobodyRemembersThem
