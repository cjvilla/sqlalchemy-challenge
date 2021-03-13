from flask import Flask, jsonify
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
#
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to my Routes!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    precipt = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    session.close()
    
    precipt_list = list(np.ravel(precipt))
    precipt_list = {precipt_list[i]: precipt_list[i + 1] for i in range(0, len(precipt_list), 2)} 
    return jsonify(precipt_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).order_by(Station.station).all()
    session.close()

    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temps = session.query(Measurement.date,  Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()

    temp_list = list(np.ravel(temps))
    temp_list = {temp_list[i]: temp_list[i + 1] for i in range(0, len(temp_list), 2)} 

    return jsonify(temp_list)

@app.route("/api/v1.0/<start_date>")
def data_start_date(start_date):
    session = Session(engine)
    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    start_list = []
    for min, avg, max in start:
        start_dict = {}
        start_dict["min_temp"] = min
        start_dict["avg_temp"] = avg
        start_dict["max_temp"] = max
        start_list.append(start_dict) 
    
    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def data_start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    start_end_list = []
    for min, avg, max in end:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end_list.append(start_end_dict) 
    

    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)