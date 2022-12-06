import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush

class Constraints:
    def __init__(self):
        self.constraints = {}
        self.agents_constraints_step = {}
    
    def add_constraint(self, agent_index, step, node):
        if Constraint_step(agent_index, step) not in self.constraints:
            self.agents_constraints_step[agent_index] = [step]
            self.constraints[Constraint_step(agent_index, step)] = [node]
            return
        self.constraints[Constraint_step(agent_index, step)].append(node)
        self.agents_constraints_step[agent_index].append(step)
    
    def get_constraints(self, agent_index, step):
        if Constraint_step(agent_index, step) in self.constraints:
            return self.constraints[Constraint_step(agent_index, step)]
        return []
    
    def get_max_step(self, agent_index):
        if agent_index in self.agents_constraints_step:
            return max(self.agents_constraints_step[agent_index])
        return 0
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        h = ""
        for constraint in list(self.constraints.values()):
            h += str(constraint)
        return hash(h)
    
    def __repr__(self) -> str:
        return self.constraints.__repr__()


class Constraint_step:
    def __init__(self, agent_index, step):
        self.agent_index = agent_index
        self.step = step
    
    def get_index(self):
        return self.agent_index
    
    def get_step(self):
        return self.step
    
    def __hash__(self):
        '''
        To implement CLOSED as set of nodes we need Node to be hashable.
        '''
        h = self.agent_index, self.step
        return hash(h)
    
    def __eq__(self, other):
        return self.agent_index == other.agent_index and self.step == other.step
    
    def __repr__(self):
        return f"{self.agent_index} {self.step}"