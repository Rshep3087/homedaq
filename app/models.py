from datetime import datetime
from app import db


class HomeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class RocketData(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    acceleration_x: float = db.Column(db.Float)
    acceleration_y: float = db.Column(db.Float)
    acceleration_z: float = db.Column(db.Float)
    pressure = db.Column(db.Float)
    pressure_units = db.Column(db.String)
    temperature = db.Column(db.Float)
    temperature_units = db.Column(db.String)
    altitude = db.Column(db.Float)
    altitude_units = db.Column(db.String)
    vertical_velocity = db.Column(db.Float)
    vertical_velocity_units = db.Column(db.String)
    vertical_acceleration = db.Column(db.Float)
    vertical_acceleration_units = db.Column(db.String)
    airbrakes_state = db.Column(db.Binary)
    flight_state = db.Column(db.Integer)
    time_milliseconds = db.Column(db.Integer, index=True)
