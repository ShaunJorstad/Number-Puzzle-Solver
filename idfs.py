
from board import Board
from multiprocessing import Pool
from time import time
import numpy as np  
import matplotlib.pyplot as plt 

class idfs:
    '''Class that solves via brute force bfs'''

    MAX_DEPTH = 15

    def __init__(self, loggingLevel, board):
        self.loggingLevel = loggingLevel
        self.board = board

    def traverse(self, stack, depth_limit, thread_num=None):
        
        # if thread_num is not None:
        #     print(f'{thread_num}: \n{stack[0]}')

        stack = list(enumerate(stack))
        
        while len(stack) > 0:

            current = stack.pop(0)

            if current[1].isSolved():
                return current[1]

            if current[0]+1 <= depth_limit:
                for branch in current[1].branches()[::-1]:
                    stack.insert(0, (current[0]+1, branch))
        return None

    def run(self, parallel=False, silent=True): 

        if not silent:
            print('running the bfs algorithm')
        if parallel:
            branches = self.board.branches()
            if not silent:
                print(f'Thread Count: {len(branches)}')

        for i in range(0, self.MAX_DEPTH):
            self.current_depth = i

            if not silent:
                print(f'Current Depth Limit: {i}')

            if parallel:
                pool = Pool()
                threads = []
                for (thread_num, branch) in enumerate(branches):
                    threads.append(pool.apply_async(self.traverse, [[branch], i, thread_num]))
                for thread in threads:
                    if thread.get() is not None:
                        thread.get().printHistory()
                        return thread.get()
            else:
                result = self.traverse([self.board], i)
                if result is not None:
                    return result


if __name__ == '__main__':

    print(f'Parallel vs. Serial Time Test')

    board = Board(presetList=[1, 2, 3, 4, 5, 0, 7, 8, 6])
    board.shuffle()

    runner = idfs(None, board)

    serialTimes = []
    parallelTimes = []
    solutionFound = []

    limit = 22

    for i in range(0, limit):

        runner.MAX_DEPTH = i

        startTime = time()
        val = runner.run(parallel=False)
        stopTime = time()
        serialTimes.append(stopTime - startTime)

        startTime = time()
        val = runner.run(parallel=True)
        stopTime = time()
        parallelTimes.append(stopTime - startTime)

        solutionFound.append(val is not None)
    
    print(f'Serial Times:')
    for time in serialTimes:
        print(f'{time}')
    print(f'Parallel Times:')
    for time in parallelTimes:
        print(f'{time}')

    print(f'\n\nWhich was better (for each max depth): ')
    for i in range(0, len(serialTimes)):
        if serialTimes[i] == parallelTimes[i]:
            print(f'{i} -- Equal -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')
        elif serialTimes[i] < parallelTimes[i]:
            print(f'{i} -- Serial -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')
        else:
            print(f'{i} -- Parallel -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')

    plt.title("Line graph")   
    plt.xlabel("Run Times")  
    plt.ylabel("Depth Limit") 
    plt.plot(range(0, limit), serialTimes, color ="red", label='Serial')  
    plt.plot(range(0, limit), parallelTimes, color ="blue", label='Parallel') 
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=2)
    plt.show()

