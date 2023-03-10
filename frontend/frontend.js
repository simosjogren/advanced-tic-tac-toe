// Constants
const DEFAULT_BOARD_SIZE = 3;
const INTERVAL_SLEEPTIME_MS = 500;
const BACKEND_FOLDER = "./backend";
const BOARD_STATE_FILE = "./current_board_state.json";
const BOARD_STATE_ENCODING = 'utf8';

// Objects
const stringTranslations = Object.assign({}, { '1': 'X', '0': '-', '-1': 'O' });
const gameData = {
    gameboard: [],
    board_size: null,
    player_mark: '1'
}

const fs = require('fs');
const spawner = require('child_process').spawn;


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


function gameOver(winner) {
    winner_string = stringTranslations[winner];
    document.getElementById("start_game_button").disabled = false;
    const winner_text = "Game Over. Winner is: " + stringTranslations[winner];
    console.log(winner_text);
    winner_zone = document.getElementById("winner_zone");
    winner_zone.innerHTML = winner_text;
}


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
            gameboard_zone = document.getElementById("gameboard_zone");
            console.log(data)
            gameData.gameboard = data["boardstate"];
            tictactoe_table_element = draw_rectangle_table()
            gameboard_zone.appendChild(tictactoe_table_element);
            if (data["game_ended"] == true) {
                gameOver(data["winner"])
            }
        });
};


// onClick when pressed the start game button.
function initializeGame() {
    // First reset the div.
    document.getElementById("gameboard_zone").innerHTML = '';
    document.getElementById("winner_zone").innerHTML = '';
    document.getElementById("start_game_button").disabled = true;
    // Lets catch the desired board size.
    gameData.board_size = document.getElementById("board_size_text").value;
    initialize_backend_board();
};


function initialize_backend_board() {
    // Nextmove isnt actually a move, it is a initialization of the board.
    const nextMove = {
        init: { boardsize: gameData.board_size },
        next_move: []
    };
    post_nextmove(nextMove, true)
};


function player_makes_move(x, y, mark) {
    const nextMove = {
        init: {},
        next_move: [x, y, mark]
    };
    console.log("Making a move x:", x, ", y:", y);
    post_nextmove(nextMove)
};


function get_marking_graphics(x, y) {
    let marking = gameData.gameboard[x][y];
    const image_element = new Image();
    if (marking === 0) {
        image_element.src = './images/empty_mark.jpg';
    } else if (marking === 1) {
        image_element.src = './images/x_mark.jpg';
    } else if (marking === -1) {
        image_element.src = './images/o_mark.jpg';
    }
    image_element.addEventListener("click", () => {
        player_makes_move(x, y, gameData.player_mark);
    })
    return image_element;
};


function draw_rectangle_table() {
    // Builds a scalable rectangle-shaped tictactoe-table as a string.
    let table = document.createElement('table');
    table.setAttribute('id', 'tictactoe_table');
    table_size = gameData.board_size;
    for (let y = 1; y <= table_size; y++) {
        tr = document.createElement('tr');
        tr.setAttribute('id', "tr_ " + y.toString())
        for (let x = 1; x <= table_size; x++) {
            // slots_in_row.push('<td>' + get_marking_graphics(x - 1, y - 1) + '</td>');
            const td = document.createElement('td');
            td.setAttribute('id', "td_ " + x.toString() + y.toString())
            td.appendChild(get_marking_graphics(x - 1, y - 1))
            tr.appendChild(td)
        }
        table.appendChild(tr);
    }
    return table;
};


// Main moves for testing locally.
function main() {
    initialize_backend_board(DEFAULT_BOARD_SIZE);
}

main();