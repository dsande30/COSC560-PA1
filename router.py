#!/usr/bin/env python3

import socket
import threading
import sys, os
from RequestParser import RequestParser
from Responder import Responder

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

    def recvall(self, client):
        BUFF_SIZE = 512 # 4 KiB
        data = b''
        while True:
            part = client.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    def serveClient(self, client, address):
        name = "{}:{}".format(address[0], address[1])
        print("Connected to", name)
        while True:
            try:
                data = self.recvall(client)
                if data:
                    request = RequestParser()
                    request.parseRequest(data)
                    response = Responder(request, client, name)
                    if request.error_code != 200:
                        response.sendError(request.error_code)
                    elif request.action == 'GET':
                        response.sendGET()
                    elif request.action == 'POST':
                        response.sendPOST()
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
    ip = '127.0.0.1'
    port = 8888
    server = Server(ip, port)
    server.listen()
