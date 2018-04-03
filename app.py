import requests
import json
from flask import Flask, make_response, render_template

app = Flask(__name__) 

@app.route("/")
def hello():
    return 'home page'

@app.route("/login")
def get_cookies():
    return 'login'


if __name__=='__main__':
    app.run()
