#!/usr/bin/python3
import socket
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 7777

s.connect((host, port))

while (1):
    line = sys.stdin.readline()
    if (line != b""):
        s.sendall(line.encode("utf-8"))

    data = s.recv(1024)

    if (data.decode() == "\n"):
        break
    else:
        print(data.decode(),end = '')
        
s.close()