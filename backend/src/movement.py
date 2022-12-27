import json

class MovementInspection():
    def __init__(self, boardfilepath, boardstate):
        self.boardfilepath = boardfilepath
        self.boardstate = boardstate

    def inspectMoveLegality(self, X, Y, MARK):
        next_position_mark = self.boardstate[X][Y]
        if (next_position_mark == '-'):
            self.boardstate[X][Y] = MARK
            return self.boardstate
        else:
            print("Position is already taken. Current position belongs to " + next_position_mark)
            return False

    def inspectWinSituation(self):
        # TODO
        return False
    
    def saveMove(self):
        # Writes the board into .txt-file.
        with open(self.boardfilepath, 'w', encoding='utf-8') as boardobject:
            boardobject.write(json.dumps(self.boardstate))