import requests
import json
from flask import Flask, make_response, render_template

application = Flask(__name__) 

@application.route("/")
def hello():
    return 'home page'

@application.route("/login")
def get_cookies():
    jsonData = {
        "spider_name":"siakad.poltektedc.ac.id",
        "start_requests":"true",
        "request": {
            "meta": {
                "id": "",
                "pass": ""
            },
        },
        "custom":"D111"
    }
    cookie = requests.post('http://localhost:9080/crawl.json', json=jsonData)
    #jCookie = json.loads(cookie.text)
    response = make_response(cookie.text, 200)
    response.set_cookie('session', value='', max_age=1440)
    return cookie.text


if __name__=='__main__':
    application.run()
