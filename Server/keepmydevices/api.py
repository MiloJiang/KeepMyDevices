from datetime import datetime

from flask_restless import APIManager
from keepmydevices import app, db
from models import Device, User

from flask_jwt import JWT, jwt_required
from werkzeug.security import check_password_hash
from flask import request, json, abort, jsonify


def authenticate(username, password):
    user = User.query.filter(User.login == username).scalar()
    if user and check_password_hash(user.password, password):
        return user
    return None


def identity(payload):
    return User.query.filter(User.id == payload['identity']).scalar()
    # return User.query.filter(User.login == "admin").first()

jwt = JWT(app, authenticate, identity)


@jwt_required()
def protected(**kw):
    pass


def init_api():
    api_mgr = APIManager(app, flask_sqlalchemy_db=db)
    api_mgr.create_api(Device,
                       methods=['GET', 'POST', 'PUT'],
                       url_prefix='/api/v1',
                       preprocessors=dict(GET_SINGLE=[protected], GET_MANY=[protected]),
                       include_columns=['id', 'sn', 'brand', 'model', 'latitude', 'longitude'],
                       primary_key='sn')


# Customize API
@app.route("/api/v1/update", methods=['GET', 'POST'])
@jwt_required()
def update_device():
    if request.method == 'POST':
        info = request.json
        if not info['sn']:
            abort(400)
        device = Device.query.filter(Device.sn == info['sn']).scalar()

        if device:
            app.logger.debug("Device already exists!")
            device.latitude = info.get('latitude')
            device.longitude = info.get('longitude')
            device.timestamp = datetime.now()
        else:
            app.logger.debug("Device doesn't exist!")
            device = Device(sn=info['sn'])
            device.brand = info.get('brand')
            device.model = info.get('model')
            device.latitude = info.get('latitude')
            device.longitude = info.get('longitude')

        device.timestamp = datetime.now()
        db.session.add(device)
        db.session.commit()
        return jsonify(device.to_json())

    else:
        return "Please use 'post' method!"
