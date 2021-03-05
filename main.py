from idfs import idfs
from ass import ass
from board import Board

algorithms = {
    '': ('idfs and A*', [idfs, ass]),
    'idfs': ('only bfs', [idfs]),
    'a': ('only a*', [ass])
}

loggingLevels = {
    '': 'silent',
    'v': 'verbose'
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
    return prompt(algorithms, 'Select which algorithm to run', 'all')


def promptLoggingLevel():
    ''' prompts the user for the logging level to use'''
    return prompt(loggingLevels, 'Select logging level', 'silent')


def useCustomBoard():
    ''' prompts the user if they want provide a custom board to solve or not'''
    return '' != prompt({'yes': 'y', '': 'no'}, f'Solve custom board\n(main algorithm analytics are not run on custom boards)', 'no')


if __name__ == '__main__':
    alg = promptAlgorithm()
    loggingLevel = promptLoggingLevel()
    customBoard = useCustomBoard()
    board = None
    if customBoard:
        print('todo: prompt user through creating custom board')
    print(
        f'\nRunning {algorithms[alg][0]} at {loggingLevels[loggingLevel]} logging')
    for algorithm in algorithms[alg][1]:
        solver = algorithm(loggingLevel, board)
        solver.run()

    test = Board(9)
    test[8] = 400
    test.swap(3, 4)
    print(test)
