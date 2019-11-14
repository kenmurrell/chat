from threading import Thread
import socket
import logging
import sys
import datetime

class Server(object):

    BUFFER_SIZE = 1024
    LOG_NAME = "chat"

    def __init__(self, server_name="SERVER"):
        self.name = server_name
        logging.basicConfig(
            format="%(asctime)s %(message)s",
            level=logging.INFO,
            datefmt="%H:%M:%S",
            handlers=[
                logging.FileHandler("%s-%s.log" % (Server.LOG_NAME,datetime.datetime.now().strftime("%H%M%S"))),
                logging.StreamHandler(sys.stdout)
            ])
        self.logger = logging.getLogger("log")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_clients = list()

    def accept_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            self.logger.info("%s:%s has connected" % client_socket.getpeername())
            self.send(client_socket, self.name, "Please enter your name to continue:")
            client_name = client_socket.recv(Server.BUFFER_SIZE).decode("utf8")
            self.send(client_socket, self.name, "Welcome to the server %s! Type {quit} to exit." % client_name)
            self.active_clients.append(client_socket)
            self.broadcast(self.name, "%s has joined the server!" % client_name)
            Thread(target=self.handle_client, args=(client_socket,client_name,)).start()

    def handle_client(self,client_socket,client_name):
        while True:
            text = client_socket.recv(Server.BUFFER_SIZE).decode("utf8")
            if text == "{quit}":
                self.kick(client_socket, client_name)
                break
            else:
                self.broadcast(client_name, text)

    def kick(self,client_socket, client_name):
        self.active_clients.remove(client_socket)
        self.logger.info("%s:%s has disconnected" % client_socket.getpeername())
        client_socket.close()
        self.broadcast(self.name, "%s has left the server!" % (client_name))

    def send(self, client_socket, sender, text):
        msg = sender + "> " + text
        client_socket.send(msg.encode("utf8"))

    def broadcast(self, sender, text):
        self.logger.info("%s> %s"%(sender,text))
        for client_socket in self.active_clients:
            self.send(client_socket, sender, text)

    def start(self, host='', port=30000):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.logger.info("Running on %s:%s" % (self.getlocalip(),port))
        self.logger.info("Waiting for connections...")
        thread = Thread(target=self.accept_connections)
        thread.start()
        thread.join()
        self.server_socket.close()

    def getlocalip(self):
        local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            local.connect(('8.8.8.8',1))
            return local.getsockname()[0]
        except OSError:
            pass;
        return self.server_socket.getsockname()[0]

if __name__ == "__main__":
    server = Server()
    server.start()
