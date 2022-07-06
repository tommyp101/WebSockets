import asyncio # Library used to write concurrent code using async/await syntax
import websockets

# async def needs await keyword within function to enable asynchronous and returns a "Promise"
async def handler(websocket): 
    while True:
        # await is used to wait for websocket.recv() to do something whether fails/completes
        try:
            message = await websocket.recv() 
        except websockets.ConnectionClosedOK:
            break
        print(message)
    # This is common so you can do:
    # async def handler(websocket):
    #   async for message in websocket:
    #   print(message)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())