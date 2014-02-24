=====================
 Username Application
=====================
The ``Username Application`` extends the :doc:`minimal-app` by enabling ``USER_LOGIN_WITH_USERNAME``,
adding email config, and enabling ``USER_ENABLE_CHANGE_USERNAME`` and ``USER_ENABLE_FORGOT_PASSWORD``.

**Features:**

* Register with username and email
* Confirm email
* Login with username
* Logout
* Change username
* Change password
* Reset forgotten password

Set up environment
------------------
We recommend working with virtualenv and virtualenvwrapper::

    mkvirtualenv my_env
    workon my_env
    pip install flask-user

    mkdir -p ~dev/example       # or C:\dev\example on Windows
    cd ~/dev/example

Collect SMTP Information
------------------------
The ``Confirm Email`` and ``Reset forgotten password`` features
require an SMTP server to be configured.
Please collect the following information::

    - MAIL_SERVER:                  # e.g. 'smtp.gmail.com'
    - MAIL_PORT:                    # e.g. 465
    - Whether to use SSL or TLS     # e.g. MAIL_SSL = True
    - MAIL_USERNAME:                # e.g. 'noreply@example.com'
    - MAIL_PASSWORD:                # e.g. 'password'
    - MAIL_DEFAULT_SENDER:          # e.g. '"Website" <noreply@example.com'


Create username_app.py
----------------------

Create ~/dev/example/username_app.py with the content below.

Make sure to adjust the SMTP settings below to the correct SMTP server settings and credentials.

::

    import os

    from flask import Flask, render_template_string
    from flask.ext.babel import Babel
    from flask.ext.mail import Mail
    from flask.ext.sqlalchemy import SQLAlchemy
    from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter

    # Setup Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///username_app.db'

    # Configure Flask-User
    app.config['USER_ENABLE_CHANGE_USERNAME'] = True
    app.config['USER_ENABLE_CHANGE_PASSWORD'] = True
    app.config['USER_ENABLE_CONFIRM_EMAIL']   = True
    app.config['USER_ENABLE_FORGOT_PASSWORD'] = True
    app.config['USER_LOGIN_WITH_USERNAME']    = True

    # Configure Flask-Mail SMTP Settings
    app.config['MAIL_SERVER']         = 'smtp.gmail.com'                    # Change this!!
    app.config['MAIL_PORT']           = 465
    app.config['MAIL_USE_SSL']        = True
    app.config['MAIL_USERNAME']       = 'user@example.com'                  # Change this!!
    app.config['MAIL_PASSWORD']       = 'password'                          # Change this!!
    app.config['MAIL_DEFAULT_SENDER'] = '"Flask.User" <noreply@example.com' # Change this!!

    # Load local_settings.py if file exists
    filename = os.path.join(app.root_path, 'local_settings.py')
    if os.path.exists(filename):
        app.config.from_object('local_settings')

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = Babel(app)
    db = SQLAlchemy(app)

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

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Home page
    @app.route('/')
    def home():
        return render_template_string(
    """
    {% extends "base.html" %}

    {% block content %}
        {% if not current_user.is_authenticated() %}
            <p>{%trans%}Hello Visitor,{%endtrans%}</p>
            <p><a href="{{ url_for('user.login') }}">{%trans%}Sign in{%endtrans%}</a></p>
            <p><a href="{{ url_for('user.register') }}">{%trans%}Register{%endtrans%}</a></p>
            <p><a href="{{ url_for('user.forgot_password') }}">{%trans%}Forgot password?{%endtrans%}</a></p>
        {% else %}
            <p>{%trans%}Hello{%endtrans%} {{ current_user.username or current_user.email }},</p>
            <p><a href="{{ url_for('user.change_username') }}">{%trans%}Change username{%endtrans%}</a></p>
            <p><a href="{{ url_for('user.change_password') }}">{%trans%}Change password{%endtrans%}</a></p>
            <p><a href="{{ url_for('user.logout') }}">{%trans%}Sign out{%endtrans%}</a></p>
        {% endif %}
    {% endblock %}
    """)

    # Start development web server
    app.run(host='0.0.0.0', port=5000, debug=True)

Run the username app
--------------------
Run the username app with the following command::

    python username_app.py

And point your browser to ``http://localhost:5000``.

If you receive an EmailException error message,
of if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

