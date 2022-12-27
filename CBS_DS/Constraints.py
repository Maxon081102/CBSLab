import os
import sys
import time

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush

from CBS_Agent import BaseNode, Agent


class Constraints:
    def __init__(self):
        self._hash = ""
        self.constraints = {}
        self.agent_constraints = {}
        self.latest_conflicts_1 = {}
        self.latest_conflicts_2 = {}

    def update_hash(self, agent, step, base_node):
        constraint = ConstraintComparator(agent.index, base_node, step)
        if len(self._hash) == 0:
            self._hash = f"{agent.index} {base_node.i} {base_node.j} {step}"
            return
        items = self._hash.split(", ")
        k = 0

        while k < len(items):
            a, i, j, t = map(int, items[k].split())
            if constraint > ConstraintComparator(a, BaseNode(i, j), t):
                break
            k += 1
        self._hash = ", ".join(items[:k] + [f"{agent.index} {base_node.i} {base_node.j} {step}"] + items[k:])
    
    def add_constraint(self, agent, step, base_node):
        if (base_node, step) not in self.constraints:
            self.constraints[(base_node, step)] = set()
        self.constraints[(base_node, step)].add(agent)

        self.agent_constraints[(agent, step)] = base_node

        if base_node != agent.goal:
            if agent not in self.latest_conflicts_1:
                self.latest_conflicts_1[agent] = -1
            self.latest_conflicts_1[agent] = max(step, self.latest_conflicts_1[agent])
            if base_node not in self.latest_conflicts_2:
                self.latest_conflicts_2[base_node] = -1
            self.latest_conflicts_2[base_node] = max(step, self.latest_conflicts_2[base_node])

        self.update_hash(agent, step, base_node)

    def is_allowed(self, agent, step, node_from, node_to):
        no_one_else_has_to_be_here =\
             (node_to, step) not in self.constraints or\
                agent in self.constraints[(node_to, step)] and\
                len(self.constraints[(node_to, step)]) == 1
        this_does_not_have_to_be_somewhere_else =\
             (agent, step) not in self.agent_constraints or\
                self.agent_constraints[(agent, step)] == node_to

        no_vertex_conflicts = no_one_else_has_to_be_here and this_does_not_have_to_be_somewhere_else
        no_edge_conflicts = (node_to, step - 1) not in self.constraints or\
                            (node_from, step) not in self.constraints or\
                            len(self.constraints[(node_to, step - 1)] & self.constraints[(node_from, step)]) == 0

        return no_vertex_conflicts and no_edge_conflicts
    
    def get_latest_constraint(self, agent):
        max_step_1, max_step_2 = 0, 0
        if agent in self.latest_conflicts_1:
            max_step_1 = self.latest_conflicts_1[agent]
        if agent.goal in self.latest_conflicts_2:
            max_step_2 = self.latest_conflicts_2[agent.goal]
        return max(max_step_1, max_step_2)
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        return hash(self._hash)
    
    def __repr__(self) -> str:
        return self.constraints.__repr__()


class ConstraintComparator:
    def __init__(self, agent_index, node, step):
        self.agent = agent_index
        self.node = node
        self.step = step

    def __eq__(self, other) -> bool:
        return self.agent == other.agent and self.node == other.node and self.step == other.step

    def __lt__(self, other) -> bool:
        if self.agent != other.agent:
            return self.agent < other.agent
        if self.step != other.step:
            return self.step < other.step
        return self.node < other.node

    def __gt__(self, other) -> bool:
        return not self < other and not self == other
