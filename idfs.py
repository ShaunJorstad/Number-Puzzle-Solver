from multiprocessing import Pool
import numpy as np
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
                        threads.append(pool.apply_async(
                            self.traverse, [[branch], i, thread_num]))
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
                        threads.append(pool.apply_async(self.greedy_traverse, [
                                       [branch], [self.board], i, thread_num]))
                    for thread in threads:
                        if thread.get() is not None:
                            thread.get().printHistory()
                            return thread.get()
                else:
                    result = self.greedy_traverse(
                        [self.board], [self.board], i)
                    if result is not None:
                        return result
