from flask import Flask, session, render_template, request
from flask_session import Session
from panda import get_results

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/")
def index():
    offers = get_results()
    return render_template("index.html", offers=offers)