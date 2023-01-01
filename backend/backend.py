from flask import Flask, request, jsonify
import json, sys
from flask_cors import CORS

from src.toolbox import Toolbox
from src.exceptions import BoardInitError

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
    tb = Toolbox( {"init": {}, "next_move": [] }, CURRENT_BOARD_STATE_FILEPATH)
    gameboard = tb.load_gameboard()
    return jsonify(gameboard), 200

@app.route("/post-gameboard", methods=['POST'])
def post_gameboard_state():
    gameboard_json = request.get_json()
    try:
        print(gameboard_json)
        tb = Toolbox(gameboard_json, CURRENT_BOARD_STATE_FILEPATH)
        if (tb.gb_init != {}):
            game_state = tb.initialize_board()
            print("Game state after initialization: ", game_state)
            return json.dumps(game_state), 200
        elif (tb.gb_next_move != []):
            loaded_board = tb.load_gameboard()
            game_state = tb.make_player_move()
            print("Game state BEFORE AI turn: ", game_state)
            tb.initAI(len(loaded_board))
            game_state = tb.make_AI_move(game_state["boardstate"])
            print("Game state AFTER AI turn: ", game_state)
            return json.dumps(game_state), 200
        
    except KeyError:
        return {}, 500
        


if __name__=="__main__":
    app.run(debug=True)