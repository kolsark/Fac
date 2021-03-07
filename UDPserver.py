#!/usr/bin/python3
import socket

s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind (("",7777))

Tret = b""

while(1):
    Tret = s.recvfrom(1500)
    if (Tret[0] != b""):
        s.sendto(Tret)
       
s.close()
