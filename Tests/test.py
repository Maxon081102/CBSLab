import sys
import time
import shutil
import os.path
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Callable, Optional

from Primitives.node import Node
from Primitives.map import Map

from mapf import MAPF
from graphics import animate_solutions

import cbs

# Should be universal type for all CBS-like algorithms
Solver = Callable[[MAPF], Optional[Node]]


def copy_solution_file(tmp_file: str):
    filename = "solutions.gif"
    i = 1
    while os.path.isfile(filename):
        filename = f"solutions{i}.gif"
        i += 1

    shutil.copyfile(tmp_file, parent_dir + "/saved/" + filename)


def base_test(task: MAPF, algorithm: Solver, *, show=False, save=False) -> tuple[Node, float, float]:
    """
    This function designed to be the base testing function for all CBS-like algorithms
    
    It means that in order to test any CBS-like algorithm you should call this function, providing 
    you algorithm as this functions's `algorithm`

    - task: MAPF task to test the algorithm on
    - algorithm: Callable function which returns the node as it's final result
    - show: boolean blag indicating if we need to draw an animated solution to this test
    - save: boolean flag, whether we should save the received result in the special folder called `save`
    """

    # TODO: try
    start_cpu_time = time.process_time()
    start_wall_time = time.time()
    result = algorithm(task)
    wall_time = time.time() - start_wall_time
    cpu_time = time.process_time() - start_cpu_time
    assert result
    if not show and not save:
        return (result, cpu_time, wall_time)

    tmp_file = animate_solutions(task.map, result, show=show)
    if save:
        copy_solution_file(tmp_file)

    return (result, cpu_time, wall_time)


def test_correctness(algorithm: Solver = cbs.find_agents_paths, can_fail_before_quit=10):
    """ 
    Validate correctness of an algorithm by comparing its solutions to the precomputed ones
    
    - algorithm: CBS algorithm to test
    - can_fail_before_quit: number of failed tests allowed before quiting this test
        It's just for debugging purposes, if your algorithm failed at least one test, 
        then it's incorrect no matter what the value of this property, just not to give any false hopes....
    """
    num_tests = 50
    failed = 0
    answers = pd.read_csv(current_dir + "/instances/min-sum-of-cost.csv")
    for i, (name, cost) in tqdm(answers.iterrows()):
        task = MAPF()
        task.read_txt(current_dir + '/' + name)
        result, _, _ = base_test(task, algorithm)
        if result.cost != cost:
            print(
                f"❌❌❌ 😰😡😩 Fail on test {i + 1}: cost found = {result.cost} ≠ {cost}, file: {name} ❌❌❌"
            )
            failed += 1
            if failed >= can_fail_before_quit:
                return

    if failed == 0:
        print(
            "️✅✅️✅ Congratulations! 🤩 Your algorithm hse passed all tests! 😎😎😎"
        )


def simple_test(filename: str, algorithms: list[Solver] = [cbs.find_agents_paths], draw=True):
    """ 
    Tests algorithms (one or multiple) on one test, giving maximum information 

    - filename: name of the test file in .txt format (as always), 
        filename MUST be relative to the `Tests` directory
    - algorithms: list of all algorithms to test, default is the standard cbs algorithm
    - whether or not to draw animated solution, it may take some time
    """

    task = MAPF()
    task.read_txt(current_dir + '/' + filename)

    for algorithm in algorithms:
        print(f"Testing '{algorithm.__name__}' algorithm on the map '{filename}':")
        result, cpu_time, wall_time = base_test(task, algorithm, show=draw)
        if result is None:
            print("Path not fount!")
            continue
        print(f"Found solution with cost = {result.cost}")
        print(f"CPU time = {cpu_time} seconds, Wall time = {wall_time} seconds")
        print("Agent paths:")
        for solution in result.solutions:
            print(f"[{solution.agent_id}] = ", end="")
            for i, point in enumerate(solution._path):
                print(f"({point[0]}, {point[1]})", end="")
                if i != len(solution._path - 1):
                    print(" -> ", end="")
                else:
                    print(", ", end="")
            print(f"cost = {solution.cost}")
        print("--------------------------------------------------------------------------\n")
