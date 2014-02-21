from flask import redirect, render_template, url_for
from flask.ext.login import current_user, login_required

from example_app import app

@app.route('/')
def home():
    if current_user.is_authenticated():
        return render_template('example_app/home.html', app=app)
    else:
        return redirect(url_for('user.login'))
