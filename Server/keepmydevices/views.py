from keepmydevices import app
from flask import render_template
from flask import redirect, url_for, request

@app.route("/")
def hello():
    # return render_template("main.html")
    return redirect(url_for('admin.login_view', next=request.url))

