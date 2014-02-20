from flask_sqlalchemy import SQLAlchemy

# db is defined in a separate database.py file to avoid circular import between .app and .models
db = SQLAlchemy()
