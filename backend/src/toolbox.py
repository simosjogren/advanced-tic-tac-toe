import sys, json, numpy as np

sys.path.append("./src")
from movement import MovementInspection
from AI_enemy import AI_enemy

sys.path.append("../..")

CURRENT_BOARD_STATE_FILEPATH = "json_api/current_board_state.json"

class Toolbox():
    def __init__(self, gameboard, board_filepath=CURRENT_BOARD_STATE_FILEPATH):
        # This try is mainly only for the get-method.
        try:
            self.gb_init = gameboard["init"]
            self.gb_next_move = gameboard["next_move"]
        except:
            print("Toolbox initialization failed.")
        self.board_filepath = board_filepath
        self.AI = AI_enemy(self.board_filepath, 'O')
        pass

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
            mv = MovementInspection(empty_board, self.board_filepath)
            mv.saveMove()
        except ValueError:
            print("Invalid board size.")
            empty_board = []
        print({"game_ended": False, "boardstate": empty_board, "winner": ""})
        return {"game_ended": False, "boardstate": empty_board, "winner": ""}
    
    def make_player_move(self):
        X = self.gb_next_move[0]
        Y = self.gb_next_move[1]
        MARK = self.gb_next_move[2]
        boardstate = self.load_gameboard(self.board_filepath)
        mv = MovementInspection(boardstate, self.board_filepath)
        boardstate = mv.inspectMoveLegality(X, Y, MARK)
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

    def make_AI_move(self, board, boardstate_filepath=CURRENT_BOARD_STATE_FILEPATH):
        # boardstate = self.load_gameboard(boardstate_filepath)
        # enemy = AI_enemy(boardstate, boardstate_filepath, mark)
        next_move = self.AI.count_next_move(board)
        pass

    
    def load_gameboard(self, boardstate_filepath, return_string=False):
        with open(boardstate_filepath, 'r', encoding='utf-8') as boardobject:
            current_board = json.load(boardobject)
            if return_string:
                return json.dumps(current_board)
            else:
                return current_board