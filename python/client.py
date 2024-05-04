import socket

HOST = "127.0.0.1"
PORT = 3002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

message = input("You > ")

while message != "exit":
    sock.send(message.encode())
    data = sock.recv(1024).decode()

    print("SERVER > " + data)

    message = input("You > ")

sock.close()
