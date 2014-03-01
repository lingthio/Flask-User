from flask import Flask, render_template_string
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

from sqlalchemy.sql import func

def create_app(test_config=None):
    # Setup Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basic_app.db'

    # Configure Flask-Mail
    app.config['MAIL_SERVER']   = 'smtp.gmail.com'
    app.config['MAIL_PORT']     = 465
    app.config['MAIL_USE_SSL']  = True
    app.config['MAIL_USERNAME'] = 'noreply@example.com'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_DEFAULT_SENDER'] = '"Website" <noreply@example.com>'

    # Configure Flask-User
    app.config['USER_ENABLE_CHANGE_USERNAME'] = True
    app.config['USER_ENABLE_CHANGE_PASSWORD'] = True
    app.config['USER_ENABLE_CONFIRM_EMAIL']   = True
    app.config['USER_ENABLE_FORGOT_PASSWORD'] = True
    app.config['USER_LOGIN_WITH_USERNAME']    = True

    # Load local_settings.py if file exists
    try:
        app.config.from_object('local_settings')
    except:
        try:
            app.config.from_object('example_apps.local_settings')
        except:
            pass

    # Over-write app config with test_config settings when specified
    if test_config:
        key_value_pairs = test_config.items()
        for key_value_pair in key_value_pairs:
            app.config[key_value_pair[0]] = key_value_pair[1]

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = Babel(app)
    app.db = SQLAlchemy(app)
    db = app.db

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        # Required fields for Flask-Login
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)

        # Required fields for Flask-User
        email = db.Column(db.String(255), nullable=True, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')

        # Optional fields for Flask-User (depends on app config settings)
        username = db.Column(db.String(50), nullable=True, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

        # Additional application fields
        created_at = db.Column(db.DateTime, nullable=False, default=func.now())
        modified_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    app.User = User

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # User profile page
    @app.route('/')     # Mapped to the URL '/'
    @login_required     # Requires an authenticated user
    def profile():
        return render_template_string(
            """
            {% extends "base.html" %}

            {% block content %}
                <p>{%trans%}Hello{%endtrans%} {{ current_user.username or current_user.email }},</p>
                <p><a href="{{ url_for('user.change_username') }}">{%trans%}Change username{%endtrans%}</a></p>
                <p><a href="{{ url_for('user.change_password') }}">{%trans%}Change password{%endtrans%}</a></p>
                <p><a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

