from sqlalchemy.sql import func
from flask_login import UserMixin

from example_app.database import db

class User(db.Model, UserMixin):
    # Flask-Login required fields
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)

    # Flask-User required fields
    username = db.Column(db.String(50), nullable=True, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, default='')
    password_reset_token = db.Column(db.String(100), nullable=False, default='')

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
