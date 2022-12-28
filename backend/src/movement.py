import json, numpy as np

class MovementInspection():
    def __init__(self, boardfilepath, boardstate):
        self.boardfilepath = boardfilepath
        self.boardstate = boardstate
        self.boardsize = len(boardstate)
        self.convertToNumpy()
        self.convertFromNumpy()

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
        # Horisontal inspection
        for y in self.boardstate:
            if ('-' in y):
                break
            elif (all(item == y[0] for item in y)):
                return [True, y[0]]
        # Vertical inspection
        for y in range(self.boardsize):
            y_count = 0
            for x in range(self.boardsize):
                mark = self.boardstate[y][x]
                if (mark == '-'):
                    break
                elif (mark != self.boardstate[y][0]):
                    break
                y_count += 1
            if (y_count == self.boardsize):
                return [True, mark]
        # Diagonal inspection 1
        counter_leftup_rightdown = 0
        for idx in range(self.boardsize):
            leftup_rightdown_mark = self.boardstate[idx][idx]
            if (leftup_rightdown_mark == '-'):
                break
            if (leftup_rightdown_mark != self.boardstate[0][0]):
                break
            counter_leftup_rightdown += 1
        if (counter_leftup_rightdown == self.boardsize):
            return [True, leftup_rightdown_mark]
        # Diagonal inspection 2
        counter_rightup_leftdown = 0
        for idx in range(self.boardsize):
            rightup_leftdown_mark = self.boardstate[self.boardsize-1-idx][idx]
            if (rightup_leftdown_mark == '-'):
                break
            if (rightup_leftdown_mark != self.boardstate[self.boardsize-1][0]):
                break
            counter_rightup_leftdown += 1
        if (counter_rightup_leftdown == self.boardsize):
            return [True, rightup_leftdown_mark]
        # Did not find any winning combinations. Continuing...
        return [False]