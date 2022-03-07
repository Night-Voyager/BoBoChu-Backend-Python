import asyncio
import websockets
import json


async def test():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(json.dumps(
            {
                "joinRoom": 334634
            }
        ))
        while True:
            print(await websocket.recv())


if __name__ == "__main__":
    asyncio.run(test())
