from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

## Migrate
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '\xc6\xed\x85\x99\xe9\xb3\xf2\xf1\xad\xed\x98\xc5\xb6=Zi\xbf\x9f\x05\xa2\xe0\xeb\xa7\xfe'
db = SQLAlchemy(app)

## Migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

## Admin
admin = Admin(app, name='keepmydevices', template_mode='bootstrap3')

# class Device(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sn = db.Column(db.String(80), unique=True)
#     brand = db.Column(db.String(80))
#     model = db.Column(db.String(120))

#     def __repr__(self):
#         return '<Device %s: [%s] [%s]>' % (self.sn, self.brand, self.model)

import keepmydevices.views

from .models import Device
from flask_admin.contrib.sqla import ModelView
admin.add_view(ModelView(Device, db.session))
