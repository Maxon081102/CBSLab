import os
import sys
import pathlib
import typing as tp

import numpy as np
import pandas as pd

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from map import Map
from CBSH import CBSH
from CBS import CBS
from CBS_CP import CBS_CP

Tests = tp.List[pd.DataFrame]

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
        row_table = {'bucket': int(bucket),
                     'start_x': int(start_y),
                     'start_y': int(start_x),
                     'goal_x': int(goal_y),
                     'goal_y': int(goal_x),
                     'length': float(length)}
        rows.append(row_table)
    return pd.DataFrame(rows)

def go_insane_and_load_all_tests_from_folder(folderName: str) -> Tests:
    folder = pathlib.Path("test/data/" + folderName)
    files = []
    for file in folder.iterdir():
        s = ''.join(list(filter(str.isdigit, str(file))))
        files.append((int(s) ,str(file)))

    files.sort()
    dataFramesForTests: Tests = []
    for _, file in files:
        scen = read_scen(file)
        dataFramesForTests.append(file)

    return dataFramesForTests

go_insane_and_load_all_tests_from_folder("amongus-scen")

def perform_super_precise_tests(map: Map, dataFrames: Tests):
    



