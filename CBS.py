import math
import heapq
import copy

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush

from map import Map
from astar import astar, Node
from Solutions import Solution, Solutions, make_path
from Constraints import Constraints, Constraint_step
from CBS_Node import CBS_Node
from CBS_Tree import CBS_tree

def get_first_conflict_from(points):
    for key_conflict in points:
        if len(points[key_conflict]) > 1:
            return key_conflict

def print_debug(mode, mes, obj=None):
    if mode:
        print(mes, obj)


def CBS(grid_map, starts_points, goals_points, heuristic_func = None, search_tree = None, show_debug=False):
    mode = show_debug
    cbs = CBS_tree()
    
    root = CBS_Node(0, Constraints(), Solutions())
    for i in range(len(starts_points)):
        find, end, steps = astar(
            grid_map, 
            starts_points[i][0],
            starts_points[i][1],
            goals_points[i][0],
            goals_points[i][1],
            i,
            Constraints(),
            heuristic_func,
            search_tree
        )
        root.get_solutions().add_solution(find, end, steps)
    
    root.count_cost()

    cbs.add_to_open(root)

    while cbs.OPEN:
        current_node = cbs.get_best_node_from_open()
        print_debug(mode, "NEW OPEN NODE", current_node)
        print_debug(mode, "SOLUTION IN OPEN NODE")
        for solution in current_node.get_solutions().solutions:
            print_debug(mode, "", solution.get_path())
        conflict, step = current_node.find_conflict()
        print_debug(mode, "CONFLICT AND STEP", [conflict, step] )
        if conflict is None:
            return current_node.get_solutions()
        
        first_conflict_key = get_first_conflict_from(conflict)
        print_debug(mode, "FIRST_CONFLICT", conflict[first_conflict_key])
        for agent_index in conflict[first_conflict_key]:
            new_cbs_node = CBS_Node(current_node.get_cost(), copy.deepcopy(current_node.get_constraints()), copy.deepcopy(current_node.get_solutions()), current_node)
            conflict_node = Node(0, 0)
            print_debug(mode, step, len(current_node.get_solutions().solutions[agent_index].get_path()))
            if step >= len(current_node.get_solutions().solutions[agent_index].get_path()):
                conflict_node = Node(current_node.get_solutions().solutions[agent_index].get_path()[-1].i, current_node.get_solutions().solutions[agent_index].get_path()[-1].j)
            else:
                conflict_node = Node(current_node.get_solutions().solutions[agent_index].get_path()[step].i, current_node.get_solutions().solutions[agent_index].get_path()[step].j)
            new_cbs_node.get_constraints().add_constraint(agent_index, step, conflict_node)
            print_debug(mode, "CONSTRAINTS", new_cbs_node.get_constraints())
            find, end, steps = astar(
                grid_map,
                starts_points[agent_index][0],
                starts_points[agent_index][1],
                goals_points[agent_index][0],
                goals_points[agent_index][1],
                agent_index,
                new_cbs_node.get_constraints(),
                heuristic_func,
                search_tree
            )
            if type(end) == bool:
                continue
            print_debug(mode, "PATH: ", make_path(end))
            new_cbs_node.get_solutions().upgrade_solution(agent_index, find, end, steps)
            
            new_cbs_node.count_cost()
            if new_cbs_node.get_cost() < math.inf:
                print_debug(mode, "NEW CBS NODE", new_cbs_node)
                cbs.add_to_open(new_cbs_node)
        # print("ALL OOPEN", cbs.OPEN)
        cbs.add_to_closed(current_node)
        print_debug(mode, "----------------------------")
                
    return None

        


