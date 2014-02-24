# -*- coding: utf-8 -*-

import os

from flask import Flask, current_app, request
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import UserManager, SQLAlchemyAdapter

from example_app.database import db

app = None

def create_app(config=None):
    global app

    # Setup Flask
    app = Flask(__name__)
    app.config.from_object('example_app.settings')

    # Load env_settings.py if file exists
    filename = os.path.join(app.root_path, 'env_settings.py')
    if os.path.exists(filename):
        app.config.from_object('example_app.env_settings')

    # Over-write app config with specified config settings
    if config:
        for key, value in config.iteritems():
            app.config[key] = value

    # Setup Flask-Mail
    app.mail = Mail(app)

    # Setup Flask-Babel
    app.babel = Babel(app)

    @app.babel.localeselector
    def get_locale():
        # Get list of translated Locale objects
        locales = current_app.babel.list_translations()
        # Convert list of Locale objects to list of language codes
        languages = []
        for locale in locales:
            languages.append(str(locale))
        # Return best match language code
        language = request.accept_languages.best_match(languages)
        return language


    # Setup Flask-SQLAlchemy
    db.init_app(app)
    db.app = app                                # This trick only works if there's only one app

    from models import User
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)
    user_manager = UserManager(db_adapter, app)

    # Import views to run all the @app.route() decorators
    from example_app import views

    return app


