import collections
import math
from tabulate import tabulate


class Board(collections.MutableSequence):
    def __init__(self, size):
        self.slots = list()
        self.size = size
        for i in range(size):
            self.slots.append(i)
        self.slots[0] = ' '

    def __len__(self):
        return len(self.slots)

    def __delitem__(self, index):
        self.slots.__delitem__(index)

    def insert(self, index, value):
        self.slots.insert(index, value)

    def __setitem__(self, index, value):
        self.slots.__setitem__(index, value)

    def __getitem__(self, index):
        return self.slots.__getitem__(index)

    def append(self, value):
        self.insert(len(self) + 1, value)

    def swap(self, i, j):
        a = self.slots[i]
        b = self.slots[j]
        self.slots[i] = b
        self.slots[b] = a

    def chunks(self):
        """Yield successive n-sized chunks from lst."""
        bp = int(math.sqrt(self.size))
        for i in range(0, len(self.slots), bp):
            yield self.slots[i:i + bp]

    def __str__(self):
        return tabulate(self.chunks(), tablefmt="fancy_grid")
