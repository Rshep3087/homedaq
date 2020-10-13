import json

import pandas as pd

ALLOWED_EXTENSIONS = {'csv'}


def read_airbrakes_csv() -> str:
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

    return df


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
