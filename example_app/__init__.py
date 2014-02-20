# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import UserMixin
from flask_user import UserManager, SQLAlchemyAdapter

from example_app.database import db

app = None

def create_app(config=None):
    global app

    # Setup Flask
    app = Flask(__name__)
    app.config.from_object('example_app.settings')
    app.config.from_object('example_app.env_settings')

    # Over-write app config with specified config settings
    if config:
        for key, value in config.iteritems():
            app.config[key] = value

    # Setup Flask-SQLAlchemy
    db.init_app(app)
    db.app = app
    from models import User
    db.create_all()

    # Setup Flask-Account
    db_adapter = SQLAlchemyAdapter(db,  User)
    user_manager = UserManager(db_adapter)
    user_manager.init_app(app)

    # Import views to run all the @app.route() decorators
    from example_app import views

    return app

# # Setup Flask-Babel
# from flask.ext.babel import Babel
# babel = Babel(app)
# LANGUAGES = {
#     'en': 'English',
#     'nl': 'Nederlands'
# }
# @babel.localeselector
# def get_locale():
#     locale = request.accept_languages.best_match(LANGUAGES.keys())
#     return locale

