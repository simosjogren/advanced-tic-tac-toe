import sys, json, numpy as np, os

sys.path.append("./src")
from movement import MovementInspection
from AI_enemy import AI_enemy

sys.path.append("../..")

class Toolbox():
    def __init__(self, gameboard, board_filepath):
        # This try is mainly only for the get-method.
        try:
            self.gb_init = gameboard["init"]
            self.gb_next_move = gameboard["next_move"]
        except:
            print("Toolbox initialization failed.")
        self.board_filepath = board_filepath
        self.boardstate = []

    def initialize_board(self):
        boardsize = self.gb_init["boardsize"]
        print("Initializing board with size: ", str(boardsize))
        try:
            # Creates the actual BOARD_SIZE x BOARD_SIZE -scaled board.
            empty_board = []
            boardsize = int(boardsize)
            for i in range(boardsize):
                x_row = []
                for j in range(boardsize):
                    x_row.append(0)
                empty_board.append(x_row)
            # Writes the board into .txt-file.
            self.boardstate = empty_board
            mv = MovementInspection(self.boardstate, self.board_filepath)
            mv.saveMove()
        except ValueError:
            print("Invalid board size.")
            empty_board = []
        return {"game_ended": False, "boardstate": self.boardstate, "winner": ""}
    
    def make_player_move(self):
        X = self.gb_next_move[0]
        Y = self.gb_next_move[1]
        MARK = self.gb_next_move[2]
        mv = MovementInspection(self.boardstate, self.board_filepath)
        self.boardstate = mv.inspectMoveLegality(X, Y, MARK)
        mv.saveMove()
        win_situation = mv.inspectWinSituation()
        if (win_situation[0]):
            game_ended = True
            winner = str(win_situation[1])
            print("Player " + winner + " won!")
        else:
            winner = ""
            game_ended = False
        return {"game_ended": game_ended, "boardstate": self.boardstate, "winner": winner}
    
    def initAI(self, size):
        boardsize_string = str(size)
        filename_string = "./trained_models/model_" + boardsize_string + "x" + boardsize_string + ".pkl"
        self.AI = AI_enemy('O', filename_string)

    def make_AI_move(self, board):
        next_move = self.AI.count_next_move(board)
        mv = MovementInspection(board, self.board_filepath)
        boardstate = mv.inspectMoveLegality(next_move[0], next_move[1], -1)
        mv.saveMove()
        win_situation = mv.inspectWinSituation()
        if (win_situation[0]):
            game_ended = True
            winner = str(win_situation[1])
            print("Player " + winner + " won!")
        else:
            winner = ""
            game_ended = False
        return {"game_ended": game_ended, "boardstate": boardstate, "winner": winner}
    
    def load_gameboard(self, return_string=False):
        parentfolders = os.path.split(self.board_filepath)[0]
        if (not os.path.exists(parentfolders)):
            print(parentfolders, " did not exist. Creating...")
            os.makedirs(parentfolders)

        with open(self.board_filepath, 'r', encoding='utf-8') as boardobject:
            current_board = json.load(boardobject)
            if return_string:
                return json.dumps(current_board)
            else:
                self.boardstate = current_board
                return self.boardstate