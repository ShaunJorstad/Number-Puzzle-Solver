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

    def run(self):
        print('running the a* algorithm')
        self.board.shuffle()
        print("Original Board")
        print(self.board)
        h = self.board.heuristic()

        self.boardsToLookAt = self.board.branches()

        while self.boardsToLookAt: #still have paths left
            #get best path
            bestCurrentBoard = self.boardsToLookAt[self.bestBoard()]
            #Print Best Board so far
            if (bestCurrentBoard.heuristic() < h):
                h = bestCurrentBoard.heuristic()
                print("Best Board")
                print(bestCurrentBoard)
                print("Best Heuristic: " + str(bestCurrentBoard.heuristic()))
            if(bestCurrentBoard.isSolved()):
                print("Solved!!")
                print(bestCurrentBoard)
                break
            self.boardsToLookAt.remove(bestCurrentBoard)
            self.boardsLookedAt.append(bestCurrentBoard)
            #add all the boards that we haven't already analyzed
            for board in bestCurrentBoard.branches():
                if board not in self.boardsLookedAt:
                    self.boardsToLookAt.append(board)
        if not self.boardsToLookAt:
            print(f"Could not solve, looked at {len(self.boardsLookedAt)} boards.")
        
    
    def bestBoard(self):
        '''Return the index to the board with the lowest heuristic'''
        lowestHeuristicBoard = self.boardsToLookAt[0]
        for board in self.boardsToLookAt:
            if board.heuristic() < lowestHeuristicBoard.heuristic():
                lowestHeuristicBoard = board
        
        return self.boardsToLookAt.index(lowestHeuristicBoard)


#for testing
a = ass(logging.DEBUG, Board(9, heuristic = 1))
a.run()

