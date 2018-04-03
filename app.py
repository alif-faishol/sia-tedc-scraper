import json
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
    form['username'] = request.json['username']
    form['passwd'] = request.json['password']
    browser.submit_selected()

    page = str(browser.get_current_page())
    if '<form action="/politeknik/mahasiswa.php"' in page:
        response = make_response('{"status":"failed"}', 200)
    else:
        cj = browser.get_cookiejar()
        cookie = ""
        for c in cj:
            cookie = c.value

        response = make_response('{"status":"success"}', 200)
        response.set_cookie('session', value=''.join(reversed(cookie[0:10])) + cookie[10:])

    return response

def get_data():
    return ''


if __name__=='__main__':
    app.run()
