from board import Board
from idfs import idfs
from time import time
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
from random import *

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
                print(
                    f'{i} -- Equal -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')
            elif serialTimes[i] < parallelTimes[i]:
                print(
                    f'{i} -- Serial -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')
            else:
                print(
                    f'{i} -- Parallel -- {"Solution Found" if solutionFound[i] else "Solution Not Found"}')

        plt.title("Line graph")
        plt.xlabel("Run Times")
        plt.ylabel("Depth Limit")
        plt.plot(range(0, limit), serialTimes, color="red", label='Serial')
        plt.plot(range(0, limit), parallelTimes,
                 color="blue", label='Parallel')
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.00), shadow=True, ncol=2)
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
        plt.plot(range(0, limit+1), serialgreedy,
                 color="blue", label='Serial greedy')
        # plt.plot(range(0, limit+1), parallelNotgreedy, color ="orange", label='Parallel Not greedy')
        plt.plot(range(0, limit+1), parallelgreedy,
                 color="purple", label='Parallel greedy')
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.00), shadow=True, ncol=2)
        plt.show()

    # test_all(25)

    did_work = 0
    for i in range(0, 1000):

        if i % 10 == 0:
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
