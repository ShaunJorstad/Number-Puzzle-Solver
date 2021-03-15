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
        self.board.shuffleValid()
        self.boardsToLookAt.append(self.board)
        h = self.board.heuristic()

        while self.boardsToLookAt: #still have paths left
            #get best path
            bestCurrentBoard = self.boardsToLookAt[self.bestBoard()]
            #if solved break
            if(bestCurrentBoard.isSolved()):
                return bestCurrentBoard
            #remove the currentBoard
            self.boardsToLookAt.remove(bestCurrentBoard)
            self.boardsLookedAt.append(bestCurrentBoard)
            #add all the boards that we haven't already analyzed
            for board in bestCurrentBoard.branches():
                if board not in self.boardsLookedAt:
                    self.boardsToLookAt.append(board)
        if not self.boardsToLookAt:
            self.board() #return original board if not found 
        
    
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

