import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".board");
  createBoard(board);
});

function sendMoves(board, websocket) {
  // When clicking a column, send a "play" event for a move in that column.
  board.addEventListener("click", ({ target }) => {
    const column = target.dataset.column;
    // Ignore clicks outside a column.
    if (column === undefined) {
      return;
    }
    const event = {
      type: "play",
      column: parseInt(column, 10),
    };
    websocket.send(JSON.stringify(event));
  });
}