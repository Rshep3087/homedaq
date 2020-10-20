import os
import time

from dateutil import parser
from flask import flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app, db

from .models import RocketData  # , HomeData
from .util import allowed_file, read_airbrakes_csv


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


@app.route("/api/add-airbrake-data", methods=['GET', 'POST'])
def add_airbrake_data():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("The Uploaded Filename is: " + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = read_airbrakes_csv("app\static\csv_files\LOG.CSV")
            for row in range(0, df.shape[0]):
                new_data = RocketData(id=int(row),
                                      acceleration_x=float(df.iloc[row, [0]]),
                                      acceleration_y=float(df.iloc[row, [1]]),
                                      acceleration_z=float(df.iloc[row, [2]]),
                                      pressure=float(df.iloc[row, [3]]),
                                      temperature=float(df.iloc[row, [4]]),
                                      altitude=float(df.iloc[row, [5]]),
                                      vertical_velocity=float(
                                          df.iloc[row, [6]]),
                                      vertical_velocity_IMU=float(
                                          df.iloc[row, [7]]),
                                      vertical_acceleration=float(
                                          df.iloc[row, [8]]),
                                      airbrakes_state=int(df.iloc[row, [9]]),
                                      time_milliseconds=int(
                                          df.iloc[row, [10]]),
                                      flight_state=int(df.iloc[row, [11]]))
                db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('add_airbrake_data'))

    return '''
    <!doctype html>
    <html lang="en-US">
    <title >Upload new File</title>
    <body style="background-color:lightgrey;">
    <style>
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    h1{background-color:Maroon;
        text-align:center;}
    h2{background-color:orange;
        text-align:center;}
    </style>
    <img src="data:image/png;base64,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" alt="Cyclone Rocketry Logo" width="500" height="200">
    <h1> Airbrakes Subscale Data Upload </h1>
    <h2> Upload LOG CSV File Here:</h2>
    <form method=post enctype=multipart/form-data style="text-align:center;">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <a  href="http://127.0.0.1:5000/api/add-airbrake-data"><p style="text-align:center"><br><br>Use this Link to view results.</p></a>
    '''


@ app.route("/api/time")
def get_current_time():
    return {"time": time.time()}
