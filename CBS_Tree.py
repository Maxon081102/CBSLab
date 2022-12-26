import math
import heapq
from heapq import heappop, heappush
from time import time

class CBS_tree:
    def __init__(self):
        self._open = []
        heapq.heapify(self._open)
        self._closed = {}
    
    def open_is_empty(self):
        return len(self._open) == 0
    
    def add_to_open(self, item):
        heapq.heappush(self._open, item)
    
    def get_best_node_from_open(self):
        best_node = heapq.heappop(self._open)
        while self.was_expanded(best_node) and len(self._open) > 0:
            best_node = heapq.heappop(self._open)     
        return best_node
    
    def add_to_closed(self, item):
        self._closed[item] = item

    def was_expanded(self, item):
        try:
            node = self._closed[item]
            return True
        except KeyError:
            return False
    
    @property
    def OPEN(self):
        return self._open
    
    @property
    def CLOSED(self):
        return self._closed