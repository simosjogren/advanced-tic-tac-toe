import sys
import json

'''
Calling syntax: python3 backend/register_player_move.py <x> <y> <marking>
For example: python3 backend/register_player_move.py 1 1 'X'
'''

BOARD_STATE_FILE = "./current_board_state.json"

X = int(sys.argv[1])
Y = int(sys.argv[2])
MARK = str(sys.argv[3])


def load_gameboard():
    with open(BOARD_STATE_FILE, 'r', encoding='utf-8') as boardobject:
        current_board = json.load(boardobject)
    return current_board


def save_gameboard(current_board):
    # Writes the board into .txt-file.
    with open(BOARD_STATE_FILE, 'w', encoding='utf-8') as boardobject:
        boardobject.write(json.dumps(current_board))


def main():

    # Lets load the current board.
    current_board = load_gameboard()

    # Checks if the move x and y hit inside the assigned board.
    # TODO

    # Make the move
    next_position_mark = current_board[X][Y]
    if (next_position_mark == '-'):
        current_board[X][Y] = MARK
        print(current_board)
        save_gameboard(current_board)
    else:
        print("Position is already taken. Current position belongs to " + next_position_mark)

main()
sys.stdout.flush()