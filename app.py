from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Fenrir_db
import time

# Connect to Database and create database session
engine = create_engine('sqlite:///fenrir_db.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
api functions
"""
def get_all_data():
    data = session.query(Fenrir_db).all()
    return jsonify(data=[d.serialize for d in data])


def get_round(round_id):
    round = session.query(Fenrir_db).filter_by(round_uuid=round_id)
    return jsonify(data=[c.serialize for c in round])

@app.route('/')
def index():
    data = session.query(Fenrir_db).all()
#    data = jsonify(data=[d.serialize for d in data])
    return render_template('index.html', posts=data)

def add_new_data(round_uuid, lap, lat, lon, vel, datetime, set, timeset, timelap):
    new_data = Fenrir_db(round_uuid = round_uuid, lap = lap, lat = lat, lon = lon, vel = vel, datetime = datetime, set = set, timeset = timeset, timelap = timelap)
    session.add(new_data)
    session.commit()
    return jsonify(data=new_data.serialize)

def delete_round(round_id):
    round = session.query(Fenrir_db).filter_by(round_uuid=round_id)
    for c in round:
        session.delete(c)
    session.commit()
    return 'round com uuid %s removida' % round_id
def get_newest_data():
    newest = session.query(Fenrir_db).order_by(Fenrir_db.id.desc()).first()
    return jsonify(data=newest.serialize)


# @app.route('/', methods=['GET'])
# @app.route('/FenrirApi', methods=['GET', 'POST'])
# def data_function():
#     if request.method == 'GET':
#         return get_all_data()
#     elif request.method == 'POST':
#         content = request.get_json()
#         return add_new_data(content['round_uuid'], content['lap'], content['lat'], content['lon'], content['vel'], time.time(), content['set'], content['timeset'], content['timelap'])
#


@app.route('/FenrirApi/<string:uuid>', methods=['GET', 'DELETE'])
def round_by_uuid(uuid):
    if request.method == 'GET':
        return get_round(uuid)

    elif request.method == 'DELETE':
        return delete_round(uuid)

@app.route('/FenrirApi/newest', methods=['GET'])
def newest_data():
    if request.method == 'GET':
        return get_newest_data()

if __name__ == '__main__':
    app.debug = True
    app.run()