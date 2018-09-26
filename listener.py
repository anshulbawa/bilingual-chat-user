import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import socket

count = 0;
driver = webdriver.Chrome("../chromedriver/chromedriver.exe")
driver.get("http://www.square-bear.co.uk/mitsuku/nfchat.htm")
driver.switch_to.frame(driver.find_element_by_css_selector("iframe[name='input']"))

HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 8080              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

while 1:
	data = conn.recv(1024)
	if not data: break
	message = str(repr(data))
	element = driver.find_element_by_name("message")
	element.send_keys(message)
	element.submit()
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source)
	soup_str = str(soup)
	global count 
	if ( count == 0):
		result = re.findall(r'You.*<br/> <br/>', soup_str)
		count = 1;
	else:
		result = re.findall(r'You.*You', soup_str)
	response = re.findall(r'</b>[^<]*<br/>', result[0])
	out = response[1]
	substr1 = "</b> "
	substr2 = "<br/>"
	out = out.replace(substr1, '')
	out = out.replace(substr2, '')
	conn.sendall(out.encode())
conn.close()