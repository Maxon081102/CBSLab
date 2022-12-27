import os
import sys
import time

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import math
import heapq
from heapq import heappop, heappush
from time import time
from IPython.display import Image as Img

from map import Map
from CBS_DS import CBS_DS
from astar import distance
from CBS_Tree import CBS_tree



def read_task_from_file(path):
    '''
    Reads map, start/goal positions and true value of path length between given start and goal from file by path. 
    '''

    tasks_file = open(path)
    height, width = map(int, tasks_file.readline().split())
    cells = [[0 for _ in range(width)] for _ in range(height)]
    i = 0
    j = 0

    for l in tasks_file:
        j = 0
        for c in l:
            if c == '.':
                cells[i][j] = 0
            elif c == '@':
                cells[i][j] = 1
            else:
                continue
            j += 1
            
        if j != width:
            raise Exception("Size Error. Map width = ", j, ", but must be", width, "(map line: ", i, ")")
                
        i += 1
        if(i == height):
            break
    agent_count = int(tasks_file.readline())
    starts = []
    goals = []
    for agent in range(agent_count):
        start_i, start_j, goal_i, goal_j = map(int, tasks_file.readline().split())
        starts.append((start_i, start_j))
        goals.append((goal_i, goal_j))
    
    return (width, height, cells, starts, goals)


tests = os.listdir("instances")
results = open("CBS_DS/results.txt", "w")

for i, testname in enumerate(tests):
    width, height, cells, starts, goals = read_task_from_file("./instances/" + testname)

    grid_map = Map()
    grid_map.set_grid_cells(width, height, cells)
    t1 = time()
    solution = CBS_DS(grid_map, starts, goals, distance, CBS_tree)
    t2 = time()
    results.write(str(i) + ') ' + testname + '\n')
    results.write("TIME " + str(t2 - t1) + '\n')
    results.write("COST: " + str(solution.get_cost()) + '\n')
    print(i)
results.close()