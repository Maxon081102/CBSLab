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


def CBS_DS(grid_map, start_points, goal_points, heuristic_func = None, search_tree = None, show_debug=False):
    log = open("logger.txt", "w")
    log.close()
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
        if cbs.was_expanded(current_node):
            break

        log = open("logger.txt", "a")
        log.write(str(hash(current_node.get_constraints())) + '\n')
        log.write(str(current_node.get_constraints()) + '\n')
        log.write(str(current_node.get_solutions()) + '\n\n')
        log.close()

        conflict = current_node.find_conflict()
        if conflict is None:
            return current_node.get_solutions()

        conflicting_agents = []
        new_constraints = [[], []]
        if len(conflict) == 4:
            vertex, step, agent_index_1, agent_index_2 = conflict
            conflicting_agents = [agent_index_1, agent_index_2]
            for i in range(2):
                new_constraints[i].append((conflicting_agents[i], step, BaseNode(vertex[0], vertex[1])))
        elif len(conflict) == 6:
            vertex_1, vertex_2, step_1, step_2, agent_index_12, agent_index_21 = conflict
            vertices = [vertex_1, vertex_2]
            conflicting_agents = [agent_index_12, agent_index_21]
            for i in range(2):
                new_constraints[i].append(
                    (conflicting_agents[i], step_1, BaseNode(vertices[i][0], vertices[i][1]))
                    )
                new_constraints[i].append(
                    (conflicting_agents[i], step_2, BaseNode(vertices[(i + 1) % 2][0], vertices[(i + 1) % 2][1]))
                    )
        
        for i, agent_index in enumerate(conflicting_agents):
            new_cbs_node = CBS_Node(
                current_node.get_cost(), copy.deepcopy(current_node.get_constraints()), 
                copy.deepcopy(current_node.get_solutions()), current_node
            )

            for constraint_tuple in new_constraints[i]:
                new_cbs_node.get_constraints().add_constraint(agents[agent_index], constraint_tuple[1], constraint_tuple[2])
            valid_node = True
            for agent in agents:
                path = new_cbs_node.get_solutions().get_solution_of_robot(agent.index).get_path()
                satisfies_new_constraints = True
                for constraint_tuple in new_constraints[i]:
                    ind, t, node = constraint_tuple
                    if t >= len(path):
                        t = -1
                    if ind == agent.index and node != BaseNode(path[t].i, path[t].j):
                        satisfies_new_constraints = False
                        break
                    if ind != agent.index and node == BaseNode(path[t].i, path[t].j):
                        satisfies_new_constraints = False
                        break
                if len(new_constraints[i]) == 2:
                    ind_1, t1, node_1 = new_constraints[i][0]
                    ind_2, t2, node_2 = new_constraints[i][1]
                    if t2 < len(path) and node_1 == BaseNode(path[t2].i, path[t2].j) and node_2 == BaseNode(path[t1].i, path[t1].j):
                        satisfies_new_constraints = False
                    
                if not satisfies_new_constraints:
                    found, end, steps = astar(
                        grid_map, 
                        agent,
                        new_cbs_node.get_constraints(),
                        heuristic_func,
                        search_tree
                    )
                    if not found:
                        valid_node = False
                        break
                    new_cbs_node.get_solutions().upgrade_solution(agent.index, found, end, steps)
            if valid_node:
                new_cbs_node.count_cost()
                if new_cbs_node.get_cost() < math.inf:
                    cbs.add_to_open(new_cbs_node)
        cbs.add_to_closed(current_node)
                
    return None

        


