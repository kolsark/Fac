#!/usr/bin/python3
import socket
import sys

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("",7777))
s.listen(1)

Tret = b""

while(1):
    Tret = s.accept()
    if (Tret[0] != b""):
        while(1):
            data = Tret[0].recv(1500)
            if (sys.getsizeof(data) == 0):
                break
            Tret[0].send(data)

s.close()