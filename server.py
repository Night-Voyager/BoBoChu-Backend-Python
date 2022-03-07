import asyncio
import json
import random

import websockets

from bobochu import Room

ROOMS = {}


async def error(websocket, message):
    """
    Send an error message
    """
    error_message = {
        "type": "error",
        "message": message
    }
    await websocket.send(json.dumps(error_message))


async def wait_for_game_start(websocket, room):
    """
    Wait for the room creator to start the game
    """
    if websocket == room.players[0]:
        async for message in websocket:
            if "start" in json.loads(message):
                websockets.broadcast(room.players, json.dumps({"start": None}))
    else:
        while True:
            pass


async def create_room(websocket):
    """
    Create a new room
    """

    # Generate a six-bit room number randomly
    room_number = random.randint(0, 999999)
    while room_number in ROOMS:
        room_number = random.randint(0, 999999)

    # Instantiate a room and register the player to the room
    room = Room(room_number)
    room.players.append(websocket)
    ROOMS[room_number] = room

    # Send the number of created room to the player
    try:
        message = {
            "roomNumber": room_number
        }
        await websocket.send(json.dumps(message))
        print("New room created with number %d, currently %d room(s) exist(s)" % (room_number, len(ROOMS)))
        await wait_for_game_start(websocket, room)
    finally:
        del ROOMS[room_number]


async def join_room(websocket, room_number):
    """
    Join a room if exists
    """

    # Find the room according to the room number
    try:
        room = ROOMS[room_number]
    except KeyError:
        await error(websocket, "Room not found")
        return

    # Register the player to the room
    room.players.append(websocket)
    print("New player joins room %d, currently %d player(s) joined" % (room_number, len(room.players)))
    websockets.broadcast(room.players, json.dumps({"newJoin": None}))
    await wait_for_game_start(websocket, room)


async def handler(websocket):
    """
    Handle a connection and dispatch it according to who is connecting.
    """

    # The message should be one of the following forms:
    #  - {"createRoom": null}
    #  - {"joinRoom": roomNumber}
    message = json.loads(await websocket.recv())

    if "createRoom" in message:
        # Create a new room
        await create_room(websocket)
    elif "joinRoom" in message:
        # Join a room if exists
        await join_room(websocket, message["joinRoom"])
    else:
        # Handle errors
        await error(websocket, "Illegal message: " + json.dumps(message))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
