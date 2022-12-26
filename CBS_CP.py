import math
import heapq
import copy
from itertools import combinations

from time import time
from heapq import heappop, heappush

from map import Map
from astar import astar, Node
from Solutions import Solution, Solutions, make_path
from Constraints import Constraints, Constraint_step
from CBS_Node import CBS_Node
from CBS_Tree import CBS_tree

from path_to_success import UranaiBaba


def carefully_extract_the_conflict(points, some_vegetables):
    beautiful_soup = []
    # print(points.items())
    for (i, j, t), pets in points.items():
        if len(pets) > 1:
            # all combinations of agents (pets) of 2
            beautiful_soup += [(*tossed, (i, j), t)
                               for tossed in combinations(pets, 2)]

    baba = UranaiBaba(beautiful_soup, some_vegetables)
    return baba.please_uranai()


def get_first_conflict_from(points):
    for key_conflict in points:
        if len(points[key_conflict]) > 1:
            return key_conflict


def print_debug(mode, mes, obj=None):
    if mode:
        print(mes, obj)


def CBS_CP(grid_map, starts_points, goals_points, heuristic_func=None, search_tree=None, show_debug=False):
    mode = show_debug
    cbs = CBS_tree()

    root = CBS_Node(0, Constraints(), Solutions())
    for i in range(len(starts_points)):
        find, end, steps, abandoned = astar(
            grid_map,
            starts_points[i][0],
            starts_points[i][1],
            goals_points[i][0],
            goals_points[i][1],
            i,
            Constraints(),
            heuristic_func,
            search_tree,
            get_all_path=True
        )
        root.get_solutions().add_solution(find, end, steps, abandoned)

    root.count_cost()

    cbs.add_to_open(root)

    while cbs.OPEN:
        current_node = cbs.get_best_node_from_open()

        print_debug(mode, "NEW OPEN NODE", current_node)
        print_debug(mode, "SOLUTION IN OPEN NODE")
        for solution in current_node.get_solutions().solutions:
            print_debug(mode, "", solution.get_path())

        # conflict, step = current_node.find_conflict()
        vertex_conflicts, vertex_conflicts_step = current_node.find_vertex_conflicts()
        edge_conflicts, edge_conflicts_step = current_node.find_edge_conflicts()
        step = 0
        # print_debug(mode, "CONFLICT AND STEP", [conflict, step])

        if vertex_conflicts is None and edge_conflicts is None:
            return current_node.get_solutions()

        if vertex_conflicts_step >= edge_conflicts_step:
            granted_conflict = carefully_extract_the_conflict(
                vertex_conflicts, current_node.get_solutions())
            step = vertex_conflicts_step
        else:
            granted_conflict_key = get_first_conflict_from(edge_conflicts)
            granted_conflict = (
                edge_conflicts[granted_conflict_key][0],
                edge_conflicts[granted_conflict_key][1],
                (0, 0),
                0
            )
            step = edge_conflicts_step

        print_debug(mode, "FIRST_CONFLICT", granted_conflict)
        # first_astar_index = conflict[first_conflict_key][0]
        # conflict_node = Node(current_node.get_solutions().solutions[first_astar_index].get_path()[step].i, current_node.get_solutions().solutions[first_astar_index].get_path()[step].j)

        (a1, a2, _, _) = granted_conflict
        for agent_index in (a1, a2):
            new_cbs_node = CBS_Node(current_node.get_cost(), copy.deepcopy(
                current_node.get_constraints()), copy.deepcopy(current_node.get_solutions()), current_node)
            conflict_node = Node(0, 0)
            path = current_node.get_solutions(
            ).solutions[agent_index].get_path()

            print_debug(mode, step, len(path))

            if step >= len(path):
                conflict_node = Node(path[-1].i, path[-1].j)
            else:
                conflict_node = Node(path[step].i, path[step].j)
            new_cbs_node.get_constraints().add_constraint(agent_index, step, conflict_node)

            print_debug(mode, "CONSTRAINTS", new_cbs_node.get_constraints())

            find, end, steps, abandoned = astar(
                grid_map,
                starts_points[agent_index][0],
                starts_points[agent_index][1],
                goals_points[agent_index][0],
                goals_points[agent_index][1],
                agent_index,
                new_cbs_node.get_constraints(),
                heuristic_func,
                search_tree,
                get_all_path=True
            )
            if not find:
                continue

            print_debug(mode, "PATH: ", make_path(end))

            new_cbs_node.get_solutions().upgrade_solution(
                agent_index, find, end, steps, abandoned)

            new_cbs_node.count_cost()
            if new_cbs_node.get_cost() < math.inf:
                print_debug(mode, "NEW CBS NODE", new_cbs_node)
                cbs.add_to_open(new_cbs_node)
        # print("ALL OOPEN", cbs.OPEN)
        cbs.add_to_closed(current_node)
        print_debug(mode, "----------------------------")

    return None
