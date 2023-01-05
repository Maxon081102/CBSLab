import numpy as np
from CExtension import lightspeed

from Primitives.map import Point, Edge
from Primitives.node import Node
from Primitives.solution import Solution
from Primitives.conflict import Conflict, VertexConflict, EdgeConflict

from search_tree import SearchTreePQS
from mapf import MAPF


def find_agents_paths(task: MAPF):
    """ Conflict Based Search itself """

    validate(task)

    ast = SearchTreePQS()

    node = get_start_node(task)
    if node is None: return None

    ast.add_to_open(node)

    while not ast.open_is_empty():  # MAIN LOOP
        node: Node = ast.get_best_node_from_open() # type: ignore
        if node is None: break # open is empty

        conflicts = simulate(node)
        if not conflicts:  # goal node found
            return node

        conflict = conflicts[0]  # base version without any improvements

        for agent_id in conflict.agent_ids: # generate new nodes for 2 agents
            neighbor = node.make_copy(conflict.produce_constraint(agent_id))
            assert neighbor.cost >= node.cost

            if not ast.was_expanded(neighbor):
                if update_solution_for(agent_id, neighbor, task):
                    assert neighbor.cost >= node.cost
                    ast.add_to_open(neighbor)

        ast.add_to_closed(node)

    return None


def simulate(node: Node) -> list[Conflict]:
    """ Given a node with solutions, simulates them to find conflicts """
    conflicts: list[Conflict] = []

    time = 0
    last_step: dict[Point, list[int]] = {}
    current_step: dict[Point, list[int]] = {}
    for time in range(node.time + 1):
        for solution in node.solutions:
            v = solution.get_point_at(time)
            if v in current_step:  # someone in there already
                for other_id in current_step[v]:
                    vc = VertexConflict((solution.agent_id, other_id), time, v)
                    conflicts.append(vc)
                    
                current_step[v].append(solution.agent_id)
            else: 
                current_step[v] = [solution.agent_id]

            # TODO: remove duplicate conflicts
            if v in last_step:  # someone was there on the previous step
                # can't have more than one agent at the same point by now
                assert len(last_step[v]) == 1

                other_id = last_step[v][0]
                if solution.agent_id == other_id:  # same agent just stayed at this point
                    continue

                previous_point = solution.get_point_at(time - 1)
                # TODO: whacky, fix later
                other_current_point = node.solutions[other_id].get_point_at(time)
                assert node.solutions[other_id].agent_id == other_id
                if other_current_point == previous_point:
                    # some agent was at this point at previous step
                    # and he is now at our previous point
                    # this means we have an edge conflict
                    ec = EdgeConflict(
                        (solution.agent_id, other_id), time - 1, tuple(sorted((previous_point, v)))
                        )
                    conflicts.append(ec)

        if conflicts: return conflicts

        last_step = current_step
        current_step = {}

    return conflicts

# a = np.array([[1, 1], [2, 1], [3, 1], [4, 1], [5, 1]])
# b = np.array([[2, 1], [3, 1], [4, 1], [3, 1], [4, 1]])
# sa = Solution(0, a)
# sb = Solution(1, b)
# node = Node([sa, sb])
# conflicts = simulate(node)
# print(conflicts)


def get_start_node(task: MAPF) -> Node:
    solutions = []
    for i, (s, g) in enumerate(zip(task.start_points, task.goal_points)):
        path = lightspeed.find_path(task.map.cells, s, g)
        if path is None: 
            return None  # type: ignore
        solutions.append(Solution(i, path))
    return Node(solutions)


def update_solution_for(agent_id: int, node: Node, task: MAPF) -> bool:
    # construct contiguous ndarrays
    vc = node.vertexConstraints.get(agent_id, [])
    ec = node.edgeConstraints.get(agent_id, [])
    v_constraints = np.zeros((len(vc), 3), dtype=np.int32)
    e_constraints = np.zeros((len(ec), 5), dtype=np.int32)

    for i, c in enumerate(vc):
        v_constraints[i] = np.asarray(c)
    for i, c in enumerate(ec):
        e_constraints[i] = np.asarray(c)

    assert v_constraints.flags['C_CONTIGUOUS']
    assert e_constraints.flags['C_CONTIGUOUS']

    s = task.start_points[agent_id]
    g = task.goal_points[agent_id]

    # find path
    path = lightspeed.find_path(task.map.cells, s, g, v_constraints=v_constraints, e_constraints=e_constraints)

    if path is None: return False

    # update solution
    node.update_solution_for(agent_id, Solution(agent_id, path))

    return True


def validate(task: MAPF):
    assert len(task.start_points) == len(task.goal_points)

    # TODO: return path not found
    # assert all starting points and goal points are different
    points = set()
    for (x, y) in task.start_points: 
        p = (x, y)
        assert p not in points
        points.add(p)
    assert len(points) == len(task.start_points)

    points.clear()
    for (x, y) in task.goal_points: 
        p = (x, y)
        assert p not in points
        points.add(p)
    assert len(points) == len(task.goal_points)