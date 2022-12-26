import typing as tp
from array import array
from dataclasses import dataclass, field

from astar import Node


class NodeTree:
    def __init__(self, node: Node) -> None:
        self.data = node
        self.children: tp.Set['NodeTree'] = set()

    def __eq__(self, other) -> bool:
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)


class MDD:
    def __init__(self, nodes: tp.List[Node]) -> None:
        assert nodes  # nodes is not empty
        self.cost: int = nodes[0].time # fuck
        self.layers: tp.List[int] = [int] * (self.cost + 1)  # type: ignore

        # now all nodes are equal so only add one
        lastNode = NodeTree(nodes[0])
        unique: tp.Dict[NodeTree, NodeTree] = {lastNode: lastNode}

        currentLayerNodes: tp.List[NodeTree] = [
            NodeTree(node) for node in nodes]
        nextLayerNodes: tp.List[NodeTree] = []

        for i in range(self.cost, -1, -1):
            self.layers[i] = len(unique)
            if i == 0: break
            unique.clear()
            nextLayerNodes.clear()
            for node in currentLayerNodes:
                parent = NodeTree(node.data.parent)  # type: ignore
                try:
                    found = unique[parent]
                    if node not in found.children:
                        found.children.add(node)

                    for nextNode in nextLayerNodes:
                        if nextNode.data is parent.data:
                            break
                    else:
                        nextLayerNodes.append(parent)

                except (KeyError):
                    parent.children.add(node)
                    unique[parent] = parent
                    nextLayerNodes.append(parent)

            currentLayerNodes = list(nextLayerNodes)

        assert len(unique) == 1
        assert len(currentLayerNodes) == 1

        self.head = currentLayerNodes[0]

    def tell_me_how_many_nodes_are_on_level(self, level: int) -> int:
        if level > self.cost:
            return 1
        res = self.layers[level]
        return res

    def __repr__(self) -> str:
        res = ""
        for i, layer in enumerate(self.layers):
            res += str(i) + ": " + str(layer) + "\n"
        return res


def TEST2():
    a = Node(0, 0, 0)

    b = Node(1, 0, 1, parent=a)
    c = Node(0, 1, 1, parent=a)

    d = Node(1, 1, 2, parent=b)
    f = Node(2, 2, 2, parent=c)

    e1 = Node(1, 2, 3, parent=d)
    e2 = Node(1, 3, 3, parent=f)

    g1 = Node(3, 3, 4, parent=e1)
    g2 = Node(3, 3, 4, parent=e2)
    # g3 = Node(3, 3, 2, parent=)

    mdd = MDD([g1, g2])

    print(mdd)



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


# TEST()
