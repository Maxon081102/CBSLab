import pathlib
import typing as tp
from dataclasses import dataclass

import numpy as np
import pandas as pd

# max time for each mini-test in seconds
TIME_LIMIT = 30

CACHE_FILE = "data/dudodi"
FOLDERPATH = "test/data/"

Tests = tp.List[pd.DataFrame]
Point = tp.Tuple[int, int]

def read_scen(filename: str) -> pd.DataFrame:
    '''
    Reads .map.scen file and writes all necessary fields into data frame

    :param filename: path to file
    '''
    with open(filename) as file:
        lines = file.readlines()
    rows: tp.List[tp.Dict] = []
    for line in lines[1:]:
        bucket, _, _, _, start_x, start_y, goal_x, goal_y, length = line.split()
        # the x-y coordiantes are flipped with matrix i-j coordinates
        # so flip them back

        # read only easy tasks
        if int(bucket) <= 10:
            row_table = {'bucket': int(bucket),
                        'start_x': int(start_y),
                        'start_y': int(start_x),
                        'goal_x': int(goal_y),
                        'goal_y': int(goal_x),
                        'length': float(length)}
            rows.append(row_table)
    base = pd.DataFrame(rows).sort_values('bucket').reset_index(drop=True)
    # base.sort_values('bucket')
    return base

def go_insane_and_load_all_tests_from_folder(folderName: str) -> Tests:
    folder = pathlib.Path(folderName)
    files = []
    for file in folder.iterdir():
        s = ''.join(list(filter(str.isdigit, str(file))))
        files.append((int(s) ,str(file)))

    files.sort()
    return [read_scen(file) for _, file in files]

import os
import sys
import time
from tqdm import tqdm
from multiprocessing import Process, Queue
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from map import Map
from astar import SearchTreePQS
from Solutions import Solutions

from collections import namedtuple

Algorithm = namedtuple("Algorithm", "name run")

# class Algorithm:
#     name: str
#     run: tp.Callable[[Map, tp.List[Point], tp.List[Point], tp.Callable, tp.Any, bool], AlgReturn]

#     def __init__(self, name: str, callFunc: tp.Callable):
#         self.name = name
#         self.run = callFunc

#     def __eq__(self, other) -> bool:
#         return self.name == other.name
        
def brooklyn(i1: int, j1: int, i2: int, j2: int) -> int:
    return abs(i1 - i2) + abs(j1 - j2)


def do_not_look_in_this_function(q, algorithm: Algorithm, map, ss, gs):
    t0 = time.process_time()
    result, explored = algorithm.run(map, ss, gs, brooklyn, SearchTreePQS, False)
    # return *algorithm.run(map, ss, gs, brooklyn, SearchTreePQS, False), time.process_time() - t0
    # give mailman a letter with our data
    # t = time.process_time() - t0
    q.put((result, explored, time.process_time() - t0))
    # q.put((result, explored, t))

def tryToTraverseHomogeniusSpace(beholding: str):
    try:
        return pd.read_csv("data/" + beholding + ".csv")
    except FileNotFoundError as spaceTimeCollapse:
        return None

def enterTheHomogeniusSpace(withA: pd.DataFrame, into: str):
    withA.to_csv("data/" + into + ".csv")


def perform_super_precise_tests(map: Map, dataFrames: Tests, algorithms: tp.List[Algorithm], beLazyAboutIt=True):
    if beLazyAboutIt:
        quiteAResult = tryToTraverseHomogeniusSpace(map.name)
        if quiteAResult is not None:
            return quiteAResult

    listOfRows = []

    # queue for getting output from different process
    # it's like a mailman
    q = Queue()
    for f in tqdm(range(len(dataFrames))):
        tests = dataFrames[f]
        # start the elimination rounds
        algorithmsLeft = list(algorithms)
        starto: tp.List[Point] = []
        finito: tp.List[Point] = []
        for i, test in tests.iterrows():
            row = {'test suite': f, 'test': i}
            start = int(test['start_x']), int(test['start_y'])  # type: ignore
            goal = int(test['goal_x']), int(test['goal_y'])  # type: ignore
            starto.append(start)
            finito.append(goal)

            # we will eliminate
            for doer in reversed(algorithmsLeft):
                p = Process(target=do_not_look_in_this_function, args=(q, doer, map, starto, finito,))
                p.start()
                p.join(timeout=TIME_LIMIT)
                if p.is_alive():
                    print(f"is about to remove the {doer}")
                    p.terminate()
                    p.join()
                    # this alg is not worthy
                    algorithmsLeft.remove(doer)
                    continue

                #  we receive a letter with data here, hopefully...
                (namingIssues, explored, t) = q.get()
                # (namingIssues, explored, t) = do_not_look_in_this_function(0, doer, map, starto, finito)
                assert namingIssues
                # if t > TIME_LIMIT:
                #     # this alg is not enough any more
                #     print(f"is about to remove the {doer}")
                #     algorithmsLeft.remove(doer)
                #     continue

                row[doer.name + '_steps'] = int(namingIssues.totalSteps)
                row[doer.name + '_expanded'] = int(explored)
                row[doer.name + '_time'] = t
            
            listOfRows.append(row)
            if not algorithmsLeft: break 

    aResult = pd.DataFrame(listOfRows)
    if beLazyAboutIt:
        enterTheHomogeniusSpace(aResult, map.name)
    return aResult