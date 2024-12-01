# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/jesusmatajr/Desktop/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome ():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))
        .all()
    )

    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)



@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    station_list = [station[0] for station in results]

    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    most_active_station = (
        session.query(Measurement.station, func.count(Measurement.station))
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .first()[0]
    )

    results = (
        session.query(Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))
        .all()
    )

    tobs_list = [temp[0] for temp in results]

    return jsonify(tobs_list)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start=None, end=None):
    if not end:
        results = (
            session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs), 
                func.max(Measurement.tobs),
            )
            .filter(Measurement.date >= start)
            .all()
        )
    else:
        results = (
            session.query(
                func.min(Measurement.tobs), 
                func.avg(Measurement.tobs), 
                func.max(Measurement.tobs),
            )
            .filter(Measurement.date >= start)
            .filter(Measurement.date <= end)
            .all()
        )

    temp_data = {
        "Min Temperature": results[0][0],
        "Avg Temperature": results[0][1],
        "Max Temperature": results[0][2],
    }

    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)
