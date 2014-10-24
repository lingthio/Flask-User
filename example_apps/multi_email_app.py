import os
from flask import Flask, redirect, render_template_string, request, url_for
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'                     # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///multi_email_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_USERNAME       = os.getenv('MAIL_USERNAME', 'email@example.com')
    MAIL_PASSWORD       = os.getenv('MAIL_PASSWORD', 'password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"Sender" <noreply@example.com>')
    MAIL_SERVER         = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT           = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL        = os.getenv('MAIL_USE_SSL', True)

    # Configure Flask-User
    USER_APP_NAME          = "AppName"          # Used by email templates
    USER_ENABLE_USERNAME   = True                   # Register and Login with username
    USER_ENABLE_EMAIL      = True                   # Register and Login with email
    USER_LOGIN_TEMPLATE    = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'
    USER_AFTER_LOGIN_ENDPOINT   = 'user_profile_page'
    USER_AFTER_CONFIRM_ENDPOINT = 'user_profile_page'

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except: pass

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Initialize Flask extensions
    babel = Babel(app)                              # Initialize Flask-Babel
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        # Removed email field
        # Removed confirmed_at field
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # Define UserEmail model.
    class UserEmail(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, default=False)
        user = db.relationship("User", uselist=False)

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User,       # Select database adapter
            UserEmailClass=UserEmail)               # Allow Multiple Emails per User
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Display Login page or Profile page
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return redirect(url_for('user_profile_page'))
        else:
            return redirect(url_for('user.login'))

    # The '/profile' page requires a logged-in user
    @app.route('/profile')
    @login_required                                 # Use of @login_required decorator
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Profile Page{%endtrans%}</h2>
                <p> {%trans%}Hello{%endtrans%}
                    {{ current_user.username or current_user.email }},</p>
                <p> <a href="{{ url_for('user.change_username') }}">
                    {%trans%}Change username{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_password') }}">
                    {%trans%}Change password{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.manage_emails') }}">
                    {%trans%}Manage emails{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

