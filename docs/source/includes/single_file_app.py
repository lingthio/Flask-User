from flask import Flask, redirect, render_template_string, request, url_for
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'                     # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///single_file_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead

def create_app():
    """ Flask application factory """
    
    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask extensions
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    # Define User model. Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <p><a href="{{ url_for('home_page') }}">Home page</a> |
                   <a href="{{ url_for('profile_page') }}">Profile page</a></p>

                <h2>Home page</h2>

                {% if current_user.is_authenticated() %}
                    <p><a href="{{ url_for('user.logout')  }}">Sign out</a></p>
                {% else %}
                    <p><a href="{{ url_for('user.login') }}">Sign in</a></p>
                {% endif %}
            {% endblock %}
            """)

    # The Profile page requires a logged-in user
    @app.route('/profile')
    @login_required                                 # Use of @login_required decorator
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <p><a href="{{ url_for('home_page') }}">Home page</a> |
                   <a href="{{ url_for('profile_page') }}">Profile page</a></p>

                <h2>Profile page</h2>

                <p>Username: {{ current_user.username }}</p>
                <p>Email:    {{ current_user.email }}   </p>

                <p><a href="{{ url_for('user.change_username') }}">Change username</a></p>
                <p><a href="{{ url_for('user.change_password') }}">Change password</a></p>
                <p><a href="{{ url_for('user.logout') }}">Sign out</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

