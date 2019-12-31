from flask import Flask, session, render_template, request
from flask_session import Session
from panda import get_results, get_results_for_city
from offers import get_offers
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
import datetime


app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'abc'
Session(app)


class search_form(FlaskForm):
    from_code = StringField('from_code')
    to_code = StringField('to_code')
    from_date = DateField('from_date', format='%Y-%m-%d')
    to_date = DateField('to_date', format='%Y-%m-%d')


@app.route("/", methods=['GET', 'POST'])
def index():
    form = search_form()
    return render_template("index.html", form = form)


@app.route("/results", methods=["POST"])
def results():
    from_code = request.form['from_code']
    to_code = request.form['to_code']
    from_date = datetime.datetime.strptime(request.form['from_date'], '%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(request.form['to_date'], '%Y-%m-%d').date()
    get_offers(from_code, to_code, from_date, to_date)
    offers = get_results()
    return render_template("results.html", offers=offers, from_code=from_code, to_code=to_code)


@app.route("/<string:city>", methods=["GET"])
def city(city):
    offers = get_results_for_city(city)
    return render_template("city.html", offers=offers)


if __name__  == '__main__':
    app.run(debug=True)