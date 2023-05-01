# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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
def welcome():
    # List all available api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start?begin=YYYY-MM-DD<br/>"
        f"/api/v1.0/start_end?begin=YYYY-MM-DD&end=YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Precipitation in the last 12 months
    
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    precip_list = list(np.ravel(results))

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of all stations
    
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Temperature Observation in the last 12 months
  
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date >= '2016-08-23').\
              filter((Measurement.station) == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/start")
def start():
    start_date = request.args['begin']
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of minimum, maximum, and average temperatures for a date
   
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start_date).all()

    session.close()

    all_tobs = []
    for minimum, maximum, average in results:
        tobs_dict = {}
        tobs_dict["minimum"] = minimum
        tobs_dict["maximum"] = maximum
        tobs_dict["average"] = average
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start_end")
def start_end():
    start_date = request.args['begin']
    end_date = request.args['end']
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of minimum, maximum, and average temperatures for a date range
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start_date).\
              filter(Measurement.date <= end_date).all()

    session.close()

    all_tobs = []
    for minimum, maximum, average in results:
        tobs_dict = {}
        tobs_dict["minimum"] = minimum
        tobs_dict["maximum"] = maximum
        tobs_dict["average"] = average
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)
    

