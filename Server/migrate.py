from keepmydevices import app
from keepmydevices import db
from keepmydevices.models import User
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    app.manager.run()

    # ## Add admin
    # admin = User.query.filter_by(login='admin').first()
    # if not admin:
    #     admin = User(login="admin", password=generate_password_hash("admin"))
    #     db.session.add(admin)
    #     db.session.commit()