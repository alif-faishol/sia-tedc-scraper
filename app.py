from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

def setupBrowserWithCookie(cookie):
    import mechanicalsoup
    from requests.cookies import RequestsCookieJar

    # Use cookie from client request, with slight edit
    c = ''.join(reversed(cookie[0:10])) + cookie[10:]
    cj = RequestsCookieJar()
    cj.set("PHPSESSID", c)

    # Setup browser, use cookie from client
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_cookiejar(cj)

    return browser

def isInLoginPage(page):
    page = str(page)
    if 'form action="/politeknik/mahasiswa.php"' in page:
        return True
    else:
        return False


@app.route("/")
def hello():
    return 'hai'

@app.route("/login", methods=["POST"])
def logging_in():
    import mechanicalsoup

    # Fill login form and submit
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://siakad.poltektedc.ac.id')
    form = browser.select_form(selector='form')
    form['username'] = request.json['username']
    form['passwd'] = request.json['password']
    browser.submit_selected()

    # Get the cookie from target website if login not failed
    if isInLoginPage(browser.get_current_page()):
        response = make_response('{"status":"failed"}', 200)
    else:
        cj = browser.get_cookiejar()
        cookie = ""

        for c in cj:
            cookie = c.value

        response = make_response('{"status":"success"}', 200)
        response.set_cookie('session', value=''.join(reversed(cookie[0:10])) + cookie[10:])

    return response

@app.route("/data/")
def get_data():
    if "session" in request.cookies:
        browser = setupBrowserWithCookie(request.cookies["session"])

        # Get data from mahasiswa.php page
        browser.open('http://siakad.poltektedc.ac.id/politeknik/mahasiswa.php')
        if isInLoginPage(browser.get_current_page()):
            return jsonify({"status":"failed"})

        data = {}
        data["bio"] = {}
        data["bio"]["nama"] = browser.get_current_page().select('td[colspan] table[align] td strong')[0].text
        data["bio"]["jurusan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[1].text
        data["bio"]["angkatan"] = browser.get_current_page().select('td[colspan] table[align] td strong')[3].text
        data["news"] = []

        newsLen = len(browser.get_current_page().select('table[bgcolor="#AAEB83"]'))
        i = 0
        while i < newsLen:
            data["news"].append({
                "date": browser.get_current_page()
                .select('table[bgcolor="#AAEB83"]')[i]
                .select('tr:nth-of-type(1)')[0].text,
                "title": browser.get_current_page()
                .select('table[bgcolor="#AAEB83"]')[i]
                .select('tr:nth-of-type(2)')[0].text,
                "body": str(browser.get_current_page()
                            .select('tr[bgcolor="#C1EBFF"]')[i]
                            .select('td:nth-of-type(3)')[0])
            })
            i += 1

        return jsonify(data)
    else:
        return jsonify({"status":"failed"})

@app.route("/data/grades/")
def get_grades():
    browser = setupBrowserWithCookie(request.cookies["session"])
    browser.open('http://siakad.poltektedc.ac.id/politeknik/khs.php')

    gradeTables = browser.get_current_page().select('table[border="1"]')[1]
    data = {
        "name": gradeTables.select('tr')[0].text,
        "semester": [],
    }

    i = -1
    find=lambda x: x and (x == "#CCFDCC") or (x == "#FFD2D2")
    for item in gradeTables.find_all('tr', bgcolor=find):

        # Mark no.1 as starting point for list of grades in a semester
        if item.select('td')[0].text == "1":
            data["semester"].append([])
            i += 1
        data["semester"][i].append({
            "no": item.select('td')[0].text,
            "code": item.select('td')[1].text,
            "name": item.select('td')[3].text,
            "credit": item.select('td')[4].text,
            "grade": item.select('td option["selected"]')[0].text,
        })

    return jsonify(data)

if __name__=='__main__':
    app.run()
