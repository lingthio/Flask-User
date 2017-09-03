import os
import datetime
from flask import Flask, render_template_string, request
from flask_babel import Babel
from flask_user import login_required, UserManager, UserMixin
from flask_user import roles_required, confirmed_email_required

ORM_type = 'SQLAlchemy'   # SQLAlchemy  or MongoAlchemy
# ORM_type = 'MongoAlchemy'   # SQLAlchemy  or MongoAlchemy
# Use "mongod -dbpath ~/mongodb/data/db" to start the MongoDB deamon

app = Flask(__name__)

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tst_app.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-MongoAlchemy settings
    MONGOALCHEMY_DATABASE = 'flask_user_tst_app_db'

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =            os.getenv('MAIL_USE_SSL',         True)

    # Disable email sending
    USER_SEND_PASSWORD_CHANGED_EMAIL=False
    USER_SEND_REGISTERED_EMAIL=False
    USER_SEND_USERNAME_CHANGED_EMAIL=False

# Read config from ConfigClass defined above
app.config.from_object(__name__+'.ConfigClass')

if ORM_type=='SQLAlchemy':
    # Initialize Flask-SQLAlchemy
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)

    # Define the User data model. Make sure to add flask_user UserMixin!!
    class User(db.Model, UserMixin):
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
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        # User email information
        email = db.Column(db.String(255), nullable=True, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, default=False)

        # Relationship
        user = db.relationship('User', uselist=False)

    class UserInvitation(db.Model):
        __tablename__ = 'user_invite'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), nullable=False)
        # save the user of the invitee
        invited_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        # token used for registration page to identify user registering
        token = db.Column(db.String(100), nullable=False, server_default='')

    # Define the Role data model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles data model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


if ORM_type == 'MongoAlchemy':
    # Initialize Flask-MongoAlchemy
    from flask_mongoalchemy import MongoAlchemy
    db = MongoAlchemy(app)


    # Define the User data model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):
        # Map MongoAlchemy's mongod_id to Flask-User's id - getter
        @property
        def id(self):
            # Convert MongoDB hexadecimal string to Flask-User Integer
            id = int(str(self.mongo_id), 16)
            return id

        # # Map MongoDB's _id to Flask-User's id - setter
        # @id.setter
        # def id(self, value):
        #     # Convert Flask-User Integer to MongoDB hexadecimal string
        #     self._id = format(value, 'x')

        # User authentication information
        username = db.StringField(default='')
        email = db.StringField(default='')
        password = db.StringField()
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), required=False, default=[])


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
    except: pass

    # Load optional test_config                     # For automated tests
    if test_config:
        app.config.update(test_config)

    # Initialize Flask extensions
    babel = Babel(app)                              # Initialize Flask-Babel

    # Reset all the database tables
    if ORM_type == 'SQLAlchemy':
        db.drop_all()
        db.create_all()

    if ORM_type == 'MongoAlchemy':
        # Drop existing table
        db.session.db.connection.drop_database(app.config.get('MONGOALCHEMY_DATABASE', ''))


    # Setup Flask-User
    if ORM_type == 'SQLAlchemy':
        user_manager = CustomUserManager(app, db, User, UserInvitationClass=UserInvitation)
    else:
        user_manager = CustomUserManager(app, db, User)

    # For debugging purposes
    token = user_manager.token_manager.generate_token('abc', 123, 'xyz')
    data_items = user_manager.token_manager.verify_token(token, 3600)
    assert data_items is not None
    assert data_items[0] == 'abc'
    assert data_items[1] == 123
    assert data_items[2] == 'xyz'

    # Create regular 'member' user
    if not User.query.filter(User.username=='member').first():
        user = User(username='member', email='member@example.com',
                password=user_manager.password_manager.hash_password('Password1'), email_confirmed_at=datetime.datetime.utcnow())
        db.session.add(user)
        user_manager.db_adapter.commit()

    # Create 'user007' user with 'secret' and 'agent' roles
    if not User.query.filter(User.username=='user007').first():
        user1 = User(username='user007', email='user007@example.com',
                password=user_manager.password_manager.hash_password('Password1'))
        if ORM_type == 'SQLAlchemy':
            user1.roles.append(Role(name='secret'))
            user1.roles.append(Role(name='agent'))
        if ORM_type == 'MongoAlchemy':
            user1.roles = ['secret', 'agent']
        db.session.add(user1)
        user_manager.db_adapter.commit()

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
    @confirmed_email_required
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
    def special_page():
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
            <h2>{%trans%}Special Page{%endtrans%}</h2>
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
