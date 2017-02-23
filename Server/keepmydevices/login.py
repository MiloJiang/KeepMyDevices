import flask_login
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash, generate_password_hash

from models import User
from keepmydevices import app, db


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

def init_login():
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    ## Add admin
    # admin = User.query.filter_by(login='admin').first()
    # if not admin:
    #     admin = User(login="admin", password=generate_password_hash("admin"))
    #     db.session.add(admin)
    #     db.session.commit()

    # Required by Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)