import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw, ImageOps
from IPython.display import display
from IPython.display import Image as Img
from heapq import heappop, heappush

def draw(grid_map, start = None, goal = None, path = None, nodes_opened = None, nodes_expanded = None, nodes_reexpanded = None, pt = False):
    '''
    Auxiliary function that visualizes the environment, the path and 
    the open/expanded/re-expanded nodes.
    
    The function assumes that nodes_opened/nodes_expanded/nodes_reexpanded
    are iterable collestions of SearchNodes
    '''
    k = 5
    height, width = grid_map.get_size()
    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color = 'white')
    draw = ImageDraw.Draw(im)
    points = [[0,1], [1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1], [0, -1], [-1, 0],
            [0,2], [2, 0], [2, 2], [-2, -2], [-2, 2], [2, -2], [0, -2], [-2, 0]]
        
    
    for i in range(height):
        for j in range(width):
            if not grid_map.traversable(i, j):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=( 0, 0, 0 ))
    if nodes_opened is not None:
        for node in nodes_opened:
            draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1), fill=(213, 219, 219), width=0)
    
    if nodes_expanded is not None:
        for node in nodes_expanded:
            draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1), fill=(131, 145, 146), width=0)
    
    if nodes_reexpanded is not None:
        for node in nodes_reexpanded:
                draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1), fill=(255, 145, 146), width=0)
    
    if path is not None:
        for step in path:
            if (step is not None):
                if (grid_map.traversable(step.i, step.j)):
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1), fill=(231, 76, 60), width=0)
                else:
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1), fill=(230, 126, 34), width=0)

    if (start is not None) and (grid_map.traversable(start.i, start.j)):
        draw.rectangle((start.j * k, start.i * k, (start.j + 1) * k - 1, (start.i + 1) * k - 1), fill=(40, 180, 99), width=0)
    
    if (goal is not None) and (grid_map.traversable(goal.i, goal.j)):
        draw.rectangle((goal.j * k, goal.i * k, (goal.j + 1) * k - 1, (goal.i + 1) * k - 1), fill=(255, 0, 0), width=0)

    if pt:
        for point in points:
            if grid_map.in_bounds(start.i + point[0], start.j + point[1]):
                i = start.i + point[0]
                j = start.j + point[1]
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(231, 76, 60))
            if grid_map.in_bounds(goal.i + point[0], goal.j + point[1]):
                i = goal.i + point[0]
                j = goal.j + point[1]
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(231, 76, 60))
                
    _, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(np.asarray(im))
    plt.show()


def draw_dynamic(grid_map, sol, output_filename = 'animated_trajectories'):
    m = 30
    quality = 6
    
    k = len(sol.solutions)
    max_len = 0
    for s in sol.solutions:
        max_len = max(max_len, len(s.get_path()))
    
    height, width = grid_map.get_size()
    h_im = height * m
    w_im = width * m
    
    step = 0
    images = []
    agent_colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(k)]
              
    while step < max_len:
        for n in range(0, quality):
            im = Image.new('RGB', (w_im, h_im), color = 'white')
            draw = ImageDraw.Draw(im)
            
            # draw static obstacles
            for i in range(height):
                for j in range(width):
                    if(not grid_map.traversable(i, j)):
                        draw.rectangle((j * m, i * m, (j + 1) * m - 1, (i + 1) * m - 1), fill=( 70, 80, 80 ))
                   
            
            #draw agents
            for i, s in enumerate(sol.solutions):
                path = s.get_path()
                pathlen = len(path)
                curr_node = path[min(pathlen - 1, step)]
                next_node = path[min(pathlen - 1, step + min(n, 1))]

                di = n * (next_node.i - curr_node.i) / quality
                dj = n * (next_node.j - curr_node.j) / quality

                draw.ellipse((float(curr_node.j + dj + 0.2) * m, 
                              float(curr_node.i + di + 0.2) * m, 
                              float(curr_node.j + dj + 0.8) * m - 1, 
                              float(curr_node.i + di + 0.8) * m - 1), 
                              fill=agent_colors[i], width=0)
            
            im = ImageOps.expand(im, border=2, fill='black')
            images.append(im)
        step += 1
        print("step")
    images[0].save('./'+output_filename+'.png', save_all=True, append_images=images[1:], optimize=False, duration=500/quality, loop=0)
    display(Img(filename = './'+output_filename+'.png'))