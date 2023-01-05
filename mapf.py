import numpy as np
from dataclasses import dataclass, field

from Primitives.map import Map

_Empty = np.array([])

@dataclass
class MAPF:
    """
    Representation of a multi-agent path finding problem

    - map: Map on which paths should be found
    - start_points: 2-d numpy array of start points for each agent (x, y by columns, points by rows)
    - goal_points: 2-d numpy array of goal points for each agent (x, y by columns, points by rows)

    sizes of start_points and gaol_points must be the same
    """

    map: Map = field(default_factory=Map)
    start_points: np.ndarray = _Empty
    goal_points: np.ndarray = _Empty

    def read_txt(self, filename: str):
        """
        Read the whole task from txt file in special format (in instances folder)

        :param filename - name of the .txt file
        """
        with open(filename) as file:
            lines = file.readlines()

        self.map.read_txt(lines)

        num_agents = int(lines[self.map.height + 1])
        self.start_points = np.zeros((num_agents, 2), dtype=int)
        self.goal_points = np.zeros((num_agents, 2), dtype=int)

        for i in range(num_agents):
            sy, sx, gy, gx = map(int, lines[self.map.height + 2 + i].split())
            self.start_points[i] = (sx, sy)
            self.goal_points[i] = (gx, gy)
