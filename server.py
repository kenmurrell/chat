from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import socket as sock_base
import logging

format_string = "%(asctime)s %(message)s"

logging.basicConfig(format=format_string, level=logging.INFO, datefmt="%H:%M:%S")
logger = logging.getLogger("log")

clients={}
addresses={}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(sock_base.SOL_SOCKET, sock_base.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        logger.info("%s:%s has connected" % client_address)
        send_personal(client,"Please enter your name to continue")
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    send_personal(client,"Welcome %s to the server. Type {quit} to exit" % name)
    broadcast("%s has joined" % name, "SERVER")
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if msg == "{quit}":
            del clients[client]
            logger.info("%s:%s has left the server" % addresses[client])
            broadcast("%s has left" % name, "SERVER")
            client.close()
            break
        else:
            broadcast(msg, name)

def broadcast(text, prefix):
    for client in clients:
        msg = prefix + "> " + text
        client.send(msg.encode("utf8"))

def send_personal(client, text):
    msg = "SERVER" + "> " + text
    client.send(msg.encode("utf8"))

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
