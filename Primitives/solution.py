from numpy import ndarray
from .map import Point


class Solution:
    """
    Wrapper around agent's path represented as 2d ndarray (rows for vertices, 2 columns for x and y)
    """

    def __init__(self, agent_id, path: ndarray) -> None:
        self.agent_id = agent_id
        self._path = path
        self.cost = len(path) - 1

    def get_point_at(self, time: int) -> Point:
        p =  self._path[time if time <= self.cost else -1]
        return p[0], p[1]
    
    def __repr__(self) -> str:
        return str(self._path)
