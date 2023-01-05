import numpy as np
from collections import namedtuple

Point = tuple[int, int]
Edge = tuple[Point, Point]


class Map:
    """ 
    Stores map as numpy byte array with shape = (width, height)

    1 - for wall, 0 - for traversable path
    """

    def read_map(self, filename: str):
        """
        Read the map file and fill bool array
        it considers '.' symbol as traversable and everything else as wall

        :param filename: name of the file
        """
        with open(filename) as file:
            lines = file.readlines()
        self.height = int(lines[1].split()[1])
        self.width = int(lines[2].split()[1])
        self._init_cells(lines[4:])
    
    def read_txt(self, lines: list[str]):
        """ Does the same as `read_from_map` but now reads from lines in special format (instances folder) """

        self.height, self.width = map(int, lines[0].split())
        self._init_cells(lines[1:self.height + 1], skip_spaces=True)

    def read_string(self, string: str):
        """ Does the same as `read_from_map` but now reads from string (with raw map) """

        lines = string.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])
        self._init_cells(lines)

    def _init_cells(self, lines: list[str], skip_spaces=False):
        self.cells = np.zeros((self.height, self.width), dtype=np.int8)
        assert len(lines) == self.height, 'height of the map should match given height'
        for i, line in enumerate(lines):
            j = 0
            for c in line.strip():
                if skip_spaces and c == ' ': continue
                self.cells[i, j] = (c != '.')
                j += 1

            assert j == self.width, 'width of each row should match given width'
