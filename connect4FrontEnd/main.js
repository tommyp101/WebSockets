import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".board");
  createBoard(board);
  const websocket = new WebSocket("ws://localhost:8001/");
  recieveMoves(board, websocket);
  sendMoves(board, websocket);
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


// Recieve the event data from server, server used data from browser -> server to alter.
function showMessage(message)
{
  window.setTimeout(() => window.alert(message), 50);
}

function recieveMoves(board, websocket) {
  websocket.addEventListener("message", ({data}) => { // Receive websocket message by listening to message events.
    const event = JSON.parse(data);
    switch (event.type) {
      case "play":
        playMove(board, event.player, event.column, event.row);
        break;
      case "win":
        showMessage(`Player ${event.player} wins!`);
        websocket.close(1000);
        break;
      case "error":
        showMessage(event.message);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}