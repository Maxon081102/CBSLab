from copy import deepcopy
from .solution import Solution
from .constraint import Constraint, VertexConstraint, EdgeConstraint


class Node:
    """
    Node for the CBS Algorithm

    - vertexConstraints: mapping from agent index to all vertex constraints on that agent, readonly
    - edgeConstraints: mapping from agent index to all edge constraints on that agent, readonly
    use `add_constraint_for` method to add new constraints 

    - solutions: list of solutions for all agents, readonly, modify using `set_solution_for` method
    - cost: summary cost of all solutions, readonly
    - time: time needed for all agents to complete their paths, just max time over all solutions
    """

    def __init__(self, initial_solutions: list[Solution]) -> None:
        assert initial_solutions
        self.vertexConstraints: dict[int, list[VertexConstraint]] = {}
        self.edgeConstraints: dict[int, list[EdgeConstraint]] = {}
        self._all_constraints: frozenset[Constraint] = frozenset()
        self.solutions = initial_solutions
        self.cost = sum(map(lambda sol: sol.cost, self.solutions))
        self.time = max(map(lambda sol: sol.cost, self.solutions))
    
    def make_copy(self, new_constraint: Constraint) -> 'Node':
        node = Node(deepcopy(self.solutions))
        node._all_constraints = self._all_constraints.union([new_constraint])

        # TODO: don't like this code
        node.vertexConstraints = deepcopy(self.vertexConstraints)
        node.edgeConstraints = deepcopy(self.edgeConstraints)

        if isinstance(new_constraint, VertexConstraint):
            constraint_dict = node.vertexConstraints
        elif isinstance(new_constraint, EdgeConstraint):
            constraint_dict = node.edgeConstraints
        else:
            raise TypeError("Unexpected Constraint type")
        
        agent_id = new_constraint.agent_id
        if agent_id in constraint_dict:
            constraint_dict[agent_id].append(new_constraint) # type: ignore
        else: constraint_dict[agent_id] = [new_constraint] # type: ignore

        return node

    def update_solution_for(self, agent_id: int, solution: Solution):
        assert self.solutions[agent_id].agent_id == agent_id
        self.cost -= self.solutions[agent_id].cost
        self.cost += solution.cost
        self.solutions[agent_id] = solution
        # self.cost = sum(map(lambda sol: sol.cost, self.solutions))
        self.time = max(map(lambda sol: sol.cost, self.solutions))

    def __hash__(self) -> int:
        # TODO: test hash
        return hash(self._all_constraints)

    def __eq__(self, other) -> bool:
        # TODO: test this as well
        return (self._all_constraints == other._all_constraints)

    def __lt__(self, other) -> bool:
        # TODO: experiment on this
        return self.cost <= other.cost
