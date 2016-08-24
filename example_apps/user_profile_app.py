import os
from flask import Flask, render_template_string, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask_user import roles_required


# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///single_file_app.sqlite')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "AppName"                # Used by email templates


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
    mail = Mail(app)                                # Initialize Flask-Mail
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy

    # Define User model. Make sure to add flask_user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        user_profile_id = db.Column(db.Integer(), db.ForeignKey('user_profile.id', ondelete='CASCADE'))

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # Relationships
        user_profile = db.relationship('UserProfile', uselist=False, foreign_keys=[user_profile_id])

    class UserProfile(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        # User information
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name = db.Column(db.String(50), nullable=False, default='')

        # Relationships
        roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))

    # Define Role model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define UserRoles model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_profile_id = db.Column(db.Integer(), db.ForeignKey('user_profile.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    # Reset all the database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User, UserProfileClass=UserProfile)
    user_manager = UserManager(db_adapter, app)

    # Create 'user007' user with 'secret' and 'agent' roles
    if not User.query.filter(User.username=='user007').first():
        user_profile1 = UserProfile(first_name='James', last_name='Bond')
        db.session.add(user_profile1)
        user1 = User(user_profile=user_profile1, username='user007',
                email='user007@example.com', password=user_manager.hash_password('Password1'),
                active=True)
        db.session.add(user1)
        user_profile1.roles.append(Role(name='secret'))
        user_profile1.roles.append(Role(name='agent'))
        db.session.commit()

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
                <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
            {% endblock %}
            """)

    # The Members page is only accessible to authenticated users
    @app.route('/members')
    @login_required                                 # Use of @login_required decorator
    def members_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
                <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
            {% endblock %}
            """)

    # The Special page requires a user with 'special' and 'sauce' roles or with 'special' and 'agent' roles.
    @app.route('/special')
    @roles_required('secret', ['sauce', 'agent'])   # Use of @roles_required decorator
    def special_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Special Page</h2>
                <p>This page can only be accessed by user007.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
                <p><a href={{ url_for('special_page') }}>Special page</a> (login with username 'user007' and password 'Password1')</p>
            {% endblock %}
            """)

    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
