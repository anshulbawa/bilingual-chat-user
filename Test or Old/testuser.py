from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import re
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 8080              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', PORT))# replaced host name with blank string

message = 'Hi there'
message = message.encode()
s.sendall(message)
message = str(repr(s.recv(1024)))
print(message)

s.close()