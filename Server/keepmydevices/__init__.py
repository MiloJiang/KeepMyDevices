from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security
from flask_restless import APIManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '\xc6\xed\x85\x99\xe9\xb3\xf2\xf1\xad\xed\x98\xc5\xb6=Zi\xbf\x9f\x05\xa2\xe0\xeb\xa7\xfe'
db = SQLAlchemy(app)

## Migrate
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

import keepmydevices.views
from .models import Device, user_datastore

## Security
security = Security(app, user_datastore)
app.config['SECURITY_LOGIN_URL'] = "/login/"
app.config['SECURITY_URL_PREFIX'] = "/admin"

## Restful API
api_mgr = APIManager(app, flask_sqlalchemy_db=db)

from admin import init_admin
init_admin()

api_mgr.create_api(Device, methods=['GET', 'POST', 'DELETE'])
