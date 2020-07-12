from dateutil import parser

from flask import render_template, request
from app import app
from app import db
from .models import HomeData


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/add_data", methods=["POST"])
def add_data():
    home_data = request.get_json()
    time = parser.parse(home_data["time"])

    new_data = HomeData(temperature=home_data["temperature"], timestamp=time)

    db.session.add(new_data)
    db.session.commit()
    return "Done", 201

