import typing as tp
from array import array
from dataclasses import dataclass

from astar import Node


@dataclass
class Layer:
    time: int
    width: int # amount of nodes on the current layer

class MDD:
    def __init__(self, nodes: tp.List[Node]) -> None:
        assert nodes  # nodes is not empty
        self.cost: int = nodes[0].g
        self.layers: tp.List[Layer] = [None] * (self.cost + 1) # type: ignore

        unique = {nodes[0]: nodes[0]} # now all nodes are equal so only add one
        currentLayerNodes = nodes
        nextLayerNodes: tp.List[Node] = []
        for i in range(self.cost, -1, -1):
            self.layers[i] = Layer(i, len(unique))
            unique.clear()
            nextLayerNodes.clear()
            for node in currentLayerNodes:
                parent: Node = node.parent # type:ignore
                try:
                    found = unique[parent]
                    if found is not parent:
                        nextLayerNodes.append(parent)
                except(KeyError):
                    unique[parent] = parent
                    nextLayerNodes.append(parent)
            
            currentLayerNodes = list(nextLayerNodes)

    def tell_me_how_many_nodes_are_on_level(self, level: int) -> int:
        if level > self.cost:
            return 1
        res = self.layers[level].width
        return res
    
    def __repr__(self) -> str:
        res = ""
        for layer in self.layers:
            res += str(layer.time) + ": " + str(layer.width) + "\n"
        return res
            

def TEST():
    a = Node(0, 0, 0)
    b = Node(1, 0, 1, parent=a)
    c = Node(0, 1, 1, parent=a)
    d = Node(1, 1, 1, parent=a)

    e1 = Node(1, 2, 2, parent=d)
    e2 = Node(1, 2, 2, parent=c)
    f = Node(2, 2, 2, parent=b)

    g1 = Node(3, 3, 3, parent=e1)
    g2 = Node(3, 3, 3, parent=e2)
    g3 = Node(3, 3, 3, parent=f)

    mdd = MDD([g1, g2, g3])

    print(mdd)

    # should be 
    # 0: 1
    # 1: 3
    # 2: 2
    # 3: 1
