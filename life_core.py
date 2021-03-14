import numpy as np


class LifeGrid:

    def __init__(self, size=(16, 16)):
        self.zeros(size)
        (self.live_min, self.live_max) = (2, 3)
        (self.birth_min, self.birth_max) = (2, 2)
        self.percent_rand = 0.5

    def __getattr__(self, attr):
        if attr == 'grid':
            return self._grid[2:-2, 2:-2]
        elif attr == 'size' or attr == 'shape':
            return (self._grid.shape[0]-4, self._grid.shape[1]-4)
        else:
            raise AttributeError

    def __getitem__(self, key):
        pass

    def __str__(self):
        return str(self.grid)

    def _convertSize(self, size):
        if size[0] <= 0:
            height = self._grid.shape[0]
        else:
            height = size[0] + 4
        if size[1] <= 0:
            width = self._grid.shape[1]
        else:
            width = size[1] + 4
        return (height, width)

    def _convertKey(self, key):
        return (key[0]+2, key[1]+2)

    def zeros(self, size=(-1, -1)):
        self._grid = np.zeros(self._convertSize(size), dtype=int)

    def rand(self, size=(-1, -1)):
        self.resize(size)
        prob = np.random.rand(self.size[0], self.size[1])
        fprob = np.vectorize(lambda x: 1 if x < self.percent_rand else 0)
        new_data = fprob(prob)
        self._grid[2:-2, 2:-2] = new_data.copy()

    def resize(self, size):
        new_size = self._convertSize(size)
        if new_size != self._grid.shape:
            new_grid = np.zeros(new_size, dtype=int)
            cp_height = min((new_size[0]-2, self._grid.shape[0]-2))
            cp_width = min((new_size[1]-2, self._grid.shape[1]-2))
            old_data = self._grid[2:cp_height, 2:cp_width]
            new_grid[2:cp_height, 2:cp_width] = old_data.copy()
            self._grid = new_grid

    def animateCell(self, key):
        self._grid[self.convertKey(key)] = 1

    def killCell(self, key):
        self._grid[self.convertKey(key)] = 0

    def getCellState(self, key):
        if self_grid[self.convertKey(key)] > 0:
            return True
        else:
            return False

    def calcMoore(self):
        g = self._grid
        sum = (g[2:, 2:]   + g[2:, 1:-1]   + g[2:, 0:-2] +
               g[0:-2, 2:] + g[0:-2, 1:-1] + g[0:-2, 0:-2] +
               g[1:-1, 2:] + g[1:-1, 0:-2])
        return sum[1:-1, 1:-1]

    def calcVonNeumann(self):
        g = self._grid
        sum = (g[2:, 1:-1] + g[0:-2, 1:-1] +
               g[1:-1, 2:] + g[1:-1, 0:-2])
        return sum[1:-1, 1:-1]

    def next_gen(self):
        pass
