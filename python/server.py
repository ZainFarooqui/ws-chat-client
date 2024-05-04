import asyncio
import json

HOST = "127.0.0.1"
PORT = 3001

CONNECTIONS = {}

async def message_all(message, sender="SERVER"):
    payload = f"[{sender}] >> {message}"
    dump = json.dumps(payload).encode("utf-8")
    for conn in CONNECTIONS:
        conn.write(dump)
        await conn.drain()


async def message_all_but_sender(sender, message):
    payload = f"[{CONNECTIONS[sender]}] >> {message}"
    dump = json.dumps(payload).encode("utf-8")

    for conn, _ in CONNECTIONS.items():
        if conn != sender:
            conn.write(dump)
            await conn.drain()


async def handle_new_joiner(conn, name):
    print("New joiner: " + name)
    CONNECTIONS[conn] = name
    message = f"{name} has joined the chat"
    await message_all(message)


async def recieve(reader):
    data = await reader.read(1024)
    payload = json.loads(data.decode("utf-8"))
    message = payload.get("message")
    event = payload.get("event", "leave")
    return message, event


async def handle_leaver(conn, message):
    if conn in CONNECTIONS:
        del CONNECTIONS[conn]
    conn.close()
    await conn.wait_closed()

    print(message)
    await message_all(message)


async def handler(reader, writer):
    print(f"Connected by {writer.get_extra_info("peername")}")

    while True:
        try:
            message, event = await recieve(reader)
        except json.JSONDecodeError:
            server_message = f"{CONNECTIONS[writer]} has unexpectedly lost connection"
            await handle_leaver(writer, server_message)
            break

        if event == "join":
            await handle_new_joiner(writer, message)

        if event == "message":
            await message_all_but_sender(writer, message)

        if event == "leave":
            server_message = f"{CONNECTIONS[writer]} has left the chat"
            await handle_leaver(writer, server_message)
            break


async def main():
    server = await asyncio.start_server(handler, HOST, PORT)

    async with server:
        print(f"Server started at {HOST}:{PORT}")
        await server.serve_forever()


asyncio.run(main())
