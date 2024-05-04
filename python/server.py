import socket
import threading

clients = {}

def broadcast(message, sender):
    for addr, client in clients.items():
        if addr != sender:
            client.send(message)

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    clients[addr] = conn
    while True:
        data = conn.recv(1024)
        if not data:
            break
        broadcast(data, addr)

    conn.close()
    del clients[conn]


HOST = "127.0.0.1"
PORT = 3002

sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

while True:
    connection, address = sock.accept()

    thread = threading.Thread(target=handle_client, args=(connection, address)) 
    thread.start()
