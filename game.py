import numpy as np

def print_field(board):
    print(board)

def evaluate_game(board):
    for player in ['X', 'O']:
        if any(np.all(board == player, axis=0)) or any(np.all(board == player, axis=1)) or np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
            return player
    if np.all(board != ''):
        return 'Draw'
    return ''

def get_player_input(turn):
    while True:
        try:
            if turn == 'X':
                choice = input(f"{turn}'s turn\nEnter the coordinates (row column): ").split()
                row, column = map(int, choice)
                if 1 <= row <= 3 and 1 <= column <= 3 and board[row-1, column-1] == '':
                    return row - 1, column - 1
                else:
                    print('Invalid input! Please enter unoccupied coordinates from 1 to 3.')
            else:
                row, column = np.random.randint(0, 3, size=2)
                if board[row, column] == '':
                    print(f"Computer chose: {row + 1} {column + 1}")
                    return row, column
        except (ValueError, IndexError):
            print('Invalid input! Please enter valid coordinates.')

def tictactoe():
    global board
    board = np.full((3, 3), '', dtype=str)
    for x in board:
        print(x)
    print("Matrix format = (row, column)")
    turn = 'X'
    for _ in range(9):
        row, column = get_player_input(turn)
        board[row, column] = turn
        for x in board:
            print(x)
        result = evaluate_game(board)
        if result:
            if result == 'Draw':
                print('Draw')
                print('#'*20)
            else:
                print(f'{result} wins')
                print('#'*20)
            break
        turn = 'O' if turn == 'X' else 'X'

