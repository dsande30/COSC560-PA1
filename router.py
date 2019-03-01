#!/usr/bin/env python3

"""
Basic HTTP server (main driver).
Processes all incoming and outgoing HTTP Requests/Responses
Creates a new thread for every request and handles it
Calls appropriate RequestParser.py and Responder.py objects
"""

import socket
import threading
import sys, os
from RequestParser import RequestParser
from Responder import Responder

class Server():
    def __init__(self, ip, port):
        """Initializes our server and binds to a socket."""

        self.host = ip
        self.port = port
        self.sock = socket.socket()

        # setsockopt allows for more flexible socket binding
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((self.host, self.port)) 
        print("Bounded on {}:{}".format(self.host, self.port))

    def listen(self):
        """Listens for incoming connections and threads them off."""

        self.sock.listen(5) # queue up to 5 clients
        # server runs infinitely and threads off each incoming connection
        while True:
            client, address = self.sock.accept()
            client.settimeout(30) # times out if client inactive for 30 seconds
            threading.Thread(target = self.serveClient, args = (client,address)).start()

    def recvall(self, client):
        """A helper function to receive ALL client data before proceeding."""

        BUFF_SIZE = 512
        data = b''
        while True:
            part = client.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    def serveClient(self, client, address):
        """Receives request, parses it, responds, and closes connection."""

        name = "{}:{}".format(address[0], address[1])
        print("Connected to", name)
        while True:
            try:
                data = self.recvall(client)
                if data:
                    print("here")
                    request = RequestParser(data) # initialize RequestParser object
                    request.parseRequest() # parse the request
                    response = Responder(request, client, name)

                    # call the appropriate Responder function based on status code
                    if request.error_code != 200:
                        response.sendError(request.error_code)
                    elif request.action == 'GET':
                        response.sendGET()
                    elif request.action == 'POST':
                        response.sendPOST()

                    # close the connection once the client has been served
                    # and exit the thread    
                    print('Served {}, disconnecting.'.format(name))
                    client.close()
                    return False
                else:
                    raise Exception('Client {} disconnected'.format(name))
            except Exception as e:
                print(e)
                client.close()
                return False # need to return to safely exit the thread
                
if __name__ == "__main__":
    ip = '127.0.0.1' # localhost
    port = 8888 # our default port
    server = Server(ip, port)
    server.listen()
