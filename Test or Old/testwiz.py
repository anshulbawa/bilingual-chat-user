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
    # The remote host
PORT = 8036              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', PORT))


message = str(repr(s.recv(1024)))
print(message)
message = 'hello'
message = message.encode()
s.sendall(message)

s.close()


