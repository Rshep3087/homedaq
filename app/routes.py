from dateutil import parser

from flask import render_template, request
from app import app
from app import db
from .models import HomeData


@app.route("/")
@app.route("/index")
def index():
    home_data = HomeData.query.limit(30)

    temperatures = [temperature.temperature for temperature in home_data]
    timestamps = [
        timestamp.timestamp.strftime("%H:%M:%S %m-%d-%y") for timestamp in home_data
    ]

    legend = "Home Temperature Data"

    return render_template(
        "index.html",
        title="Home",
        values=temperatures,
        labels=timestamps,
        legend=legend,
    )


@app.route("/add_data", methods=["POST"])
def add_data():
    home_data = request.get_json()

    new_data = HomeData(
        temperature=home_data["temperature"], timestamp=home_data["time"]
    )

    db.session.add(new_data)
    db.session.commit()
    return "Done", 201

