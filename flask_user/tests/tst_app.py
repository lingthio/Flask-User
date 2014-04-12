from flask import Flask, render_template_string, request
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask.ext.user import roles_required

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'                        # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///roles_required_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    USER_ENABLE_USERNAME        = True              # Register and Login with username
    USER_ENABLE_EMAIL           = True              # Register with email
    USER_ENABLE_CONFIRM_EMAIL   = True              # Require email confirmation
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_FORGOT_PASSWORD = True

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
        return request.accept_languages.best_match(['en', 'nl'])

    # Define the User-Roles pivot table
    user_roles = db.Table('user_roles',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))

    # Define Role model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=True, unique=True)
        email = db.Column(db.String(255), nullable=True, unique=True)
        confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, default='')
        reset_password_token = db.Column(db.String(100), nullable=False, default='')
        # Relationships
        roles = db.relationship('Role', secondary=user_roles,
                backref=db.backref('users', lazy='dynamic'))

    # Reset all the database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)
    user_manager = UserManager(db_adapter, app)

    # Create 'user007' user with 'secret' and 'agent' roles
    if not User.query.filter(User.username=='user007').first():
        user1 = User(username='user007', email='user007@example.com', active=True,
                password=user_manager.hash_password('Password1'))
        user1.roles.append(Role(name='secret'))
        user1.roles.append(Role(name='agent'))
        db.session.add(user1)
        db.session.commit()

    # The '/' page is accessible to anyone
    @app.route('/')
    def home_page():
        # if current_user.is_authenticated():
        #     return profile_page()
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
            <h2>{%trans%}Home Page{%endtrans%}</h2>
            <p><a href="{{ url_for('user.login') }}">{%trans%}Sign in{%endtrans%}</a></p>
            {% endblock %}
            """)

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
            <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    # The '/special' page requires a user that has the 'special' AND ('sauce' OR 'agent') role.
    @app.route('/special')
    @roles_required('secret', ['sauce', 'agent'])   # Use of @roles_required decorator
    def special_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
            <h2>{%trans%}Special Page{%endtrans%}</h2>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
