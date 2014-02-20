from flask import render_template

from example_app import app

@app.route('/')
def home():
    return render_template('example_app/home.html', app=app)