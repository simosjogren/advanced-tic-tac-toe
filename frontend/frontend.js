// Constants
const DEFAULT_BOARD_SIZE = 3;
const INTERVAL_SLEEPTIME_MS = 500;
const BACKEND_FOLDER = "./backend";
const BOARD_STATE_FILE = "./current_board_state.json";
const BOARD_STATE_ENCODING = 'utf8';

// Objects
let gameData = {
    gameboard: [],
    board_size: null,
    player_mark: 'X'
}

const fs = require('fs');
const spawner = require('child_process').spawn;


// onClick when pressed the start game button.
function initializeGame() {
    document.getElementById("start_game_button").disabled = true;
    gameData.board_size = document.getElementById("board_size_text").value;
    initialize_backend_board();
    // setInterval(checkBoardState, INTERVAL_SLEEPTIME_MS);
    // player_makes_move(1, 2, 'X');
};



function checkBoardState() {
    console.log(gameData.gameboard)
    fetch('http://127.0.0.1:5000/get-gameboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => {
            gameData.gameboard = data;
        });
};


function post_nextmove(nextMove, init_run = false) {
    fetch('http://127.0.0.1:5000/post-gameboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nextMove)
    })
        .then(response => response.json())
        .then(data => {
            if (init_run == false) {
                document.getElementById("tictactoe_table").remove();
            }
            gamemobard_zone = document.getElementById("gameboard_zone");
            console.log(data)
            gameData.gameboard = data;
            tictactoe_table_element = draw_rectangle_table()
            gameboard_zone.appendChild(tictactoe_table_element);
        });
};


function initialize_backend_board() {
    // Nextmove isnt actually a move, it is a initialization of the board.
    const nextMove = {
        init: { boardsize: gameData.board_size }
    };
    post_nextmove(nextMove, true)
};


function player_makes_move(x, y, mark) {
    const nextMove = {
        next_move: [x, y, mark]
    };
    console.log("Making a move x:", x, ", y:", y);
    post_nextmove(nextMove)
};


function get_onClickevent_link(x, y, marking) {
    // Returns a onClick event link for given image.
    // If the mark is NOT null, then we dont give a link to the mark.
    if (marking !== '-') {
        return " onClick=\"player_makes_move(" + x.toString() +
            ", " + y.toString() + ", \'" + marking + "\')\"";
    }
}


function get_marking_graphics(x, y) {
    marking = gameData.gameboard[x][y]
    if (marking === '-') {
        return "<img src=\"./images/empty_mark.jpg\" " + get_onClickevent_link(x, y, gameData.player_mark) + ">";
    } else if (marking === 'X') {
        return "<img src=\"./images/x_mark.jpg\" " + get_onClickevent_link(x, y, gameData.player_mark) + ">";
    } else if (marking === 'O') {
        return "<img src=\"./images/o_mark.jpg\" " + get_onClickevent_link(x, y, gameData.player_mark) + ">";
    }
};


function draw_rectangle_table() {
    // Builds a scalable rectangle-shaped tictactoe-table as a string.
    var rows = [];
    table_size = gameData.board_size;
    for (let y = 1; y <= table_size; y++) {
        var slots_in_row = [];
        for (let x = 1; x <= table_size; x++) {
            slots_in_row.push('<td>' + get_marking_graphics(x - 1, y - 1) + '</td>');
        }
        rows.push('<tr>' + slots_in_row.join('') + '</tr>');
    }
    // Create a HTML element for that.
    let table = document.createElement('table');
    table.setAttribute('id', 'tictactoe_table');
    table.innerHTML = rows.join('');

    return table;
};


// Main moves for testing locally.
function main() {
    initialize_backend_board(DEFAULT_BOARD_SIZE);
}

main();