import numpy as np
from .map import Point, Edge
from dataclasses import dataclass


@dataclass(frozen=True)
class Constraint:
    agent_id: int
    time: int

    def __array__(self): ...


@dataclass(frozen=True)
class VertexConstraint(Constraint):
    point: Point

    def __array__(self):
        return np.array([self.time, *self.point])


@dataclass(frozen=True)
class EdgeConstraint(Constraint):
    edge: Edge

    def __array__(self):
        return np.array([self.time, *self.edge[0], *self.edge[1]])
