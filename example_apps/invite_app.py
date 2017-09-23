import os
from flask import Flask, redirect, render_template_string, request, url_for
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import confirmed_email_required, utils, login_required, \
                        UserManager, UserMixin
from flask_user.signals import user_sent_invitation, user_registered

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///test_app.sqlite')
    CSRF_ENABLED = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =            os.getenv('MAIL_USE_SSL',         True)

    # Flask-User settings
    USER_APP_NAME        = "AppName"                # Used by email templates
    USER_ENABLE_INVITE_USER = True
    USER_REQUIRE_INVITATION = True

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except ImportError: pass

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Initialize Flask extensions
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    babel = Babel(app)                              # Initialize Flask-BabelEx
    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        language = request.accept_languages.best_match(translations)
        return language

    # Define the User data-model. Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        username = db.Column(db.String(50), nullable=True, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User email information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime(), nullable=True)

        # User information
        is_enabled = db.Column(db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    class UserInvitation(db.Model):
        __tablename__ = 'user_invitations'
        id = db.Column(db.Integer, primary_key=True)
        # UserInvitation email information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255, collation='NOCASE'), nullable=False)
        # save the user of the invitee
        invited_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User, UserInvitationClass=UserInvitation)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    @user_registered.connect_via(app)
    def after_registered_hook(sender, user, user_invitation):
        sender.logger.info("USER REGISTERED")

    @user_sent_invitation.connect_via(app)
    def after_invitation_hook(sender, **extra):
        sender.logger.info("USER SENT INVITATION")

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Home Pages{%endtrans%}</h2>
                {% if call_or_get(current_user.is_authenticated) %}
                <p> <a href="{{ url_for('user_profile_page') }}">
                    {%trans%}Profile Page{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
                {% else %}
                <p> <a href="{{ url_for('user.login') }}">
                    {%trans%}Sign in or Register{%endtrans%}</a></p>
                {% endif %}
            {% endblock %}
            """)
        user_manager = current_app.user_manager
        if user_manager.call_or_get(current_user.is_authenticated):
            return redirect(url_for('user_profile_page'))
        else:
            return redirect(url_for('user.login'))

    # The Profile page requires a logged-in user
    @app.route('/user/profiles')
    @login_required                                 # Use of @login_required decorator
    @confirmed_email_required
    def user_profile_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
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
                <p> <a href="{{ url_for('user.invite_user') }}">
                    {%trans%}Invite User{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

