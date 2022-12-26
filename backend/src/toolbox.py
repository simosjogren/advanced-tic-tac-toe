import sys, json

sys.path.append("../..")

class Toolbox():
    def __init__(self):
        pass

    def initialize_board(self, boardsize, boardstatefile):
        # Checks the validity of the gameboard size.
        try:
            # Creates the actual BOARD_SIZE x BOARD_SIZE -scaled board.
            empty_board = []
            boardsize = int(boardsize)
            for i in range(boardsize):
                x_row = []
                for j in range(boardsize):
                    x_row.append('-')
                empty_board.append(x_row)
            # Writes the board into .txt-file.
            with open(boardstatefile, 'w') as boardobject:
                boardobject.write(json.dumps(empty_board))
                return True
        except ValueError:
            print("Invalid board size.")
            return False
    
    def make_player_move(self, next_move, boardstate_filepath):
        # TODO: FIX the functionality.
        # try:
        X = next_move[0]
        Y = next_move[1]
        MARK = next_move[2]
        boardstate = self.load_gameboard(boardstate_filepath, return_string=False)
        next_position_mark = boardstate[X][Y]
        if (next_position_mark == '-'):
            boardstate[X][Y] = MARK
            print(boardstate[X][Y])
            self.save_gameboard(boardstate, boardstate_filepath)
            return True
        else:
            print("Position is already taken. Current position belongs to " + next_position_mark)
            return False
        # except:
        #     return False
    
    def load_gameboard(self, boardstate_filepath, return_string=True):
        with open(boardstate_filepath, 'r', encoding='utf-8') as boardobject:
            current_board = json.load(boardobject)
            if return_string:
                return json.dumps(current_board)
            else:
                return current_board

    def save_gameboard(self, boardstate, boardstatefilepath):
        # Writes the board into .txt-file.
        with open(boardstatefilepath, 'w', encoding='utf-8') as boardobject:
            boardobject.write(json.dumps(boardstate))