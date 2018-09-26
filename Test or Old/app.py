from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import re

f = open('message.txt', 'a', os.O_NONBLOCK)

count = 0;
driver = webdriver.Chrome("../chromedriver/chromedriver.exe")
driver.get("http://www.square-bear.co.uk/mitsuku/nfchat.htm")
driver.switch_to.frame(driver.find_element_by_css_selector("iframe[name='input']"))

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("chat.html")

@app.route('/ajax', methods = ['POST'])
def ajax_request():
	message = request.form['message']
	s = message
	element = driver.find_element_by_name("message")
	element.send_keys(s)
	element.submit()
	time.sleep(2)
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
	f.write(s)
	f.write('\n')
	f.write(out)
	f.write('\n')
	f.flush()
	return jsonify(message = out)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    multiply_text = text * 3
    return multiply_text

if __name__ == '__main__':
    app.run()