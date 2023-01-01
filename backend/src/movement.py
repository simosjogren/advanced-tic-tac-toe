import json, numpy as np

CURRENT_BOARD_STATE_FILEPATH = "json_api/current_board_state.json"

class MovementInspection():
    def __init__(self, boardstate, boardfilepath=CURRENT_BOARD_STATE_FILEPATH):
        self.boardfilepath = boardfilepath
        self.boardstate = np.array(boardstate, dtype=np.int8)
        self.boardsize = len(boardstate)

    def inspectMoveLegality(self, X, Y, MARK):
        next_position_mark = self.boardstate[X][Y]
        if (next_position_mark == 0):
            self.boardstate[X][Y] = np.int8(MARK)
            return self.boardstate.tolist()
        else:
            print("Position is already taken. Current position belongs to " + str(next_position_mark))
            return False
            
    def saveMove(self):
        # Writes the board into .txt-file.
        with open(self.boardfilepath, 'w', encoding='utf-8') as boardobject:
            boardobject.write(json.dumps(self.boardstate.tolist()))

    def inspectWinSituation(self):
        '''
        This function requires a numpy conversion and its done in the beginning and
        in the end of this function.
        '''
        # Horisontal & Vertical inspection
        abs_boardsize = abs(self.boardsize)
        for idx in range(self.boardsize):
            if (sum(self.boardstate[idx,:]) == abs_boardsize):
                return [True, self.boardstate[idx,0]]
            elif (sum(self.boardstate[:,idx]) == abs_boardsize):
                return [True, self.boardstate[0,idx]]
        # Diagonal inspection 1
        diagonal_vector = np.diagonal(self.boardstate) * np.ones(self.boardsize, dtype=np.int8).T
        if (diagonal_vector.sum() == abs_boardsize):
            return [True, self.boardstate[0,0]]
        # Flip the array 90 degrees, and then diagonal inspection 2
        diagonal_vector = np.diagonal(np.rot90(self.boardstate))
        if (diagonal_vector.sum() == abs_boardsize):
            return [True, self.boardstate[self.boardsize-1,0]]
        return [False]