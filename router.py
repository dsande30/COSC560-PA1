#!/usr/bin/env python3

import socket
import threading
import sys

class Server():
    def __init__(self, ip, port):
        self.host = ip
        self.port = port
        self.sock = socket.socket()

        # setsockopt allows for more flexible socket binding
        # (i.e. 1.1.1.1:23 and 0.0.0.0:23 can be bound simultaneously)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((self.host, self.port)) 
        print("Bounded on {}:{}".format(self.host, self.port))

    def listen(self):
        self.sock.listen(5) # queue up to 5 clients

        # server runs infinitely and threads off each incoming connection
        while True:
            client, address = self.sock.accept()
            client.settimeout(30) # times out if client inactive for 30 seconds
            threading.Thread(target = self.serveClient, args = (client,address)).start()

    def serveClient(self, client, address):
        name = "{}:{}".format(address[0], address[1])
        print("Connected to", name)
        client.send('Hi, I\'m the thread that will be processing your requests :)'.encode())
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Response for now is just an echo back of same data
                    # This is where RequestParser would come into play
                    response = data
                    client.send(response)
                else:
                    raise Exception('Client {} disconnected'.format(name))
            except Exception as e:
                print(e)
                client.close()
                return False # need to return to safely exit the thread
                
if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 8888
    server = Server(ip, port)
    server.listen()
