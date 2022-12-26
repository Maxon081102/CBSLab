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
from Constraints import Constraints
from CBS_Node import CBS_Node
from CBS_Tree import CBS_tree
from CBS_Agent import BaseNode, Agent


def get_first_conflict_from(points):
    for key_conflict in points:
        if len(points[key_conflict]) > 1:
            return key_conflict

def print_debug(mode, mes, obj=None):
    if mode:
        print(mes, obj)


def CBS(grid_map, start_points, goal_points, heuristic_func = None, search_tree = None, show_debug=False):
    mode = show_debug
    cbs = CBS_tree()
    agents = []
    
    root = CBS_Node(0, Constraints(), Solutions())
    for i in range(len(start_points)):
        agents.append(
            Agent(
                i, 
                (start_points[i][0], start_points[i][1]), 
                (goal_points[i][0], goal_points[i][1])
            )
        )
    
    for agent in agents:
        found, end, steps = astar(
            grid_map, 
            agent,
            Constraints(),
            heuristic_func,
            search_tree
        )
        if not found:
            return None
        root.get_solutions().add_solution(found, end, steps)
    root.count_cost()

    cbs.add_to_open(root)

    while cbs.OPEN:
        current_node = cbs.get_best_node_from_open()

        conflict, step = current_node.find_conflict()
        if conflict is None:
            return current_node.get_solutions()
        
        first_conflict_key = get_first_conflict_from(conflict)
        for agent_index in conflict[first_conflict_key]:
            new_cbs_node = CBS_Node(
                current_node.get_cost(), copy.deepcopy(current_node.get_constraints()), 
                copy.deepcopy(current_node.get_solutions()), current_node
            )
            conflict_node = BaseNode(0, 0)
            if step >= len(current_node.get_solutions().solutions[agent_index].get_path()):
                conflict_node = BaseNode(
                    current_node.get_solutions().solutions[agent_index].get_path()[-1].i, 
                    current_node.get_solutions().solutions[agent_index].get_path()[-1].j
                )
            else:
                conflict_node = BaseNode(
                    current_node.get_solutions().solutions[agent_index].get_path()[step].i, 
                    current_node.get_solutions().solutions[agent_index].get_path()[step].j
                )
            
            new_cbs_node.get_constraints().add_constraint(agents[agent_index], step, conflict_node)
            found, end, steps = astar(
                grid_map, 
                agents[agent_index],
                new_cbs_node.get_constraints(),
                heuristic_func,
                search_tree
            )
            if not found:
                continue
            
            new_cbs_node.get_solutions().upgrade_solution(agent_index, found, end, steps)
            new_cbs_node.count_cost()
            if new_cbs_node.get_cost() < math.inf:
                cbs.add_to_open(new_cbs_node)
        cbs.add_to_closed(current_node)
                
    return None

        


