import socket
from threading import Thread
import sys

class Client(object):

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = 1024

    def connect(self, host, port):
        self.client_socket.connect((host,port))
        receive_thread = Thread(target=self.receive, args=(self.client_socket,))
        send_thread = Thread(target=self.send, args=(self.client_socket,))
        receive_thread.start()
        send_thread.start()

    def receive(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(self.buffer).decode("utf8")
                print(msg)
            except OSError:
                break

    def send(self, client_socket):
        while True:
            msg = input()
            client_socket.send(msg.encode("utf8"))
            if msg == "{quit}":
                client_socket.close()
                break

if __name__ == "__main__":
    client = Client()
    host = input("Enter host: ")
    port = int(input("Enter port: "))
    client.connect(host, port)
