from dateutil import parser
import time

from flask import render_template, request
from app import app
from app import db
from .models import HomeData, RocketData


@app.route("/api/index")
def index():
    """
    Get the data to display to user
    """
    home_data = HomeData.query.order_by(HomeData.timestamp.desc()).limit(30)

    temperatures = [temperature.temperature for temperature in home_data]
    timestamps = [
        timestamp.timestamp.strftime("%H:%M:%S %m-%d-%y") for timestamp in home_data
    ]

    average_temperature = sum(temperatures) / len(temperatures)

    legend = "Home Temperature Data"

    return {
        "values": temperatures,
        "timestamps": timestamps,
        "legend": legend,
        "average_temperature": average_temperature,
    }


@app.route("/api/add_data", methods=["POST"])
def add_data():
    home_data = request.get_json()
    print(home_data)
    time = parser.parse(home_data["time"])

    new_data = HomeData(temperature=home_data["temperature"], timestamp=time)

    db.session.add(new_data)
    db.session.commit()
    return "Done", 201


@app.route("/api/add-airbrake-data", methods=["POST"])
def add_airbrake_data():
    airbrake_data = request.get_json()
    print(airbrake_data)
    # new_data = RocketData()

    # db.session.add(new_data)
    # db.session.commit()
    return "Done", 201


@app.route("/api/time")
def get_current_time():
    return {"time": time.time()}
