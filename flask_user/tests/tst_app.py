import os
import datetime
from flask import Flask, render_template_string, request
from flask_user import login_required, roles_required, UserManager, UserMixin

ORM_type = 'SQLAlchemy'   # SQLAlchemy  or MongoEngine
# ORM_type = 'MongoEngine'   # SQLAlchemy  or MongoEngine

# Use "mongod -dbpath ~/mongodb/data/db" to start the MongoDB deamon

app = Flask(__name__)

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tst_app.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'tst_app',
        'host': 'mongodb://localhost:27017/tst_app'
    }

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =            os.getenv('MAIL_USE_SSL',         True)

    USER_APP_NAME = 'Test App'
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = 'noreply@example.com'

# Read config from ConfigClass defined above
app.config.from_object(__name__+'.ConfigClass')

if ORM_type=='SQLAlchemy':
    # Initialize Flask-SQLAlchemy, using SQLALCHEMY_DATABASE_URI setting
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)

    # Define the User data-model. Make sure to add flask_user UserMixin!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)

        # User authentication information
        username = db.Column(db.String(50), nullable=True, unique=True)
        email = db.Column(db.String(255), nullable=True, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

        # Relationships
        roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))

    # Define UserEmail DataModel.
    class UserEmail(db.Model):
        __tablename__ = 'user_emails'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        # User email information
        email = db.Column(db.String(255), nullable=True, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, default=False)

        # Relationship
        user = db.relationship('User', uselist=False)

    class UserInvitation(db.Model):
        __tablename__ = 'user_invitations'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), nullable=False)
        # save the user of the invitee
        invited_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        # token used for registration page to identify user registering
        token = db.Column(db.String(100), nullable=False, server_default='')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles data-model
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


if ORM_type == 'MongoEngine':
    # Initialize Flask-MongoEngine, using MONGODB_SETTINGS setting
    from flask_mongoengine import MongoEngine

    db = MongoEngine(app)

    # Define the User document.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):

        # User authentication information
        username = db.StringField(default='')
        email = db.StringField(default='')
        password = db.StringField()
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        # roles = ListField(StringField(), required=False, default_empty=True)
        roles = db.ListField(db.StringField(), default=[])


# Define custom UserManager class
class CustomUserManager(UserManager):
    # Customize settings
    def __init__(self, *args, **kwargs):
        super(CustomUserManager, self).__init__(*args, **kwargs)
        self.APP_NAME = "CustomAppName"
        self.ENABLE_EMAIL = True
        self.ENABLE_INVITATION = True


def init_app(app, test_config=None):                # For automated tests
    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except ImportError: pass

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Setup Flask-User
    if ORM_type == 'SQLAlchemy':
        RoleClass = Role
        user_manager = CustomUserManager(app, db, User, UserInvitationClass=UserInvitation, RoleClass=RoleClass)
    else:
        RoleClass = None
        user_manager = CustomUserManager(app, db, User, RoleClass=RoleClass)

    # Reset database by dropping, then creating all tables
    db_adapter = user_manager.db_adapter
    db_adapter.drop_all_tables()
    db_adapter.create_all_tables()

    # For debugging purposes
    token = user_manager.token_manager.generate_token('abc', 123, 'xyz')
    data_items = user_manager.token_manager.verify_token(token, 3600)
    assert data_items is not None
    assert data_items[0] == 'abc'
    assert data_items[1] == 123
    assert data_items[2] == 'xyz'

    # Create regular 'member' user
    user = db_adapter.add_object(User, username='member', email='member@example.com',
            password=user_manager.password_manager.hash_password('Password1'), email_confirmed_at=datetime.datetime.utcnow())
    db_adapter.commit()

    # Create 'user007' user with 'secret' and 'agent' roles
    user = db_adapter.add_object(User, username='user007', email='admin@example.com',
            password=user_manager.password_manager.hash_password('Password1'))
    db_adapter.add_user_role(user, 'secret', RoleClass=RoleClass)
    db_adapter.add_user_role(user, 'agent', RoleClass=RoleClass)
    db_adapter.commit()

    # The '/' page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
            <h2>{%trans%}Home Page{%endtrans%}</h2>
            <p><a href="{{ url_for('user.login') }}">{%trans%}Sign in{%endtrans%}</a></p>
            {% endblock %}
                """)

    # The '/profile' page requires a logged-in user
    @app.route('/user/profile')
    @login_required                                 # Use of @login_required decorator
    def user_profile_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
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

    # The '/special' page requires a user that has the 'secret' AND ('sauce' OR 'agent') role.
    @app.route('/special')
    @roles_required('secret', ['sauce', 'agent'])   # Use of @roles_required decorator
    def admin_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
            <h2>{%trans%}Admin Page{%endtrans%}</h2>
            {% endblock %}
            """)

    # For testing only
    app.db = db
    if ORM_type == 'SQLAlchemy':
        app.UserEmailClass = UserEmail

    return app


# Start development web server
if __name__=='__main__':
    app = init_app(app)
    app.run(host='0.0.0.0', port=5555, debug=True)
