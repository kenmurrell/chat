import socket
from threading import Thread
import sys

class Client(object):

    BUFFER_SIZE = 1024
    TIMEOUT = 10

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(Client.TIMEOUT)

    def connect(self, host, port):
        try:
            self.client_socket.connect((host,port))
        except OSError:
            print("-> Error connecting to %s:%s. Is the host and port correct?" % (host,port))
            sys.exit(1)
        receive_thread = Thread(target=self.receive, args=(self.client_socket,))
        send_thread = Thread(target=self.send, args=(self.client_socket,))
        receive_thread.start()
        send_thread.start()

    def receive(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(Client.BUFFER_SIZE).decode("utf8")
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
