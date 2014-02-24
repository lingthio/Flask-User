from sqlalchemy.sql import func
from flask.ext.user import UserMixin

from example_app.database import db

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

    # Additional application fields
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
