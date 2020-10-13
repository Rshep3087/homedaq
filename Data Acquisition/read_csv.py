"""
Author: Daniel Williams
Created: 10/13/2020 11:08
This script is intended to read in the Airbrakes data struct and then prep the output for the web app.
"""

import pandas as pd
import json


def read_airbrakes_csv():
    column_names = ["Acceleration_Heading", "Acceleration_X", "Acceleration_Y", "Acceleration_Z", "Pressure_Heading", "Pressure (Pa)",
                    "Temperature_Heading", "Temperature (C)", "Altitude_Heading", "Altitude (Ft)", "VelV_Heading", "VelV (ft/s)",
                    "VelV_IMU_Heading", "VelV_IMU", "AccelV_Heading", "AccelV", "Actuation_Heading", "Actuation State", "Time_Heading",
                    "Time Milli-Seconds", "Flight_State_Heading", "Flight_State"]
    df = pd.read_csv(
        "D:\Documents\Programs\Python\Homedaq\homedaq\Data Acquisition\LOG.CSV")
    df.columns = column_names
    removed_columns = ["Acceleration_Heading", "Pressure_Heading", "Temperature_Heading", "Altitude_Heading", "VelV_Heading",
                       "VelV_IMU_Heading", "AccelV_Heading", "Actuation_Heading", "Time_Heading", "Flight_State_Heading"]
    df.drop(removed_columns, axis=1, inplace=True)
    data = df.to_json()
    # print(data)
    # test_data = json.loads(data)
    return data


read_airbrakes_csv()
