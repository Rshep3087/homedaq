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
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = read_airbrakes_csv("app\static\csv_files\LOG.CSV")
            print("Triggered")
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
            print(RocketData)
            db.session.commit()
            return redirect(url_for('add_airbrake_data'))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@ app.route("/api/time")
def get_current_time():
    return {"time": time.time()}
