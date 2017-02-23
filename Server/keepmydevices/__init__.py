from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '\xc6\xed\x85\x99\xe9\xb3\xf2\xf1\xad\xed\x98\xc5\xb6=Zi\xbf\x9f\x05\xa2\xe0\xeb\xa7\xfe'
db = SQLAlchemy(app)

from commands import init_commands
import keepmydevices.views
from login import init_login
from admin import init_admin
from api import init_api

init_commands()
init_login()
init_admin()
init_api()

