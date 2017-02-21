from flask_restless import APIManager
from keepmydevices import app, db
from models import Device, User

from flask_jwt import JWT, jwt_required
from werkzeug.security import check_password_hash


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
                       methods=['GET', 'POST', 'DELETE'],
                       url_prefix='/api/v1',
                       preprocessors=dict(GET_SINGLE=[protected], GET_MANY=[protected]),
                       include_columns=['id', 'sn', 'brand', 'model', 'latitude', 'longitude'])
