# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# welcome
@app.route("/")
def welcome():
    """Start at the homepage. List all the available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).order_by(measurement.date.desc()).all()
    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

# stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation)
    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        stations_dict = {}
        stations_dict['station'] = station
        stations_dict['name'] = name
        stations_dict['latitude'] = latitude
        stations_dict['longitude'] = longitude
        stations_dict['elevation'] = elevation
        all_stations.append(stations_dict)
    return jsonify(all_stations)

# tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=last_year).all()
    session.close()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['temperature observations'] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

# start
@app.route("/api/v1.0/<start>")
def temps_s(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date>=start).all()
    session.close()

    # temps = []
    temps_dict = {}
    temps_dict['tmin'] = results[0][0]
    temps_dict['tavg'] = results[0][1]
    temps_dict['tmax'] = results[0][2]
    return jsonify(temps_dict)

# start/end
@app.route("/api/v1.0/<start>/<end>")
def temps_se(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    session.close()

    temps_se_dict = {}
    temps_se_dict['tmin'] = results[0][0]
    temps_se_dict['tavg'] = results[0][1]
    temps_se_dict['tmax'] = results[0][2]
    return jsonify(temps_se_dict)


if __name__ == '__main__':
    app.run(debug=True)
     


