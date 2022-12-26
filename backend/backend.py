from flask import Flask, request
import json, sys
from flask_cors import CORS

sys.path.append(".src/")
from src.toolbox import Toolbox
tb = Toolbox()

CURRENT_BOARD_STATE_FILEPATH = "json_api/current_board_state.json"
print("Test-server")

app = Flask(__name__)
CORS(app)

@app.route("/gameboard", methods=['POST', 'GET'])
def get_gameboard_state():
    if (request.method == 'GET'):
        return tb.load_gameboard(CURRENT_BOARD_STATE_FILEPATH)
    elif (request.method == 'POST'):
        gameboard_json = request.get_json()
        try:
            init_parameters = gameboard_json["init"]
            init_status = tb.initialize_board(init_parameters["boardsize"], CURRENT_BOARD_STATE_FILEPATH)
            if init_status:
                return "Board state saved succesfully", 200
            else:
                return "Board state saved unsuccessfully", 500
        except:
            print("Making a move: ", gameboard_json["next_move"])
            tb.make_player_move(gameboard_json["next_move"], CURRENT_BOARD_STATE_FILEPATH)

            # TODO: Function call for the AI to make a move.
            return "Board state saved successfully", 200

if __name__=="__main__":
    app.run(debug=True)