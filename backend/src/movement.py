import json, numpy as np

class MovementInspection():
    def __init__(self, boardfilepath, boardstate):
        self.boardfilepath = boardfilepath
        self.boardstate = boardstate
        self.boardsize = len(boardstate)

    def convertToNumpy(self):
        # 'X' = 1, 'O' = -1, '-' = 0.
        numpy_array = np.empty((self.boardsize, self.boardsize), dtype=np.int8)
        for y in range(self.boardsize):
            row_array = np.zeros(len(self.boardstate), dtype=np.int8)
            for x in range(self.boardsize):
                if (self.boardstate[y][x] == 'X'):
                    row_array[x] = np.int8(1)
                elif (self.boardstate[y][x] == 'O'):
                    row_array[x] = np.int8(-1)
            numpy_array[y] = row_array
        self.boardstate = numpy_array
    
    def convertFromNumpy(self):
        string_array = []
        for y in range(self.boardsize):
            row_array = []
            for x in range(self.boardsize):
                if (self.boardstate[y][x] == 1):
                    row_array.append("X")
                elif (self.boardstate[y][x] == -1):
                    row_array.append("O")
                elif (self.boardstate[y][x] == 0):
                    row_array.append("-")
            string_array.append(row_array)
        self.boardstate = string_array

    def inspectMoveLegality(self, X, Y, MARK):
        next_position_mark = self.boardstate[X][Y]
        if (next_position_mark == '-'):
            self.boardstate[X][Y] = MARK
            return self.boardstate
        else:
            print("Position is already taken. Current position belongs to " + next_position_mark)
            return False
            
    def saveMove(self):
        # Writes the board into .txt-file.
        with open(self.boardfilepath, 'w', encoding='utf-8') as boardobject:
            boardobject.write(json.dumps(self.boardstate))

    def inspectWinSituation(self):
        '''
        This function requires a numpy conversion and its done in the beginning and
        in the end of this function.
        '''
        self.convertToNumpy()
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
        self.convertFromNumpy()
        return [False]