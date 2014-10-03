from flask import Flask, redirect, render_template_string, request, url_for
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'               # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    USER_PRODUCT_NAME           = "ProductName"     # Used by email templates
    USER_ENABLE_USERNAME        = True              # Register and Login with username
    USER_ENABLE_EMAIL           = True              # Register and Login with email
    USER_LOGIN_TEMPLATE         = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE      = 'flask_user/login_or_register.html'
    USER_AFTER_LOGIN_ENDPOINT   = 'profile_page'
    USER_AFTER_CONFIRM_ENDPOINT = 'profile_page'

    USER_ENABLE_CONFIRM_EMAIL = False

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
        language = request.accept_languages.best_match(translations)
        print('translations=',repr(translations), 'language=', repr(language))
        return language

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Home Page{%endtrans%}</h2>
                {% if current_user.is_authenticated() %}
                <p> <a href="{{ url_for('profile_page') }}">
                    {%trans%}Profile Page{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
                {% else %}
                <p> <a href="{{ url_for('user.login') }}">
                    {%trans%}Sign in or Register{%endtrans%}</a></p>
                {% endif %}
            {% endblock %}
            """)
        if current_user.is_authenticated():
            return redirect(url_for('profile_page'))
        else:
            return redirect(url_for('user.login'))

# The Profile page requires a logged-in user
    @app.route('/profile')
    @login_required                                 # Use of @login_required decorator
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Profile Page{%endtrans%}</h2>
                <p> {%trans%}Hello{%endtrans%}
                    {{ current_user.username or current_user.email }},</p>
                <p> <a href="{{ url_for('home_page') }}">
                    {%trans%}Home Page{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_username') }}">
                    {%trans%}Change username{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_password') }}">
                    {%trans%}Change password{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

