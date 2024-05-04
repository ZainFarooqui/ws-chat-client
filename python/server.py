import asyncio
import json
import websockets

HOST = "127.0.0.1"
PORT = 3002

CONNECTIONS = set()

def message_all(message):
    websockets.broadcast(CONNECTIONS, message)

async def message_all_but_sender(websocket, message):
    for conn in CONNECTIONS:
        if conn != websocket:
            await conn.send(message)


async def hello(websocket):
    dump = b''
    dump += await websocket.recv()
    payload = json.loads(dump.decode("utf-8"))
    name = payload["message"]
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def handle_new_joiner(websocket, name):
    print("New joiner: " + name)    
    personal_message = "You can leave at any time by CtrlC or typing EXIT!"
    await websocket.send(personal_message)
    
    CONNECTIONS.add(websocket)
    message = f"{name} has joined the chat"
    message_all(message)


async def handler(websocket):
    while True:
        dump = b''
        dump += await websocket.recv()
        payload = json.loads(dump.decode("utf-8"))

        if payload["event"] == "join":
            await handle_new_joiner(websocket, payload["message"])
        
        if payload["event"] == "message":
            await message_all_but_sender(websocket, payload["message"])
    
async def main():
    await websockets.serve(handler, HOST, PORT)
    await asyncio.Future()

asyncio.run(main())
