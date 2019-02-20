#!/usr/bin/env python3
import socket

ip = '127.0.0.1'
port = 8888

s = socket.socket()
s.connect((ip, port))

while True:
    r = s.recv(1024)
    print("Server says: " + r.decode('ascii'))

    msg = input(" -> ")
    if msg == 'exit':
        s.close()
        break
    s.sendall(msg.encode())
