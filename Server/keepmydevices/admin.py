from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose

from flask import redirect, request, url_for

from keepmydevices import app
from keepmydevices import db
from models import Device, User, Role

from flask_security import logout_user
from flask_security import current_user


class DeviceAdmin(ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# class LogoutView(BaseView):
#     @expose('/')
#     def index(self):
#         logout_user()
#         return redirect('/admin')
#
#     def is_visible(self):
#         return current_user.is_authenticated
#
#
# class LoginView(BaseView):
#     @expose('/')
#     def index(self):
#         logout_user()
#         return redirect('/login?next=/admin')
#
#     def is_visible(self):
#         return not current_user.is_authenticated

def init_admin():
    admin = Admin(app, name='keepmydevices', template_mode='bootstrap3')
    admin.add_view(DeviceAdmin(Device, db.session))
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Role, db.session))

