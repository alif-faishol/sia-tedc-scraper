import mechanicalsoup
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return 'hai'

@app.route("/login", methods=["POST"])
def logging_in():

    # Fill login form and submit
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://siakad.poltektedc.ac.id')
    form = browser.select_form(selector='form')
    form['username'] = request.json['username']
    form['passwd'] = request.json['password']
    browser.submit_selected()

    # Get the cookie from target website if login not failed
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

        # Use cookie from client request, with slight edit
        cookie = ''.join(reversed(request.cookies["session"][0:10])) + request.cookies["session"][10:]
        cj = RequestsCookieJar()
        cj.set("PHPSESSID", cookie)

        # Setup browser, use cookie from client
        browser = mechanicalsoup.StatefulBrowser()
        browser.set_cookiejar(cj)

        data = {}

        # Get data from mahasiswa.php page
        browser.open('http://siakad.poltektedc.ac.id/politeknik/mahasiswa.php')
        data["bio"] = {}
        data["bio"]["nama"] = browser.get_current_page().select('td[colspan] table[align] td strong')[0].text
        data["bio"]["jurusan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[1].text
        data["bio"]["angkatan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[3].text

        return jsonify(data)
    else:
        return 'tydac'


if __name__=='__main__':
    app.run()
