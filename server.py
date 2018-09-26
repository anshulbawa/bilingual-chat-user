import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import socket
import math
import random

global count
count = 0;
driver = webdriver.Chrome("../chromedriver/chromedriver.exe")
driver.get("http://www.mitsuku.co.uk/") # ping new site instead of squarebear one

HOST = '10.168.237.173'  #IP
PORT = 8036              # Wizard Port
s_wiz = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_wiz.bind((HOST, PORT))
s_wiz.listen(1)
conn_wiz, addr_wiz = s_wiz.accept()
print ('Connected by', addr_wiz)

PORT = 8080              # User Port
s_usr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_usr.bind((HOST, PORT))
s_usr.listen(1)
conn_usr, addr_usr = s_usr.accept()
print ('Connected by', addr_usr)


#Policy Guide
degreecodes = {'N' : 0,
           'T' : 1,
           'L' : 2,
           'P' : 3
           }
def mode_code(x) :
	return degreecodes[x[1]] if (x[0]=='E') else 7 - degreecodes[x[1]]
	# return (x[0]=='H')*5 + degreecodes[x[1]]
code_mode = {
	0 : 'EN', 
	1 : 'ET',
	2 : 'EL',
	3 : 'EP',
	4 : 'HP',
	5 : 'HL',
	6 : 'HT',
	7 : 'HN',
}
mode_history = []

def policy0(modes) : #none
	return code_mode[0]

def policy1(modes) : #random
	return code_mode[math.random.randint(0,7)]

def policy2(modes) : #nudge #better policy think
	if len(mode_history) > 3 :
		modes = modes[-3:]
	avgmode = math.ceil(float(sum(modes))/max(len(modes),1))
	delta = 0
	if random.uniform(0,1) > 0.5 :
		delta = 1
	return code_mode[min(avgmode+delta,7)]

while 1:
	m1 = str(repr(conn_usr.recv(1024))).encode().strip('\'').strip('\"') # initial message sent by user
	print "STEP 3",m1
	conn_wiz.sendall(m1)
	print "STEP 4"
	time.sleep(1)
	m2md = str(repr(conn_wiz.recv(1024))).strip('\'').strip('\"')
	print "STEP 11",m2md
	m2, md = m2md.split(';') # translated has the translated message and mode has the CS modes
	
	mode_history.append(mode_code(md))
	md2 = policy2(mode_history)
	mode_history.append(mode_code(md2))

	if (count == 0):
		driver.switch_to.frame('mainframe')
	element = driver.find_element_by_name("message")
	
	# # /html/body/center/table/tbody/tr[3]/td[2]/font/p/font/text()[2]

	element.send_keys(m2)
	element.submit()
	print "STEP 12"
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source, "lxml")
	soup_str = str(soup) 
	if ( count == 0):
		result = re.findall(r'You.*<br/> <br/>', soup_str)
		count = 1;
	else:
		result = re.findall(r'You.*You', soup_str)
	m3 = re.findall(r'</b>[^<]*<br/>', result[0])[1].replace("</b> ", '').replace("<br/>", '').strip(' ').encode()
	m3md2 = m3+';'+md2.encode()
	print "STEP 13,14,15",m3md2
	conn_wiz.sendall(m3md2)
	print "STEP 16"
	m4 = str(repr(conn_wiz.recv(1024))).encode().strip('\'').strip('\"')
	print "STEP 21",m4
	conn_usr.sendall(m4)
	print "STEP 22"
conn_usr.close()
conn_wiz.close()