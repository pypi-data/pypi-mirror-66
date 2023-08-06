import numpy as np
import pandas as pd


class Phenotype:
    """
    Phenotype class
    
    Examples
    --------
    >>> ph = Phenotype(D=10, capacity=1000)
    >>> ph.add_center(0)
    >>> ph._used_centers
    >>> ph.replace(0,8,11.9)
    >>> ph.L()
    >>> ph.replace(0,2,11.9)
    >>> ph.add_center(1)
    >>> ph.add_center(2)
    >>> ph.replace(1,2,13.9)
    >>> ph.replace(2,2,15.9)
    >>> ph.to_pandas()
         0    1     2    3    4    5    6    7     8    9
    0  0.0  0.0  11.9  0.0  0.0  0.0  0.0  0.0  11.9  0.0
    1  0.0  0.0  13.9  0.0  0.0  0.0  0.0  0.0   0.0  0.0
    2  0.0  0.0  15.9  0.0  0.0  0.0  0.0  0.0   0.0  0.0
    >>> ph.delete_center(1)
    >>> ph.to_pandas()
         0    1     2    3    4    5    6    7     8    9
    0  0.0  0.0  11.9  0.0  0.0  0.0  0.0  0.0  11.9  0.0
    2  0.0  0.0  15.9  0.0  0.0  0.0  0.0  0.0   0.0  0.0
    >>> ph.reverse_changes()
    Empty DataFrame
    Columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    Index: []
    """
    def __init__(self, D, capacity):
        self._possible_centers = np.zeros((capacity, D), dtype=np.float)
        self._capacity = capacity
        self._free_centers = list(range(capacity))[::-1]
        self._used_centers = []
        self._changes_tracker = []
        self._centers_creation = []

    def replace(self, c, d, x, memo=True):
        old_x = self._possible_centers[c,d]
        self._possible_centers[c,d] = x
        if memo: self._changes_tracker.append((c,d,old_x))

    def reverse_changes(self):
        while self._changes_tracker:
            c,d,x = self._changes_tracker.pop()
            self.replace(c, d, x, False)
        while self._centers_creation:
            c,a = self._centers_creation.pop()
            if a > 0:
                self.delete_center(c,False)
            if a < 0:
                self.add_center(c,False)

    def delete_center(self,c,memo=True):
        self._used_centers.remove(c)
        self._free_centers.append(c)
        if memo: self._centers_creation.append((c, -1))

    def empty_center_candidate(self):
        return(self._free_centers[0])

    def add_center(self,c,memo=True):
        self._free_centers.remove(c)
        self._used_centers.append(c)
        if memo: self._centers_creation.append((c, 1))

    def apply_changes(self):
        self._changes_tracker = []
        self._centers_creation = []

    def L(self):
        return(self._possible_centers[self._used_centers,:])

    def to_pandas(self):
        L = pd.DataFrame(self.L(), index = self._used_centers)
        return(L)
