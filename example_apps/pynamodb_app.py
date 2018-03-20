# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import os
import uuid

from flask import Flask, render_template_string
from flask_mail import Mail
from flask_user import login_required, UserManager, UserMixin
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute


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
    db = None
    mail = Mail(app)  # Initialize Flask-Mail

    # Define the User data model. Make sure to add flask_user UserMixin !!!
    class UsernameIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        username = UnicodeAttribute(hash_key=True)

    class EmailIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        email = UnicodeAttribute(hash_key=True)

    class User(Model, UserMixin):
        class Meta:
            table_name = 'users'

        id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid1()))
        active = BooleanAttribute()

        # User authentication information
        username = UnicodeAttribute(null=True)
        password = UnicodeAttribute(null=True)

        username_index = UsernameIndex()

        # User email information
        email = UnicodeAttribute(null=True)
        email_confirmed_at = UTCDateTimeAttribute(null=True)

        email_index = EmailIndex()

        # User information
        first_name = UnicodeAttribute(null=True)
        last_name = UnicodeAttribute(null=True)


    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Create all database tables
    print('create_schema()')
    user_manager.db_manager.create_all_tables()
    print('created_schema()')

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
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
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

    return app


# Start development web server
app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
