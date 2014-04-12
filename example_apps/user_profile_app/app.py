from flask import Flask, render_template_string, request
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, roles_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask.ext.user.forms import RegisterForm
from wtforms import validators
from wtforms import StringField

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'                      # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user_profile_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True


class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.Required('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.Required('Last name is required')])

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except: pass

    # Over-write app config                         # For automated tests
    if test_config:
        for key, value in test_config.items():
            app.config[key] = value

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = babel = Babel(app)
    app.db = db = SQLAlchemy(app)

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

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
        user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=True, default=None)
        # Flask-User fields
        active = db.Column(db.Boolean(), nullable=False, default=False)
        email = db.Column(db.String(255), nullable=False, default='')
        password = db.Column(db.String(255), nullable=False, default='')
        # Relationships
        user_profile = db.relationship('UserProfile', uselist=False, foreign_keys=[user_profile_id])
        roles = db.relationship('Role', secondary=user_roles,
                backref=db.backref('users', lazy='dynamic'))

    class UserProfile(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name = db.Column(db.String(50), nullable=False, default='')

    # Reset all the database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, UserClass=User, UserProfileClass=UserProfile)
    user_manager = UserManager(db_adapter, app,
            register_form=MyRegisterForm)

    # The '/' page is accessible to anyone
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return profile_page()
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
                {{ current_user.user_profile.first_name }},</p>
            <p> <a href="{{ url_for('user.change_password') }}">
                {%trans%}Change password{%endtrans%}</a></p>
            <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app

# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
