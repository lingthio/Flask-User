from sqlalchemy.sql import func
from flask_login import UserMixin

from example_app.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, default='')
    active = db.Column(db.Boolean(), nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
