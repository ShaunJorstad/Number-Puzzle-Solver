import logging
import sys
from board import Board


class ass:
    '''Class that solves puzzle via A* search'''

    def __init__(self, loggingLevel, board, boardsToLookAt=None, boardsLookedAt=None, paths=None):
        self.loggingLevel = loggingLevel
        self.board = board
        self.boardsToLookAt = []
        self.boardsLookedAt = []
        self.paths = []

    def run(self, parallel=False, smart=False):
        print('running the a* algorithm')
        self.boardsToLookAt.append(self.board)
        levelsDeep = 0

        while self.boardsToLookAt:  # still have paths left
            # get best path
            bestCurrentBoard = self.boardsToLookAt[self.bestBoardIndex()]
            # if solved break
            if(bestCurrentBoard.isSolved()):
                print()
                return bestCurrentBoard
            #print progress bar
            if levelsDeep < bestCurrentBoard.getNumSwaps():
                levelsDeep = bestCurrentBoard.getNumSwaps()
                #clear writeout
                sys.stdout.write('\r')
                # the exact output you're looking for:
                sys.stdout.write("[%-20s] %d%%" % ('='*levelsDeep, 5*levelsDeep))
                print(f'.', end='')
            
            # remove the currentBoard
            self.boardsToLookAt.remove(bestCurrentBoard)
            self.boardsLookedAt.append(bestCurrentBoard)
            # add all the boards that we haven't already analyzed
            for board in bestCurrentBoard.branches():
                if board not in self.boardsLookedAt:
                    self.boardsToLookAt.append(board)
        if not self.boardsToLookAt:
            print()
            self.board()  # return original board if not found

    def bestBoardIndex(self):
        '''Return the index to the board with the lowest heuristic'''
        lowestHeuristicBoard = self.boardsToLookAt[0]
        for board in self.boardsToLookAt:
            if board.heuristic() + board.getNumSwaps() < lowestHeuristicBoard.heuristic() + lowestHeuristicBoard.getNumSwaps():
                lowestHeuristicBoard = board

        return self.boardsToLookAt.index(lowestHeuristicBoard)


# for testing
# b = Board(9, heuristic=1)
# b.shuffleValid()
# a = ass(logging.DEBUG, b)
# final = a.run()
# final.printHistory()
