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
    
    def add_constraint(self, agent_index, step, node):
        if Constraint_step(agent_index, step) not in self.constraints:
            self.constraints[Constraint_step(agent_index, step)] = [node]
            return
        self.constraints[Constraint_step(agent_index, step)].append(node)
    
    def get_constraints(self, agent_index, step):
        if Constraint_step(agent_index, step) in self.constraints:
            return self.constraints[Constraint_step(agent_index, step)]
        return []
    
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