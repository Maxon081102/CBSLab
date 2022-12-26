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
        self.latest_conflicts = {}

    def update_hash(self, agent, step, base_node):
        if len(self._hash) == 0:
            self._hash = f"{agent.index} {base_node.i} {base_node.j} {step}"
            return
        items = self._hash.split(", ")
        i = 0
        while i < len(items):
            a, i, j, t = map(int, items[i].split())
            if agent.index > a:
                if base_node.i > i and base_node.j > j:
                    if step > t:
                        break
            i += 1
        self._hash = ", ".join(items[:i] + [f"{agent.index} {base_node.i} {base_node.j} {step}"] + items[i:])
    
    def add_constraint(self, agent, step, base_node):
        if (base_node, step) not in self.constraints:
            self.constraints[(base_node, step)] = set()
        self.constraints[(base_node, step)].add(agent)

        self.agent_constraints[(agent, step)] = base_node

        if base_node != agent.goal:
            if agent not in self.latest_conflicts:
                self.latest_conflicts[agent] = -1
            self.latest_conflicts[agent] = max(step, self.latest_conflicts[agent])

        self.update_hash(agent, step, base_node)

    def is_allowed(self, agent, step, node):
        no_one_else_must_be_here =\
             (node, step) not in self.constraints or\
                agent in self.constraints[(node, step)] and\
                len(self.constraints[(node, step)]) == 1
        this_does_not_have_to_be_somewhere_else =\
             (agent, step) not in self.agent_constraints or\
                self.agent_constraints[(agent, step)] == node
            
        return no_one_else_must_be_here and this_does_not_have_to_be_somewhere_else
    
    def get_latest_constraint(self, agent):
        if agent in self.latest_conflicts:
            return self.latest_conflicts[agent]
        return 0
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        return hash(self._hash)
    
    def __repr__(self) -> str:
        return self.constraints.__repr__()
