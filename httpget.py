#!/usr/bin/python3
import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]
port = 80
try:
    s.connect((host, port))
except (socket.gaierror, ConnectionRefusedError) as e:
    print("socket error!")
    sys.exit(1)
    
request = "GET / HTTP/1.1\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"
    
s.sendall(request.encode("utf-8"))
data = s.recv(1024)
while data != b"":
    print(data.decode(),end = '')
    data = s.recv(1024)
    
s.close()