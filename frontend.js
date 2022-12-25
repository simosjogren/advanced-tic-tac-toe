
// Constants
const BOARD_SIZE = 3;
const INTERVAL_SLEEPTIME_MS = 10;
const BACKEND_FOLDER = "./backend";
const BOARD_STATE_FILE = "./current_board_state.json";
const BOARD_STATE_ENCODING = 'utf8';
const fs = require('fs');
const spawner = require('child_process').spawn;

// Objects
var gameboard = {};


function initialize_backend_board() {
    const board_initialization = spawner('python3', [BACKEND_FOLDER + '/initialize_board.py', BOARD_SIZE]);
    // Lets initialize the board using python.
    board_initialization.stdout.on('data', (data) => {
        console.log("Initialized board: ", JSON.parse(data.toString()));
    });
};


function checkBoardState() {
    fs.readFile(BOARD_STATE_FILE, BOARD_STATE_ENCODING, (err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        if (data !== gameboard) {
            console.log('Data has changed: ', data.toString());
            gameboard = data;
        }
    });
};


function player_makes_move(x, y, mark) {

    const register_player_move = spawner('python3', [BACKEND_FOLDER + '/register_player_move.py', x.toString(), y.toString(), mark.toString()]);
    register_player_move.stdout.on('data', (data) => {
        console.log("New databoard: ", data.toString());
    });
};


// Main moves
async function main() {
    initialize_backend_board();
    setInterval(checkBoardState, INTERVAL_SLEEPTIME_MS);
    // player_makes_move(1, 1, 'X');
}

main();