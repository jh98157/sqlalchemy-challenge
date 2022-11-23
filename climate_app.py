import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)

Measurement= Base.classes.measurement
Station= Base.classes.station

session=Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my Climate App!<br/>"
        f"Here are the available routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end_date<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = dt.date(2017, 8 ,23)
    year_before = recent_date - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= recent_date)
                .filter(Measurement.date >= year_before)
                .order_by(Measurement.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)
session.close()

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())
session.close()

@app.route('/api/v1.0/tobs') 
def tobs():  
    recent_date = dt.date(2017, 8 ,23)
    year_before = recent_date - dt.timedelta(days=365)

    lastyear = (session.query(Measurement.date,Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= recent_date)
                .filter(Measurement.date >= year_before)
                .order_by(Measurement.date).all())
    temps=list(np.ravel(lastyear))
    return jsonify(temps=temps)
session.close()

@app.route('/api/v1.0/start_date') 
def start():  
    start_date = dt.date(2016, 8 ,23)
    start_temp = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
                .filter(Measurement.date >= start_date).all())
    temps=list(np.ravel(start_temp))
    return jsonify(temps=temps)

session.close()

@app.route('/api/v1.0/start_end_date')
def start_end():  
    start_date = dt.date(2016, 8 ,23)
    end_date=dt.date(2018,1,1)
    start_temp = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
                .filter(Measurement.date >= start_date)
                .filter(Measurement.date <= end_date)
                .order_by(Measurement.date).all())
    temps=list(np.ravel(start_temp))
    return jsonify(temps=temps)

session.close()

if __name__ == "__main__":
    # debug mode (disable in production) 
    app.run(debug=True)