from bfs import bfs
from ass import ass

algorithms = {
    '': ('bfs and A*', [bfs, ass]),
    'bfs': ('only bfs', [bfs]),
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


if __name__ == '__main__':
    alg = promptAlgorithm()
    loggingLevel = promptLoggingLevel()
    # prompt user to select whether a collection of prechosen boards will be used to test the algorithm on, or if they would like to construct their own custom board. it's possible that not invalid board configurations exist
    print(
        f'\nRunning {algorithms[alg][0]} at {loggingLevels[loggingLevel]} logging')
    for algorithm in algorithms[alg][1]:
        solver = algorithm(loggingLevel)
        solver.run()
