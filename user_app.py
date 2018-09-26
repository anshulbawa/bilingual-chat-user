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

HOST = '10.168.237.173'   # The remote host - IP from ifconfig
PORT = 8080               # The same port as used by the server
conn_usr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_usr.connect((HOST, PORT))   # replaced host name with blank string - Why?

app = Flask(__name__)

@app.route('/')
def my_form():
	print "Rendering template"
	return render_template("basic.html")

@app.route('/step2', methods = ['POST'])
def step2():
	m1 = request.form['message'].encode().strip('\'').strip('\"')
	print "STEP 1"
	conn_usr.sendall(m1)
	print "STEP 2",m1
	# return jsonify(message = m1)
	m4 = str(repr(conn_usr.recv(1024))).strip('\'')
	print "STEP 23 and starting 24",m4
	return jsonify(message = m4)

@app.route('/step23', methods = ['POST'])
def step23():
	m4 = str(repr(conn_usr.recv(1024))).strip('\'').strip('\"').encode()
	print "STEP 23 and starting 24",m4
	return jsonify(message = m4)

if __name__ == '__main__':
    	app.run(host = '0.0.0.0', port =5000)
	s.close()