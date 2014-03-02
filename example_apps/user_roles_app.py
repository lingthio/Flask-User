from flask import Flask, render_template_string
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import login_required, roles_required, SQLAlchemyAdapter, UserManager, UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()


# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'           # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user_roles_app.db'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Change this to test Confirm email and Forgot password!
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                 # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    USER_LOGIN_WITH_USERNAME    = True
    USER_REGISTER_WITH_EMAIL    = True
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_CONFIRM_EMAIL   = True
    USER_ENABLE_FORGOT_PASSWORD = True

def create_app(test_config=None):
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists
    try: app.config.from_object('local_settings')
    except: pass

    # Over-write app config with test_config settings when specified
    if test_config:
        for key, value in test_config.items():
            app.config[key] = value

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = Babel(app)
    app.db = db = SQLAlchemy(app)

    # Define the User-Roles pivot table
    user_roles = db.Table('user_roles',
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        username = db.Column(db.String(50), nullable=True, unique=True)
        email = db.Column(db.String(255), nullable=True, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, default='')
        reset_password_token = db.Column(db.String(100), nullable=False, default='')
        # Relationships
        roles = db.relationship('Role', secondary=user_roles,
                backref=db.backref('users', lazy='dynamic'))
    app.User = User

    # Define Role model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Create all database tables
    db.drop_all()
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User, RoleClass=Role)
    user_manager = UserManager(db_adapter, app)

    # Create special user with special roles to access special_page
    role1 = Role(name='secret')
    role2 = Role(name='agent')
    # Create a user with both roles
    user1 = User(username='user007', email='user007@example.com',
            active=True,
            password=user_manager.password_crypt_context.encrypt('Password1'),
            )
    db.session.add(user1)
    user1.roles.append(role1)
    user1.roles.append(role2)
    db.session.commit()

    # For profile page, user must have logged in
    @app.route('/')     # Mapped to the URL '/'
    @login_required     # Requires an authenticated user
    def profile():
        return render_template_string(
            """
            {% extends "base.html" %}

            {% block content %}
                <h2>Profile Page</h2>
                <p>{%trans%}Hello{%endtrans%} {{ current_user.username or current_user.email }},</p>
                <p><a href="{{ url_for('user.change_username') }}">{%trans%}Change username{%endtrans%}</a></p>
                <p><a href="{{ url_for('user.change_password') }}">{%trans%}Change password{%endtrans%}</a></p>
                <p><a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    # For profile page, user must have logged in
    @app.route('/special')  # Route this URL
    @roles_required('secret', ['sauce', 'agent'])  # Requires 'special' and ('sauce' or 'agent')
    def special_page():
        return render_template_string(
            """
            {% extends "base.html" %}

            {% block content %}
                <h2>Special Page</h2>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
