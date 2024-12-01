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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
# Creating Homepage Route
@app.route("/")
def welcome ():
    """Listing all available API routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br>"
    )


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation data for the last 12 months and returning a JSON representation"""
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    """Querying precipitation data"""
    results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))
        .all()
    )

    """Converting results into a dictionary with date as key and precipitation as values"""
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    """Returning list of all stations as JSON representation"""
    results = session.query(Station.station).all()

    station_list = [station[0] for station in results]

    return jsonify(station_list)


# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    """Returning list of temperature observations for most active stations in the last year as JSON representation"""
    # Calculating the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Getting the most active station
    most_active_station = (
        session.query(Measurement.station, func.count(Measurement.station))
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .first()[0]
    )

    # Querying temperature observations for the most active station in the last year
    results = (
        session.query(Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))
        .all()
    )

    # Converting list of tuples into a flat list
    tobs_list = [temp[0] for temp in results]

    return jsonify(tobs_list)


# Start and end date route 
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start=None, end=None):
    """List of Min, Avg, and Max temps for given start or start-end range, and returning it as JSON"""
    # Query for min, avg, and max temps
    if not end:
        results = (
            session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
            .filter(Measurement.date >= start)
            .all()
        )
    else:
        results = (
            session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
            .filter(Measurement.date >= start)
            .filter(Measurement.date <= end)
            .all()
        )

    # Extract results and returning as JSON
    temp_data = {
        "Min Temperature": results[0][0],
        "Avg Temperature": results[0][1],
        "Max Temperature": results[0][2],
    }

    return jsonify(temp_data)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
