
export function draw_rectangle_table(table_size) {
    // Builds a scalable rectangle-shaped tictactoe-table.
    const gameboard_zone = document.getElementById("gameboard_zone");
    var rows = [];
    for (let i = 1; i <= table_size; i++) {
        var slots_in_row = [];
        for (let j = 1; j <= table_size; j++) {
            slots_in_row.push('<td>Empty</td>')
        }
        rows.push('<tr>' + slots_in_row.join('') + '</tr>')
    }

    // Create the HTML string for the table
    var tableHTML = '<table>' + rows.join('') + '</table>';
}