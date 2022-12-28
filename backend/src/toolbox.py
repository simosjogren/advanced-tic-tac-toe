import sys, json

sys.path.append("./src")
from movement import MovementInspection
from AI_enemy import AI_enemy

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
            mv = MovementInspection(boardstatefile, empty_board)
            mv.saveMove()
            return True
        except ValueError:
            print("Invalid board size.")
            return False
    
    def make_player_move(self, next_move, boardstate_filepath):
        X = next_move[0]
        Y = next_move[1]
        MARK = next_move[2]
        boardstate = self.load_gameboard(boardstate_filepath, return_string=False)
        mv = MovementInspection(boardstate_filepath, boardstate)
        mv.inspectMoveLegality(X, Y, MARK)
        mv.saveMove()
        win_situation = [False, ""]
        if (win_situation[0]):
            print("Player " + win_situation[1] + " won!")
            return True
        else:
            return False

    def make_AI_move(self, boardstate_filepath):
        boardstate = self.load_gameboard(boardstate_filepath, return_string=False)
        # enemy = AI_enemy(boardstate, boardstate_filepath, mark)       
    
    def load_gameboard(self, boardstate_filepath, return_string=True):
        with open(boardstate_filepath, 'r', encoding='utf-8') as boardobject:
            current_board = json.load(boardobject)
            if return_string:
                return json.dumps(current_board)
            else:
                return current_board