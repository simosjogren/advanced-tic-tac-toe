// import { draw_rectangle_table } from './tictactoe_table';

// Constants
const DEFAULT_BOARD_SIZE = 3;
const INTERVAL_SLEEPTIME_MS = 500;
const BACKEND_FOLDER = "./backend";
const BOARD_STATE_FILE = "./current_board_state.json";
const BOARD_STATE_ENCODING = 'utf8';

const fs = require('fs');
const spawner = require('child_process').spawn;

// Objects
var gameboard = {};

function checkBoardState() {
    console.log(gameboard)
    fetch('http://127.0.0.1:5000/gameboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => { gameboard = data });
};


function post_nextmove(nextMove) {
    fetch('http://127.0.0.1:5000/gameboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nextMove)
    })
        .then(response => {
            if (response.ok) {
                console.log('Success!');
            } else {
                console.log('An error occurred:', response.status);
            }
        });
};


function initialize_backend_board(board_size) {
    // Nextmove isnt actually a move, it is a initialization of the board.
    const nextMove = {
        init: { boardsize: board_size }
    };
    post_nextmove(nextMove)
};


function player_makes_move(x, y, mark) {
    const nextMove = {
        next_move: [x, y, mark]
    };
    console.log("Making a move x:", x, ", y:", y);
    post_nextmove(nextMove)
};


function draw_rectangle_table(table_size) {
    // Builds a scalable rectangle-shaped tictactoe-table as a string.
    var rows = [];
    for (let i = 1; i <= table_size; i++) {
        var slots_in_row = [];
        for (let j = 1; j <= table_size; j++) {
            slots_in_row.push('<td>Empty</td>');
        }
        rows.push('<tr>' + slots_in_row.join('') + '</tr>');
    }
    // Create a HTML element for that.
    let table = document.createElement('table');
    table.setAttribute('id', 'tictactoe_table');
    table.innerHTML = rows.join('');


    return table;
};

function initializeGame() {
    const board_size = document.getElementById("board_size_text").value;
    initialize_backend_board(board_size);
    setInterval(checkBoardState, INTERVAL_SLEEPTIME_MS);
    player_makes_move(1, 1, 'X');
    tictactoe_table_element = draw_rectangle_table(parseInt(board_size))
    document.getElementById("gameboard_zone").appendChild(tictactoe_table_element);
};


// Main moves for testing locally.
function main() {
    initialize_backend_board(DEFAULT_BOARD_SIZE);
}

main();