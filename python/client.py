import asyncio
import json
import websockets

HOST = "127.0.0.1"
PORT = 3002

async def join_server(ws):
    name = input("Welcome to the chat! What should people call you? ")
    
    payload = {
        "message": name,
        "event": "join"
    }
    dump = json.dumps(payload).encode("utf-8")
    await ws.send(dump)

    personal = await ws.recv()
    print(f">> {personal}")
    all = await ws.recv()
    print(f">> {all}")

async def persist_connection(ws):
    next_message = ""
    while next_message != "EXIT!":
        message = input("")

        payload = {
            "message": message,
            "event": "message"
        }
        dump = json.dumps(payload).encode("utf-8")
        await ws.send(dump)

        chat = await ws.recv()
        print(f">> {chat}")


async def main():
    uri = f"ws://{HOST}:{PORT}"
    ws = await websockets.connect(uri)

    await join_server(ws)
    
    await persist_connection(ws)
    

asyncio.run(main())
