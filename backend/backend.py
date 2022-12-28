from flask import Flask, request, jsonify
import json, sys
from flask_cors import CORS

from src.toolbox import Toolbox
tb = Toolbox()

CURRENT_BOARD_STATE_FILEPATH = "json_api/current_board_state.json"

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/get-gameboard", methods=['GET'])
def get_gameboard_state():
    gameboard = tb.load_gameboard(CURRENT_BOARD_STATE_FILEPATH)
    return jsonify(gameboard), 200

@app.route("/post-gameboard", methods=['POST'])
def post_gameboard_state():
    gameboard_json = request.get_json()
    try:
        init_parameters = gameboard_json["init"]
        init_status = tb.initialize_board(init_parameters["boardsize"], CURRENT_BOARD_STATE_FILEPATH)
        if init_status:
            return tb.load_gameboard(CURRENT_BOARD_STATE_FILEPATH), 200
        else:
            return "Board state saved unsuccessfully", 500
    except:
        print("Making a move: ", gameboard_json["next_move"])
        # TODO Make Toolbox a object
        game_ended = tb.make_player_move(gameboard_json["next_move"], CURRENT_BOARD_STATE_FILEPATH)
        # TODO Send win information to frontend.
        game_ended = tb.make_AI_move(CURRENT_BOARD_STATE_FILEPATH)

        return tb.load_gameboard(CURRENT_BOARD_STATE_FILEPATH), 200

if __name__=="__main__":
    app.run(debug=True)