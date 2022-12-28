from movement import MovementInspection
import random, numpy

class AI_enemy():
    def __init__(self, board, boardfilepath, mark):
        self.board = board
        self.mark = mark
        self.mv = MovementInspection(self.board, boardfilepath)

    def count_next_move():
        return []