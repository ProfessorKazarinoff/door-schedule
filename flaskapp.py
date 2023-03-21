# flaskapp.py

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1> Flask App to build a schedule</h1>"
