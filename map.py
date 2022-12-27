import numpy as np

class Map:

    def __init__(self):
        '''
        Default constructr

        don't ask
        '''
        self._width = 0
        self._height = 0
        self._cells = []
        self.name = ""

    def convert_back(self) -> str:
        res = ""
        for i in range(self._height):
            for j in range(self._width):
                res += "@" if self._cells[i][j] == 1 else "."
            res += '\n'
        file = open("test.txt", "w")
        file.write(res)
        file.close()
        return res


    def read_from_map(self, filename: str):
        '''
        Read the map file and load it

        :param filename: name of the file
        '''
        with open(filename) as file:
            lines = file.readlines()

        self._height = int(lines[1].split()[1])
        self._width = int(lines[2].split()[1])
        self._cells = np.zeros((self._height, self._width), dtype=int)

        assert len(lines[4:]) == self._height, 'height of the map should match given height'

        for i, line in enumerate(lines[4:]):
            assert len(line.strip()) == self._width, 'width of each row should match given width'
            for j, c in enumerate(line.strip()):
                if c not in ('.', 'T', '@'):
                    print("some werid")
                self._cells[i][j] = (0 if c == '.' else 1)
    

    def read_from_string(self, cell_str, width, height):
        '''
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
        '''
        self._width = width
        self._height = height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self._cells[i][j] = 0
                    elif c == '#':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                
                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )
    
     
    def set_grid_cells(self, width, height, grid_cells):
        '''
        Initialization of map by list of cells.
        '''
        self._width = width
        self._height = height
        self._cells = grid_cells


    def in_bounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self._width) and (0 <= i < self._height)
    

    def traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        ''' 
        return not self._cells[i][j]


    def get_neighbors(self, i, j):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 4-connected (i.e. only moves into cardinal directions are allowed)
        '''  
        
        neighbors = []
        delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        return neighbors

    def get_size(self):
        return (self._height, self._width)



