from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import math
import heapq
from heapq import heappop, heappush
from time import time
from IPython.display import Image as Img

from map import Map
from draw import draw, draw_dynamic
from CBS_DS import CBS_DS
from Solutions import make_path
from astar import Node, distance, SearchTreePQS


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


height = 15
width = 30

test_map_str_1 = '''
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
'''

test_map_str_2 = '''
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
. . # # # # # # # # . . . . . . . . . . . # # . . . . . . . 
# . # . . . . . . . . . . . . . . . . . . # # . . . . . . . 
# . # . # # # # # # . . . . . . . . . . . # # . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . # # . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . # # # # # . . . . 
# . # . # . . . . . . . . # # . . . . . . # # # # # . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . . 
# . # . # . . . . . . . . # # . . . . . . . . . . . . . . .
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
'''

test_map_str_3 = '''
# . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
# . # . # # # . . . . . . . . . . . . . . # # . . . . . . . 
# . # . . . # . . . . . . . . . . . . . . # # . . . . . . . 
# . # # # . # . . . . . . . . . . . . . . # # . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . # # . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . # # # # # . . . . 
# . # # # . # . . . . . . # # . . . . . . # # # # # . . . . 
# . # # # . # . . . . . . # # . . . . . . . . . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . . . . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . . . . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . . . . . . . . . . 
# . # # # . # . . . . . . # # . . . . . . . . . . . . . . . 
# . # . . . # . . . . . . # # . . . . . . . . . . . . . . . 
# . . . # # # . . . . . . # # . . . . . . . . . . . . . . .
# # # # # . . . . . . . . # # . . . . . . . . . . . . . . .
'''

test_maps = [
    test_map_str_1, 
    test_map_str_2,
    test_map_str_3
]

test_map_1 = Map()

test_on_map_1 = [
    [
        [[0, 0], [0, 1]], 
        [[2, 2], [10, 1]]
    ],
    [
        [[4, 1], [10, 1]], 
        [[10, 1], [4, 1]]
    ],
    [
        [[0, 1], [0, 0]], 
        [[10, 1], [2, 2]]
    ],
    [
        [[9, 22], [9, 28], [6, 25]], 
        [[9, 28], [9, 22], [12, 25]]
    ],
    [
        [[0, 0], [0, 1], [1, 0]], 
        [[2, 2], [10, 1], [1, 3]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1]], 
        [[2, 2], [10, 1], [1, 3], [10, 10]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1]], 
        [[2, 2], [0, 0], [1, 3], [10, 10]]
    ],
    [
        [[0, 0], [0, 1]], 
        [[0, 1], [0, 0]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1]], 
        [[1, 1], [1, 0], [0, 1], [0, 0]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1], [2, 1], [1, 2], [2, 0], [0, 2]],
        [[1, 1], [1, 0], [0, 1], [0, 0], [0, 2], [2, 0], [1, 2], [2, 1]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1], [0, 2], [1, 2]], 
        [[0, 10], [10, 0], [1, 10], [10, 1], [1, 1], [1, 0], [0, 1], [0, 0]]
    ]
]

test_on_map_2 = [
    [
        [[0, 0], [0, 1]], 
        [[2, 3], [10, 1]]
    ],
    [
        [[1, 0], [0, 1]], 
        [[11, 1], [10, 1]]
    ],
    [
        [[1, 0], [0, 1]], 
        [[10, 1], [11, 1]]
    ],
    [
        [[0, 0], [0, 1], [1, 0], [1, 1]], 
        [[10, 3], [10, 1], [11, 3], [12, 1]]
    ]
]

test_on_map_3 = [
    [
        [[4, 1], [10, 1]], 
        [[10, 1], [4, 1]]
    ]
]

tests = [
    test_on_map_1,
    test_on_map_2,
    test_on_map_3
]

def test_cbs_on_map(number, number_test, show_debug=False, show_all_solution=True, show_path=True):
    test_map = Map()
    test_map.read_from_string(test_maps[number], width, height) 
    starts_points = tests[number][number_test][0]
    goal_points = tests[number][number_test][1]
    draw(test_map)
    sol = CBS_DS(test_map, starts_points, goal_points, distance, SearchTreePQS, show_debug)
    if show_all_solution:
        for i in range(len(starts_points)):
            print(sol.get_solution_of_robot(i).get_path())
            draw(test_map, Node(starts_points[i][0], starts_points[i][1]), Node(goal_points[i][0], goal_points[i][1]), sol.get_solution_of_robot(i).get_path())
    if show_path:
        for i in range(len(starts_points)):
            print(sol.get_solution_of_robot(i).get_path())


def test_cbs_on_map_dynamic(number, number_test, show_debug=False, show_all_solution=True, show_path=True):
    test_map = Map()
    test_map.read_from_string(test_maps[number], width, height) 
    starts_points = tests[number][number_test][0]
    goal_points = tests[number][number_test][1]
    sol = CBS_DS(test_map, starts_points, goal_points, manhattan, SearchTreePQS, show_debug)
    draw_dynamic(test_map, sol)

