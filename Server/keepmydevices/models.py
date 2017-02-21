from keepmydevices import db
from flask_sqlalchemy import orm

from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Device(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    sn      = db.Column(db.String(80), unique=True)
    brand   = db.Column(db.String(80))
    model   = db.Column(db.String(120))
    latitude    = db.Column(db.Float)
    longitude   = db.Column(db.Float)
    timestamp   = db.Column(db.TIMESTAMP, default=datetime.now())

    @orm.validates('sn')
    def validate_sn(self, key, value):
        assert value != ''
        return value

    def __repr__(self):
        return '<Device %s: [%s] [%s]>' % (self.sn, self.brand, self.model)