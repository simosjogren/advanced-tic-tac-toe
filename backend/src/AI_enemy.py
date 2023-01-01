from movement import MovementInspection
import numpy as np, pickle, sys, copy

sys.path.append('../')

class AI_enemy():
    def __init__(self, mark, model_filename):
        self.mark = mark
        with open(model_filename, 'rb') as f:
            self._model = pickle.load(f)

    def getAvailableMoves(self, board):
        availableMoves = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (board[i][j]) == 0:
                    availableMoves.append([i, j])
        return availableMoves

    def count_next_move(self, boardstate):
        boardsize = len(boardstate)
        available_moves = self.getAvailableMoves(boardstate)
        maxValue = 0
        bestMove = available_moves[0]
        for availableMove in available_moves:
            boardCopy = copy.deepcopy(boardstate)
            boardCopy[availableMove[0]][availableMove[1]] = -1
            # Number two in the below as index is temporary.
            value = self._model.predict(np.array(boardCopy).reshape(-1, np.power(boardsize, 2)))[0][2]
            print(value)
            if value > maxValue:
                maxValue = value
                bestMove = availableMove
        selectedMove = bestMove
        print("Best move: ", selectedMove)
        return selectedMove
