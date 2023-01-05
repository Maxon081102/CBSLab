from .map import Point, Edge
from .constraint import Constraint, VertexConstraint, EdgeConstraint
from dataclasses import dataclass


@dataclass
class Conflict:
    agent_ids: tuple[int, int]
    time: int

    def produce_constraint(self, agent_id: int) -> Constraint: 
        ...


@dataclass
class VertexConflict(Conflict):
    point: Point

    def produce_constraint(self, agent_id: int) -> Constraint:
        assert agent_id in self.agent_ids
        return VertexConstraint(agent_id, self.time, self.point)


@dataclass
class EdgeConflict(Conflict):
    edge: Edge

    def produce_constraint(self, agent_id: int) -> Constraint:
        assert agent_id in self.agent_ids
        return EdgeConstraint(agent_id, self.time, self.edge)
