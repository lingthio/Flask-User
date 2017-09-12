# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_user import login_required, UserManager, UserMixin
from flywheel import Model, Field, GlobalIndex
from flask_flywheel import Flywheel
from datetime import datetime


# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"MyApp" <noreply@example.com>')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

    # Flask-User settings
    USER_APP_NAME = "AppName"  # Used by email templates


def create_app():
    """ Flask application factory """

    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    # Initialize Flask extensions
    db = Flywheel(app)  # Initialize Flask-Flywheel
    mail = Mail(app)  # Initialize Flask-Mail

    # Define the User data model. Make sure to add flask_user UserMixin !!!
    class User(Model, UserMixin):
        __metadata__ = {
            "_name": "users",
            'global_indexes': [
                GlobalIndex.keys('email-index', 'email').throughput(read=2, write=2)
            ],
        }

        id = Field(hash_key=True)

        # User authentication information
        username = Field(hash_key=True)
        password = Field()

        # User email information
        email = Field()
        email_confirmed_at = Field(data_type=datetime)

        # User information
        active = Field(data_type=bool)
        first_name = Field()
        last_name = Field()

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.engine.register(User)
    print('create_schema()')
    db.engine.create_schema()
    print('created_schema()')

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

    # The Members page is only accessible to authenticated users
    @app.route('/members')
    @login_required  # Use of @login_required decorator
    def members_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
