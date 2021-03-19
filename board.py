import collections
import math
from tabulate import tabulate
import os
import sys
import random
import time
import logging
from aStar import aStar
from idfs import idfs


class Board(collections.MutableSequence):
    ''' 
    Board class for the puzzle
    \nThis class extends list, and can be manipulated like a list
    \n- access cells via [index] notation
    \n The space is stored as the number 0. When this prints out it parses as a space
    '''

    def __init__(self, size=9, presetList=None, heuristic=None, swapHistory=[]):
        '''
        size is the number of tiles to create
        \n- size is the size of puzzle to create, defaults to 9. An exception is thrown if this value is not a perfect square
        \n- presetList list of numbers to start the puzzle with. Exception is thrown if this length doesn't match the size
        \n- heuristic is the index of the heuristic to use
        '''
        self.heuristicIndex = heuristic
        self.heur = 0
        self.swapHistory = swapHistory
        if not int(math.sqrt(size) + 0.5) ** 2 == size:
            raise Exception(f'Invalid size: {size} is not a perfect square')
        if presetList != None and len(presetList) != size:
            raise Exception(
                f'Invalid list length: {presetList} isn\'t of length {size}')
        if presetList != None:
            self.slots = presetList
            self.size = size
            self.heur = self.heuristic()
        else:
            self.slots = list()
            self.size = size
            for i in range(size):
                self.slots.append(i + 1)
            self.slots[8] = 0

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

    def __eq__(self, other):
        if self.size != other.size:
            return False

        for i in range(len(self.slots)):
            if(self.slots[i] != other.slots[i]):
                return False

        return True

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

    def getNumSwaps(self):
        return len(self.swapHistory)

    def printHistory(self):
        for (i, j) in reversed(self.swapHistory):
            self.swap(i, j, recordSwap=False)

        print(f'Starting Board, swapCount: 0\n{self}\n')
        count = 0
        for (i, j) in self.swapHistory:
            self.swap(i, j, recordSwap=False)
            count += 1
            print(f'\nSwapCount: {count}\n{self}\n')

    def swap(self, i, j, force=False, recordSwap=True):
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
        if recordSwap:
            self.swapHistory.append((i, j))
        self.heur = self.heuristic()

    def branch(self, i, j):
        '''
        creates a new instance of the current board, and performs the designated swap. Returns the new instance. An exception is raised by the swap method if the indices are invalid
        '''
        nextBoard = Board(self.size, self.slots.copy(),
                          heuristic=self.heuristicIndex, swapHistory=self.swapHistory.copy())
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
        if self.heuristicIndex == None:
            return 0
        if self.heuristicIndex == 0:
            correct = 0
            correctBoard = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            for i in range(self.size):
                if correctBoard[i] == self.slots[i]:
                    correct += 1
            return self.size - correct
        if self.heuristicIndex == 1:
            distance = 0
            for i, num in enumerate(self):
                if (num == 0):
                    continue
                rowDistance = abs((num - 1) // 3 - i // 3)
                colDistance = abs((num - 1) % 3 - i % 3)
                distance += rowDistance + colDistance
            return distance

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

    def isValid(self):
        ''' determines if a board is solveable'''
        totalSwaps = 0
        for i in range(self.size):
            val = self[i]
            for j in range(self.size - i):
                innerVal = self[j + i]
                if innerVal == 0:
                    continue
                if (val > innerVal):
                    totalSwaps += 1
        return totalSwaps % 2 == 0

    def shuffleValid(self):
        '''shuffles the board into a randomly solveable position. I havn't verified that the resulting board is actually solveable'''
        self.shuffle()
        while not self.isValid():
            self.shuffle()

    def playGame(self):
        val = None
        if not self.isValid():
            print("This board has no solution")
            return
        while not self.isSolved() and val != "solve":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)
            print(f'Total moves: {len(self.swapHistory)}')
            print("type (solve) to view the solution")
            val = input(f'select tile to move (1 -> {self.size -1}): ')
            try:
                if val == "solve":
                    # solver =
                    solver = aStar('v', self)
                    solution = solver.run()
                    solution.printHistory()
                    return
                else:
                    val = int(val)
                    i = self.slots.index(val)
                    j = self.slots.index(0)
                    self.swap(i, j)
            except:
                pass
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)
        print('complete!')

    def __str__(self):
        ''' prints board out neatly'''
        return tabulate(self.chunks(), tablefmt="fancy_grid")
