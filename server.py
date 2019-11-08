from threading import Thread
import socket
import logging

class Server(object):

    def __init__(self, host='', port=30000):
        format_str = "%(asctime)s %(message)s"
        logging.basicConfig(format=format_str, level=logging.INFO, datefmt="%H:%M:%S")
        self.logger = logging.getLogger("log")
        self.host = host
        self.port = port
        self.buffer = 1024
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_clients = list()
        self.name_map = dict()

    def accept_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            self.active_clients.append(client_socket)
            self.logger.info("%s:%s has connected" % client_socket.getsockname())
            self.send(client_socket, "SERVER", "Please enter your name to continue")
            client_name = client_socket.recv(self.buffer).decode("utf8")
            self.name_map[client_socket] = client_name
            self.broadcast("SERVER", "%s has joined" % client_name)
            self.send(client_socket, "SERVER", "Welcome to the server %s!. Type {quit} to exit" % client_name)
            Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self,client_socket):
        while True:
            text = client_socket.recv(self.buffer).decode("utf8")
            if text == "{quit}":
                self.kick(client_socket)
                break
            else:
                self.broadcast(self.name_map[client_socket], text)

    def kick(self,client_socket):
        client_name = self.name_map[client_socket]
        del self.name_map[client_socket]
        self.active_clients.remove(client_socket)
        self.logger.info("%s:%s has disconnected" % client_socket.getsockname())
        client_socket.close()
        self.broadcast("%s has left" % client_name, "SERVER")

    def send(self, client_socket, sender, text):
        msg = sender + "> " + text
        client_socket.send(msg.encode("utf8"))

    def broadcast(self, sender, text):
        for client_socket in self.active_clients:
            self.send(client_socket, sender, text)

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host,self.port))
        self.server_socket.listen(5)
        print("Waiting for connection...")
        thread = Thread(target=self.accept_connections)
        thread.start()
        thread.join()
        self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start()
