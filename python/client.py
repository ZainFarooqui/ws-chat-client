import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 3001


def recieve(sock):
    res = sock.recv(1024).decode("utf-8")
    data = json.loads(res)
    print(data)


def send(sock, message, event):
    payload = {
        "message": message,
        "event": event,
    }
    dump = json.dumps(payload).encode("utf-8")
    sock.send(dump)


def join_chat(sock):
    print("Welcome to the chat room!")
    message = input("What do you want people to call you? ")
    print("You can leave at any time by CtrlC or typing EXIT!")

    send(sock, message, "join")

    recieve(sock)


def reader(sock, stop_event):
    while not stop_event.is_set():
        try:
            recieve(sock)
        except (ConnectionResetError, json.JSONDecodeError):
            print("Server closed connection")
            stop_event.set()
            leave_chat(sock)



def writer(sock, stop_event):
    while not stop_event.is_set():
        message = input()
        if message == "EXIT!":
            stop_event.set()
            leave_chat(sock)
            break

        send(sock, message, "message")


def persist_chat(sock):
    stop_event = threading.Event()

    rthread = threading.Thread(target=reader, args=(sock, stop_event))
    wthread = threading.Thread(target=writer, args=(sock, stop_event))

    rthread.start()
    wthread.start()

    rthread.join()
    wthread.join()


def leave_chat(sock):
    send(sock, "", "leave")

    print("Thanks for chatting")
    sock.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    join_chat(sock)

    persist_chat(sock)


if __name__ == "__main__":
    main()
