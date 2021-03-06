import collections
import math
from tabulate import tabulate
import os
import sys
import random
import time
import logging


class Board(collections.MutableSequence):
    ''' 
    Board class for the puzzle
    \nThis class extends list, and can be manipulated like a list
    \n- access cells via [index] notation
    \n The space is stored as the number 0. When this prints out it parses as a space
    '''

    def __init__(self, size=9, presetList=None, heuristic=None):
        '''
        size is the number of tiles to create
        \n- size is the size of puzzle to create, defaults to 9. An exception is thrown if this value is not a perfect square
        \n- presetList list of numbers to start the puzzle with. Exception is thrown if this length doesn't match the size
        \n- heuristic is the index of the heuristic to use
        '''
        if not int(math.sqrt(size) + 0.5) ** 2 == size:
            raise Exception(f'Invalid size: {size} is not a perfect square')
        if presetList != None and len(presetList) != size:
            raise Exception(
                f'Invalid list length: {presetList} isn\'t of length {size}')
        if presetList != None:
            self.slots = presetList
            self.size = size
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
        '''
        Walks the user through assigning the numbers in the grid
        '''
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

    def swap(self, i, j, force=False):
        '''
        swaps two cells in the puzzle. An exception is raised if the indices are an invalid move
        passing force as true doesn't check the bounds before swapping
        '''
        if not force:
            if i < 0 or i >= self.size:
                raise Exception(
                    f'Invalid swap bounds. {i} is not within the board constraints')
            if j < 0 or j >= self.size:
                raise Exception(
                    f'Invalid swap bounds. {j} is not within the board constraints')
            if not (self.slots[i] == 0 or self.slots[j] == 0):
                raise Exception(
                    f'Invalid swap bounds. neither {i} nor {j} are the empty space')
            if not (abs(i - j) == int(math.sqrt(self.size)) or abs(i-j) == 1):
                raise Exception(
                    f'Invalid swap bounds. {i} is not swappable with {j}')
        a = self.slots[i]
        b = self.slots[j]
        self.slots[i] = b
        self.slots[j] = a

    def branch(self, i, j):
        '''
        creates a new instance of the current board, and performs the designated swap. Returns the new instance. An exception is raised by the swap method if the indices are invalid
        '''
        nextBoard = Board(self.size, self.slots.copy())
        nextBoard.swap(i, j)
        return nextBoard

    def branches(self):
        '''
        returns a list of new board objects for every possible swap available. If an exception is raised this is due to an internal logical error
        '''
        def swapIndexes(index):
            indexes = []
            length = int(math.sqrt(self.size))
            # if not in last row, add lower index
            if index + length < self.size:
                indexes.append(index + length)
            # check row above
            if index - length >= 0:
                indexes.append(index - length)
            # check column left
            if index % length != 0:
                indexes.append(index - 1)
            # check column right
            if index % length != length - 1:
                indexes.append(index + 1)
            return indexes
        nextBranches = []
        blank = self.slots.index(0)
        for index in swapIndexes(blank):
            nextBranches.append(self.branch(blank, index))
        return nextBranches

    def heuristic(self):
        ''' todo: work in progress'''
        if self.heuristic == None:
            return 1

    def isSolved(self):
        ''' returns true if the board is solved'''
        lastVal = 0
        for i in self.slots:
            if i == 0:
                continue
            if i < lastVal:
                return False
            lastVal = i
        return True

    def chunks(self):
        """Yield successive n-sized chunks from lst. this is used for printing"""
        bp = int(math.sqrt(self.size))
        for i in range(0, len(self.slots), bp):
            yield (val if val != 0 else ' ' for val in self.slots[i:i + bp])

    def shuffle(self):
        '''shuffles the board randomly. This may not be solveable'''
        random.shuffle(self.slots)

    def shuffleValid(self):
        '''shuffles the board into a randomly solveable position. I havn't verified that the resulting board is actually solveable'''
        inversions = random.randrange(14, 80, 2)
        for i in range(inversions):
            a = random.randrange(0, self.size)
            if a == 0:
                self.swap(0, 1, True)
            elif a == self.size - 1:
                pass
                self.swap(self.size - 1, self.size-2, True)
            else:
                direction = random.randrange(0, 2)
                if direction == 0:
                    self.swap(a, a-1, True)
                else:
                    self.swap(a, a+1, True)

    def playGame(self):
        self.shuffleValid()
        while not self.isSolved():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)
            val = int(input('select tile to move: '))
            i = self.slots.index(val)
            j = self.slots.index(0)
            try:
                self.swap(i, j)
            except:
                pass
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)
        print('complete!')

    def __str__(self):
        ''' prints board out neatly'''
        return tabulate(self.chunks(), tablefmt="fancy_grid")
