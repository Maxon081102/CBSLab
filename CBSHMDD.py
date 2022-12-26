import time as timer
import os
import psutil
import heapq
import networkx as nx

def compute_cg_heuristic(paths_for_all_agent):

    mdds = []
    for agent_paths in paths_for_all_agent:
        mdd = MDD()
        mdd.build(agent_paths)
        mdds.append(mdd)

    conflict_graph = construct_conflict_graph(len(mdds), mdds)

    # print(conflict_graph)

    hval = mvc(conflict_graph)

    # print("h_val: {}".format(hval))

    if hval is None:
        return 0

    return hval

def construct_conflict_graph(num_agents, mdds):

    conflict_graph = nx.Graph()

    for outer_agent in range(num_agents):
        for inner_agent in range(outer_agent + 1, num_agents):
            # print("Comparing: {}, {}".format(outer_agent, inner_agent))
            a1_mdd = mdds[outer_agent]
            a2_mdd = mdds[inner_agent]
            # print(a1_mdd)
            # print(a2_mdd)
            min_path_length = min(len(a2_mdd.layers), len(a1_mdd.layers))

            for timestep in range(min_path_length):
                if len(a1_mdd.layers[timestep]) == 1 and len(a2_mdd.layers[timestep]) == 1:
                    # print("==============")

                    # print(a1_mdd.layers[timestep].keys())
                    # print(list(a1_mdd.layers[timestep].items())[0][1])
                    if list(a1_mdd.layers[timestep].items())[0][1] == list(a2_mdd.layers[timestep].items())[0][1]:
                        conflict_graph.add_edge(inner_agent, outer_agent)

    return conflict_graph


def mvc(g):
    for k in range(1, g.number_of_nodes()):
        if k_vertex_cover(g, k):
            return k


def k_vertex_cover(g, k):

    if g.number_of_edges() == 0:
        return True
    elif g.number_of_edges() > k*g.number_of_nodes():
        return False

    # pick any edge in graph
    v = list(g.edges())[0]
    g1 = g.copy()
    g2 = g.copy()

    g1.remove_node(v[0])
    g2.remove_node(v[1])
    # recursively check if either g1 or g2 have vertex cover of k-1
    return k_vertex_cover(g1, k-1) or k_vertex_cover(g2, k-1)


class MDD_Node:
    def __init__(self, i, j) -> None:
        self.parents = []
        self.i = i
        self.j = j
    
    def add_parent(self, parent):
        self.parents.append(parent)
    
    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, other: object) -> bool:
        return self.i == other.i and self.j == other.j

class MDD:
    def __init__(self) -> None:
        self.layers = []
    
    def build(self, paths):
        layers_count = len(paths[0])
        self.layers.append({})
        self.layers[0][MDD_Node(paths[0][0].i, paths[0][0].j)] = MDD_Node(paths[0][0].i, paths[0][0].j)
        for layer in range(1, layers_count - 1):
            self.layers.append({})
            for path in range(len(paths)):
                node = MDD_Node(paths[path][layer].i, paths[path][layer].j)
                parent_node = MDD_Node(
                    paths[path][layer].parent.i, paths[path][layer].parent.j)
                if node in self.layers[layer]:
                    self.layers[layer][node].add_parent(self.layers[layer - 1][parent_node])
                else:
                    node.add_parent(self.layers[layer - 1][parent_node])
                    self.layers[layer][node] = node





