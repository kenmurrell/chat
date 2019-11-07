from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

HOST = input("Enter host: ")
PORT = int(input("Enter post: "))

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
        except OSError:
            break

def send():
    while True:
        msg = input()
        client_socket.send(msg.encode("utf8"))
        if msg == "{quit}":
            client_socket.close()
            break
    sys.exit(1)

receive_thread = Thread(target=receive)
receive_thread.start()
send_thread = Thread(target=send)
send_thread.start()
