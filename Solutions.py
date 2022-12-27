import math
import heapq
import typing as tp

from time import time
from heapq import heappop, heappush

from astar import Node

def make_path(goal):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''
    length = goal.f
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1]

def make_all_path(abandoned):
    paths = []
    for end in abandoned:
        length = end.f
        current = end
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        path = path[::-1]
        paths.append(path)
    return paths


class Solutions:
    def __init__(self):
        self.solutions = []
        self.totalSteps = 0
    
    def add_solution(self, find, end, steps, abandoned: tp.List[Node] = []):
        self.totalSteps += steps
        self.solutions.append(Solution(find, end, steps, abandoned))
    
    def upgrade_solution(self, index, find, end, steps, abandoned: tp.List[Node] = []):
        self.totalSteps += steps
        self.solutions[index] = Solution(find, end, steps, abandoned)
    
    def get_solution_of_robot(self, index):
        return self.solutions[index]
    
    def get_cost(self):
        cost = 0
        for solution in self.solutions:
            cost += solution.get_cost()
        return cost
    
    def __repr__(self) -> str:
        for solution in self.solutions:
            print(solution.get_path())
    
class Solution:
    def __init__(self, find, end, steps, abandoned: tp.List[Node] = []):
        self._find = find
        self._end = end
        self._steps = steps
        self._abandoned = abandoned
        self._sneakyMdd = None # there IS none
    
    def find(self):
        return self._find
    
    def get_path(self):
        path = make_path(self._end)
        return path
    
    def get_all_path(self):
        paths = make_all_path(self._abandoned)
        return paths
    
    def steps(self):
        return self._steps
    
    def get_cost(self):
        return self._end.time

    def remember_the_past(self):
        return self._abandoned
