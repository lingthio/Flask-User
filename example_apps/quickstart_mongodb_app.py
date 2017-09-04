# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)
# - Placing everything in one file

from flask import Flask, render_template_string
from flask_mongoalchemy import MongoAlchemy
from flask_user import login_required, UserManager, UserMixin


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app.sqlite'    # File-based SQL database

    # Flask-MongoAlchemy settings
    MONGOALCHEMY_DATABASE = 'flask_user_quickstart_db'

    # Flask-Mail settings
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '“Sender” <noreply@example.com>'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    # Flask-User settings
    USER_APP_NAME = "Flask-User QuickStart App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication

    # For debugging purposes
    USER_SEND_PASSWORD_CHANGED_EMAIL=False
    USER_SEND_REGISTERED_EMAIL=False
    USER_SEND_USERNAME_CHANGED_EMAIL=False
    USER_ENABLE_CONFIRM_EMAIL=False


def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize MongoDB
    db = MongoAlchemy(app)

    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):
        # Map MongoAlchemy's mongod_id to Flask-User's id - getter
        @property
        def id(self):
            # Convert MongoDB hexadecimal string to Flask-User Integer
            id = int(str(self.mongo_id), 16)
            return id

        # # Map MongoDB's _id to Flask-User's id - setter
        # @id.setter
        # def id(self, value):
        #     # Convert Flask-User Integer to MongoDB hexadecimal string
        #     self._id = format(value, 'x')

        # User authentication information
        email = db.StringField(default='')
        password = db.StringField(default='')
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # # For debugging only
    # id = 12345
    # encrypted_id = user_manager._encrypt_id(id)
    # decrypted_id = user_manager._decrypt_id(encrypted_id)
    # if id!=decrypted_id:
    #     a = 'something went wrong'

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required    # User must be authenticated
    def members_page():
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """)

    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

