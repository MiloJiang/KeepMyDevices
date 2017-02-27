from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand

from keepmydevices import app, db, models
from werkzeug.security import generate_password_hash


class CreateAdmin(Command):

    def run(self):
        admin = models.User.query.filter_by(login='admin').first()
        if not admin:
            admin = models.User(login="admin", password=generate_password_hash("admin"))
            db.session.add(admin)
            db.session.commit()
            print("User added...Done!")
        else:
            print("User already exists!")


def init_commands():
    app.migrate = Migrate(app, db)
    app.manager = Manager(app)
    app.manager.add_command('db', MigrateCommand)
    app.manager.add_command('init', CreateAdmin)
