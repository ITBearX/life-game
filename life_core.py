import logging
import numpy as np


def moore_nbr(g):
    s = (
        g[2:, 2:] + g[2:, 1:-1] + g[2:, 0:-2] +
        g[0:-2, 2:] + g[0:-2, 1:-1] + g[0:-2, 0:-2] +
        g[1:-1, 2:] + g[1:-1, 0:-2]
    )
    return s[1:-1, 1:-1]


def von_neumann_nbr(g):
    s = (
        g[2:, 1:-1] + g[0:-2, 1:-1] +
        g[1:-1, 2:] + g[1:-1, 0:-2]
    )
    return s[1:-1, 1:-1]


class LifeGrid:

    def __init__(
        self,
        rows=16, cols=16,
        h_wrap=False, v_wrap=False,
        nbr_func = moore_nbr,
        alive_nbr_min=2, alive_nbr_max=3,
        birth_nbr_min=3, birth_nbr_max=3
    ):
        self.zeros(rows, cols)
        self.nbr_func = nbr_func
        self.h_wrap, self.v_wrap = h_wrap, v_wrap
        self.alive_nbr_min, self.alive_nbr_max = alive_nbr_min, alive_nbr_max
        self.birth_nbr_min, self.birth_nbr_max = birth_nbr_min, birth_nbr_max

    def __getattr__(self, attr):
        if attr == 'grid':
            return self._grid[2:-2, 2:-2]
        elif attr in ('size', 'shape'):
            return (self._grid.shape[0] - 4, self._grid.shape[1] - 4)
        elif attr in ('rows', 'height'):
            return self._grid.shape[0] - 4
        elif attr in ('cols', 'width'):
            return self._grid.shape[1] - 4
        raise AttributeError

    def __getitem__(self, key):
        if self._grid[self._np_key(key)] > 0:
            return True
        return False

    def __setitem__(self, key, value):
        self._grid[self._np_key(key)] = 1 if value > 0 else 0

    def __str__(self):
        return str(self.grid)

    def zeros(self, rows=-1, cols=-1):
        '''Make an empty grid'''
        self._grid = np.zeros(self._np_size(rows, cols), dtype=int)

    def rand(self, alive_perc=0.5, rows=-1, cols=-1):
        '''Make a random grid'''
        self.resize(rows, cols, False)
        prob = np.random.rand(self.rows, self.cols)
        fprob = np.vectorize(lambda x: 1 if x < alive_perc else 0)
        new_data = fprob(prob)
        self._grid[2:-2, 2:-2] = new_data.copy()

    def resize(self, rows=-1, cols=-1, keep_data=True):
        new_size = self._np_size(rows, cols)
        if new_size != self._grid.shape:
            new_grid = np.zeros(new_size, dtype=int)
            if keep_data:
                cp_rows = min((new_size[0], self._grid.shape[0])) - 2
                cp_cols = min((new_size[1], self._grid.shape[1])) - 2
                old_data = self._grid[2:cp_rows, 2:cp_cols]
                new_grid[2:cp_rows, 2:cp_cols] = old_data.copy()
            self._grid = new_grid
            return True
        return False

    def next_gen(self):
        self._wrap_append()
        nbr = self.nbr_func(self._grid)
        keep_alive = (self.alive_nbr_min <= nbr) & (nbr <= self.alive_nbr_max)
        give_birth = (self.birth_nbr_min <= nbr) & (nbr <= self.birth_nbr_max)
        self._grid[2:-2, 2:-2] = (keep_alive & self.grid) | give_birth

    def load(self, f_name):
        with open(f_name, 'rb') as f:
            ld_data = np.load(f)
            logging.info(f'Loaded shape:{ld_data.shape[0]},{ld_data.shape[1]}')
            self.resize(ld_data.shape[0], ld_data.shape[1])
            logging.info(f'Resized shape:{self.rows},{self.cols}')
            self._grid[2:-2, 2:-2] = ld_data.copy()

    def save(self, f_name):
        with open(f_name, 'wb') as f:
            np.save(f, self.grid)

    def _np_size(self, rows, cols):
        '''Return the grid actual size with helper rows/cols'''
        if rows <= 0:
            rows = self._grid.shape[0]
        else:
            rows += 4
        if cols <= 0:
            cols = self._grid.shape[1]
        else:
            cols += 4
        return (rows, cols)

    def _np_key(self, key):
        '''Adjust coordinates to access internal numpy grid'''
        return (key[0] + 2, key[1] + 2)

    def _wrap_append(self):
        '''Fill helper extra rows/cols if the grid is wrapped'''

        wrap_table = [2, 3, -4, -3]
        if self.v_wrap:
            for (i, j) in enumerate(wrap_table, start=-2):
                self._grid[i, :] = self._grid[j, :]
        else:
            for i in range(-2, 2):
                self._grid[i, :] = np.zeros((self._grid.shape[1]), dtype=int)
        if self.h_wrap:
            for (i, j) in enumerate(wrap_table, start=-2):
                self._grid[:, i] = self._grid[:, j]
        else:
            for i in range(-2, 2):
                self._grid[:, i] = np.zeros((self._grid.shape[0]), dtype=int)
