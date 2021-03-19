from idfs import idfs
from aStar import aStar
from board import Board
import os

algorithms = {
    '': ('idfs and A*', [idfs, aStar], [False, False]),
    'idfs': ('only bfs', [idfs], [False, False]),
    'aStar': ('only a*', [aStar], [False, False]),
    'idfs-greedy': ('idfs serial greedy', [idfs], [False, True]),
    'idfs-parallel': ('idfs parallel', [idfs], [True, False]),
    'idfs-parallel-greedy': ('idfs parallel greedy', [idfs], [True, True])
}

loggingLevels = {
    '': 'silent',
    'v': 'verbose'
}

heuristicLevels = {
    '': 'no heuristic',
    '0': 'Bad heuristic: num of correctly positioned tiles',
    '1': 'Good heuristic: Manhatten distance'
}


def prompt(validInput, promptTitle, default):
    '''
    prompts the user based on the provided options repeatedly until a valid value is selected, and then returned
    '''
    userInput = 'null'
    while userInput not in validInput.keys():
        print(f'{promptTitle}')
        print(f'Select (default={default}): [', end='')
        for (key, value) in validInput.items():
            print(f'{key} ', end='')
        print(']')
        userInput = input(': ')
    return userInput


def promptAlgorithm():
    ''' prompts the user for the algorithm to run'''
    os.system('cls' if os.name == 'nt' else 'clear')
    return prompt(algorithms, 'Select which algorithm to run', 'all')


def promptLoggingLevel():
    ''' prompts the user for the logging level to use'''
    os.system('cls' if os.name == 'nt' else 'clear')
    return prompt(loggingLevels, 'Select logging level', 'silent')


def promptHeuristicLevel():
    '''prompts for heurstic to use'''
    os.system('cls' if os.name == 'nt' else 'clear')
    print('0: (bad) number of correctly positioned tiles')
    print('1: (good) manhatten distance')
    result = prompt(heuristicLevels, 'Select heuristic', 'none')
    if result == '':
        return None
    return int(result)


def useCustomBoard():
    ''' prompts the user if they want provide a custom board to solve or not'''
    os.system('cls' if os.name == 'nt' else 'clear')
    return '' != prompt({'yes': 'y', '': 'no'}, f'Solve custom board\n(main algorithm analytics are not run on custom boards)', 'no')


if __name__ == '__main__':
    boardSize = 9
    alg = promptAlgorithm()
    loggingLevel = promptLoggingLevel()
    customBoard = useCustomBoard()
    heuristicLevel = promptHeuristicLevel()
    board = None
    if customBoard:
        board = Board(boardSize)
        board.customBuild()
    else:
        # reference a list of predefined boards
        board = Board(boardSize, heuristic=heuristicLevel)
        board.shuffleValid()
    print(
        f'\nRunning {algorithms[alg][0]} at {loggingLevels[loggingLevel]} logging')
    for algorithm in algorithms[alg][1]:
        solver = algorithm(loggingLevel, board)
        result = solver.run(
            parallel=algorithms[alg][2][0], greedy=algorithms[alg][2][1])
        print(result)
        # run should return the final board so that we can print the history here
