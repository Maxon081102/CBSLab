import math
import heapq

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from time import time
from PIL import Image, ImageDraw
from heapq import heappop, heappush


class BaseNode:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __repr__(self) -> str:
        return f"({self.i}, {self.j})"

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, other) -> bool:
        return self.i == other.i and self.j == other.j

    def __lt__(self, other):
        return self.i < other.i if self.i != other.i else self.j < other.j


class Agent:
    def __init__(self, index, start=(0, 0), finish=(0, 0)) -> None:
        self.index = index
        self.start = BaseNode(start[0], start[1])
        self.goal = BaseNode(finish[0], finish[1])

    def __eq__(self, other):
        return self.index == other.index

    def __lt__(self, other):
        return self.index < other.index

    def __repr__(self):
        return f"Agent #{self.index}"

    def __hash__(self):
        return self.index
