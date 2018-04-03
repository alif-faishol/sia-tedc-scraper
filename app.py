import json
import mechanicalsoup
from requests.cookies import RequestsCookieJar
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

@app.route("/data")
def get_data():
    if "session" in request.cookies:
        cookie = ''.join(reversed(request.cookies["session"][0:10])) + request.cookies["session"][10:]
        cj = RequestsCookieJar()
        cj.set("PHPSESSID", cookie)
        browser = mechanicalsoup.StatefulBrowser()
        browser.set_cookiejar(cj)
        browser.open('http://siakad.poltektedc.ac.id/politeknik/mahasiswa.php')
        data = {}
        data["bio"] = {}
        data["bio"]["nama"] = browser.get_current_page().select('td[colspan] table[align] td strong')[0].text
        data["bio"]["jurusan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[1].text
        data["bio"]["angkatan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[2].text
        return str(data)
    else:
        return 'tydac'


if __name__=='__main__':
    app.run()
