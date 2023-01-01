from movement import MovementInspection
import numpy as np, pickle, sys, copy

sys.path.append('../')
import train_model.model

class AI_enemy():
    def __init__(self, boardfilepath, mark):
        self.mark = mark
        # self.mv = MovementInspection(self.board, boardfilepath)
        with open('./src/model.pkl', 'rb') as f:
            self._model = pickle.load(f)

    def getAvailableMoves(self, board):
        availableMoves = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (board[i][j]) == 0:
                    availableMoves.append([i, j])
        return availableMoves

    def count_next_move(self, boardstate):
        print("TILA 1: ", boardstate)
        available_moves = self.getAvailableMoves(boardstate)
        print("Available moooooves: ", available_moves)
        maxValue = 0
        bestMove = available_moves[0]
        for availableMove in available_moves:
            # get a copy of a board
            boardCopy = copy.deepcopy(np.array(boardstate, dtype=np.int8).ravel())
            print(boardCopy)
            # boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
            value = self._model.predict(boardCopy, 2)
            if value > maxValue:
                maxValue = value
                bestMove = availableMove
        selectedMove = bestMove
        print("Best mooove: ", selectedMove)
        self._model.predict(boardstate, 0)
        return selectedMove
