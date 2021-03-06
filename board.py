import collections
import math
from tabulate import tabulate
import os
import sys
import random
import time


class Board(collections.MutableSequence):
    def __init__(self, size, presetList=None):
        if presetList != None:
            self.slots = presetList
        else:
            self.slots = list()
            self.size = size
            for i in range(size):
                self.slots.append(i)

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

    def customBuild(self):
        usedValues = []
        validRange = list(range(self.size))
        for i in range(self.size):
            self.slots[i] = ' '
        for i in range(self.size):
            os.system('cls' if os.name == 'nt' else 'clear')
            self.slots[i] = '#'
            print(self)
            inputVal = -1
            print(set(validRange) - set(usedValues))
            while inputVal not in validRange or inputVal in usedValues:
                try:
                    inputVal = input(f'Index {i} number: ')
                    inputVal = int(inputVal)
                except:
                    if inputVal == 'quit':
                        sys.exit()
                    print('invalid input: enter "quit" to exit')
            self.slots[i] = inputVal
            usedValues.append(inputVal)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)

    def swap(self, i, j):
        a = self.slots[i]
        b = self.slots[j]
        self.slots[i] = b
        self.slots[j] = a

    def chunks(self):
        """Yield successive n-sized chunks from lst."""
        bp = int(math.sqrt(self.size))
        for i in range(0, len(self.slots), bp):
            yield (val if val != 0 else ' ' for val in self.slots[i:i + bp])

    def shuffle(self):
        random.shuffle(self.slots)

    def shuffleValid(self):
        inversions = random.randrange(14, 80, 2)
        for i in range(inversions):
            a = random.randrange(0, self.size)
            if a == 0:
                self.swap(0, 1)
            elif a == self.size - 1:
                pass
                self.swap(self.size - 1, self.size-2)
            else:
                direction = random.randrange(0, 2)
                if direction == 0:
                    self.swap(a, a-1)
                else:
                    self.swap(a, a+1)

    def __str__(self):
        return tabulate(self.chunks(), tablefmt="fancy_grid")
