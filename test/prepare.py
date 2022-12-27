import os
import sys
import typing as tp
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from CBS import CBS
from CBS_CP import CBS_CP
from CBSH import CBSH

from test import Algorithm, Tests, go_insane_and_load_all_tests_from_folder
from map import Map

allWeHave = [
    Algorithm("standard", CBS),
    Algorithm("prioritizing", CBS_CP),
    Algorithm("heuristic", CBSH)
]

maps = ["nlo", "milklake", "amongus"]

def gimmemymaps() -> tp.Dict[str, Map]:
    gimme = {}
    for name in maps:
        m = Map()
        m.name = name
        m.read_from_map("data/" + name + ".map")
        gimme[name] = m
    return gimme

def gimmemydata() -> tp.Dict[str, Tests]:
    gimme = {}
    for key in maps:
        gimme[key] = go_insane_and_load_all_tests_from_folder("data/" + key + "-scen")
    return gimme

def testSanity():
    with open("test/data/nlo.map") as orig:
        lines = orig.readlines()
        newlines = []
        for i in range(len(lines)):
            l = ""
            for j in range(len(lines[i])):
                if lines[i][j] == '\n': l += '\n'; continue
                if lines[i][j] != '.': l += '@'
                else: l += '.'
            newlines.append(l)

        assert ''.join(newlines[4:]) == a