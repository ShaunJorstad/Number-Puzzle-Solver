
from board import Board
from multiprocessing import Pool
from time import time
import numpy as np  
import matplotlib.pyplot as plt 
from random import *

class idfs:
    '''Class that solves via brute force bfs'''

    MAX_DEPTH = 25

    def __init__(self, loggingLevel, board, max_depth=None):
        self.loggingLevel = loggingLevel
        self.board = board
        if max_depth is not None:
            self.MAX_DEPTH = max_depth

    def greedy_traverse(self, stack, viewed, depth_limit, thread_num=None):
        
        # if thread_num is not None:
                #     print(f'{thread_num}: \n{stack[0]}')

        stack = list(enumerate(stack))

        while len(stack) > 0:
            
            current = stack.pop(0)

            if current[1].isSolved():
                return current[1]

            if current[0]+1 <= depth_limit:
                for branch in current[1].branches()[::-1]:
                    if branch not in viewed:
                        stack.insert(0, (current[0]+1, branch))
                        viewed.append(branch)
        return None


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

    def run(self, parallel=False, silent=False, greedy=False): 

        if not silent:
            print('running the idfs algorithm')
        if parallel:
            branches = self.board.branches()
            if not silent:
                print(f'Thread Count: {len(branches)}')

        for i in range(0, self.MAX_DEPTH):
            self.current_depth = i

            if not greedy:
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
            else:
                if parallel:
                    pool = Pool()
                    threads = []
                    for (thread_num, branch) in enumerate(branches):
                        threads.append(pool.apply_async(self.greedy_traverse, [[branch], [self.board], i, thread_num]))
                    for thread in threads:
                        if thread.get() is not None:
                            thread.get().printHistory()
                            return thread.get()
                else:
                    result = self.greedy_traverse([self.board], [self.board], i)
                    if result is not None:
                        return result


if __name__ == '__main__':

    def parallel_vs_serial(limit):
        print(f'Parallel vs. Serial Time Test')

        board = Board(presetList=[1, 2, 3, 4, 5, 0, 7, 8, 6])
        board.shuffle()

        runner = idfs(None, board)

        serialTimes = []
        parallelTimes = []
        solutionFound = []

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
    
    def test_all(limit):
        board = Board(presetList=[1, 2, 3, 4, 5, 6, 8, 7, 0])

        serialNotgreedy = []
        serialgreedy = []
        parallelNotgreedy = []
        parallelgreedy = []

        for i in range(0, limit+1):

            print(f'Begin depth: {i}')
            runner = idfs(None, board, max_depth=i)

            # startTime = time()
            # runner.run()
            # stopTime = time()
            # serialNotgreedy.append(stopTime-startTime)

            startTime = time()
            runner.run(greedy=True)
            stopTime = time()
            serialgreedy.append(stopTime-startTime)

            # startTime = time()
            # runner.run(parallel=True, greedy=False)
            # stopTime = time()
            # parallelNotgreedy.append(stopTime-startTime)

            startTime = time()
            runner.run(parallel=True, greedy=True)
            stopTime = time()
            parallelgreedy.append(stopTime-startTime)

        plt.title("Line graph")   
        plt.xlabel("Depth Limit")  
        plt.ylabel("Run Times") 
        # plt.plot(range(0, limit+1), serialNotgreedy, color ="red", label='Serial Not greedy')  
        plt.plot(range(0, limit+1), serialgreedy, color ="blue", label='Serial greedy')  
        # plt.plot(range(0, limit+1), parallelNotgreedy, color ="orange", label='Parallel Not greedy') 
        plt.plot(range(0, limit+1), parallelgreedy, color ="purple", label='Parallel greedy') 
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=2)
        plt.show()

    # test_all(25)

    did_work = 0
    for i in range(0, 1000):

        if i%10 == 0:
            print(f'{i}')

        solved_board = Board(presetList=[1, 2, 3, 4, 5, 6, 7, 8, 0])
        board = solved_board.branches()[0]
        depth = 15

        for _ in range(0, depth-1):
            
            branches = board.branches()
            board = branches[randint(0, len(branches)-1)]
            while board == solved_board:
                board = branches[randint(0, len(branches)-1)]

        # print(board)
        runner = idfs(None, board, depth+1)
        if runner.run(greedy=True, silent=True) is not None:
            did_work += 1
        # print(runner.run(greedy=True))
    print(f'{did_work}/1000 Worked: {(did_work/1000)*100}%')
