from flask import Flask, session, render_template, request
from flask_session import Session
from panda import get_results, get_results_for_city
from offers import get_offers
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
import datetime


app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'abc'
Session(app)


class search_form(FlaskForm):
    from_code = StringField('From City', default='WRO')
    to_code = StringField('To City', default='XXX')
    from_date = DateField('From Date', format='%Y-%m-%d', default=datetime.date(2020, 3, 16))
    to_date = DateField('To Date', format='%Y-%m-%d', default=datetime.date(2020, 3, 22))
    travellers = IntegerField('Travellers', default=2)
    min_days = IntegerField('Min Days', default=4)
    max_days = IntegerField('Max Days', default=6)
    rating = SelectField('Rating', choices=[(5, '+5'), (6, '+6'), (7, '+7'), (8, '+8'), (9, '+9')], default=9)
    distance = IntegerField('Center Distance', default=1)
    rooms = IntegerField('Rooms', default=1)
    apartment = BooleanField('Apartments')
    hostel = BooleanField('Hostels', default=True)
    hotel = BooleanField('Hotels', default=True)
    guest_house = BooleanField('Guest Houses', default=True)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = search_form()
    return render_template("index.html", form=form)

# sfasffa
@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method == 'POST':
        from_code = request.form['from_code']
        to_code = request.form['to_code']
        from_date = datetime.datetime.strptime(request.form['from_date'], '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(request.form['to_date'], '%Y-%m-%d').date()
        min_days = request.form['min_days']
        max_days = request.form['max_days']
        travellers = request.form['travellers']
        distance = request.form['distance']
        rooms = request.form['rooms']
        rating = request.form['rating']
        # don;t undestand why unchecked boolean fields returns error (get method as workaround)
        apartment = request.form.get('apartment')
        hostel = request.form.get('hostel')
        hotel = request.form.get('hotel')
        guest_house = request.form.get('guest_house')
        room_types_raw = [apartment, hostel, hotel, guest_house]
        print(room_types_raw)
        room_types = list(map(lambda x: x == 'y', room_types_raw))
        print(room_types)
        get_offers(from_code, to_code, from_date, to_date, min_days, max_days, travellers, distance, rooms, rating, room_types)
    offers = get_results()
    return render_template("results.html", offers=offers)


@app.route("/<string:city>", methods=["GET"])
def city(city):
    offers = get_results_for_city(city)
    return render_template("results.html", offers=offers)


if __name__ == '__main__':
    app.run(debug=True)