from flask import Flask, render_template_string
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'             # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///minimal_app.db'  # Use Sqlite file db
    CSRF_ENABLED = True

# Setup Flask and read config from ConfigClass defined above
app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

# Setup Flask-Babel and Flask-SQLAlchemy
app.babel = Babel(app)
db = SQLAlchemy(app)

# Define User model. Make sure to add flask.ext.user UserMixin!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')

# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

# The '/' page requires a logged-in user
@app.route('/')
@login_required                                 # Use of @login_required decorator
def profile_page():
    return render_template_string(
        """
        {% extends "base.html" %}
        {% block content %}
            <h2>Profile Page</h2>
            <p> {%trans%}Hello{%endtrans%}
                {{ current_user.username or current_user.email }},</p>
            <p> <a href="{{ url_for('user.change_password') }}">
                {%trans%}Change password{%endtrans%}</a></p>
            <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                {%trans%}Sign out{%endtrans%}</a></p>
        {% endblock %}
        """)

# Start development web server
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

