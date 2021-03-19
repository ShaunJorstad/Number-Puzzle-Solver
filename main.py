from board import Board
import os


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


def useCustomBoard():
    ''' prompts the user if they want provide a custom board to solve or not'''
    os.system('cls' if os.name == 'nt' else 'clear')
    return '' != prompt({'yes': 'y', '': 'no'}, f'Solve custom board\n(main algorithm analytics are not run on custom boards)', 'no')


if __name__ == '__main__':
    boardSize = 9
    board = Board(heuristic=1)
    board.shuffleValid()
    if useCustomBoard():
        board.customBuild()
    board.playGame()
