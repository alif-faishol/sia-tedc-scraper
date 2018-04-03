import json
import base64
import mechanicalsoup
import http.cookiejar
from bs4 import BeautifulSoup
from flask import Flask, request, make_response

app = Flask(__name__) 

@app.route("/")
def hello():
    return 'hai'

@app.route("/login", methods=["POST"])
def logging_in():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://siakad.poltektedc.ac.id')
    form = browser.select_form(selector='form')
    #form['username'] = request.data['username']
    #form['passwd'] = request.data['password']

    cj = browser.get_cookiejar()
    cookie = ""
    for c in cj:
        cookie = c.value

    response = make_response('{"status":"success"}', 200)
    response.set_cookie('session', value=''.join(reversed(cookie[0:10])) + cookie[10:])
    return response

if __name__=='__main__':
    app.run()
