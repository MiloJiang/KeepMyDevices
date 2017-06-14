from keepmydevices import app
from flask import render_template
# from flask_login import login_required

from .models import Device


@app.route("/")
def main():
    devices = Device.query.all()
    return render_template("main.html", devices=devices)

