import asyncio
import itertools
import json
import websockets
from connect4 import PLAYER1, PLAYER2, Connect4
import secrets # Library used to generate secure random numbers for managing secrets

JOIN = {} # Global dictionary variable that holds each user's unique key, each key contains the game and socket connection.
async def error(websocket, message):
    event = {
        "type": "error", 
        "message": message
    }
    await websocket.send(json.dumps(event))

async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    connected.add(websocket)

    try:
        print("second player joined game", id(game))
        async for message in websocket:
            print("second player sent", message)
    finally:
        connected.remove(websocket)

async def start(websocket):
    # Initialize a Connect Four game.
    game = Connect4()
    connected = {websocket}

    join_key  = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {
            "type": "init",
            "join": join_key
            }
        await websocket.send(json.dumps(event))
        print("first player started game", id(game))
        async for message in websocket:
            print("first player sent", message)
    finally:
        del JOIN[join_key]


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        await join(websocket, event["join"])
    else:
        await start(websocket)

    # Players take alternate turns, using the same browser.
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]
        try:
            row = game.play(player, column)
        except RuntimeError as exc:
            # Send an "error" event if the move was illegal.
            event = {
                "type": "error",
                "message": str(exc),
            }
            await websocket.send(json.dumps(event))
            continue

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))

        # If move is winning, send a "win" event.
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            await websocket.send(json.dumps(event))

        # Alternate turns.
        player = next(turns)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())