import sys
import json

'''
Calling syntax: python3 backend/initialize_board.py <board-size>
For example: python3 backend/initialize_board.py 3
'''

BOARD_STATE_FILE = "/current_board_state.json"

def main():
    # Checks the validity of the gameboard size.
    try:
        BOARD_SIZE = int(sys.argv[1])

        # Creates the actual BOARD_SIZE x BOARD_SIZE -scaled board.
        empty_board = []
        for i in range(BOARD_SIZE):
            x_row = []
            for j in range(BOARD_SIZE):
                x_row.append('-')
            empty_board.append(x_row)

        # Returns the board to javascript.
        empty_board_string = json.dumps(empty_board)
        print(empty_board_string)

        # Writes the board into .txt-file.
        with open('.' + BOARD_STATE_FILE, 'w') as boardobject:
            boardobject.write(empty_board_string)
    except ValueError:
        print("Invalid board size.")

main()
sys.stdout.flush()