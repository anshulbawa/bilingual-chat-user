import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import socket

                 # Symbolic name meaning all available interfaces
PORT = 8036              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

                 # Symbolic name meaning all available interfaces
PORT = 8080              # Arbitrary non-privileged port
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind(('', PORT))
s1.listen(1)
conn1, addr = s1.accept()
print ('Connected by', addr)


while 1:
	data = conn1.recv(1024)
	if not data: break
	message = str(repr(data))
	conn.sendall(message.encode())
	data = conn.recv(1024)
	if not data: break
	message = str(repr(data))
	conn1.sendall(message.encode())
conn.close()
conn1.close()