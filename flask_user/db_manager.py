"""This module implements the DBManager for Flask-User.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from .db_adapters import DynamoDbAdapter, MongoDbAdapter, SQLDbAdapter

class DBManager(object):
    """Manage DB objects."""

    def __init__(self, app, db):
        """Initialize the appropriate DbAdapter, based on the ``db`` parameter type."""
        self.app = app
        self.user_manager = app.user_manager
        self.db_adapter = None
        self.db_type = None

        # Check if db is a SQLAlchemy instance
        if self.db_adapter is None:
            try:
                from flask_sqlalchemy import SQLAlchemy

                if isinstance(db, SQLAlchemy):
                    self.db_adapter = SQLDbAdapter(app, db)
                    self.db_type = 'SQL'
            except ImportError:
                pass  # Ignore ImportErrors

        # Check if db is a MongoEngine instance
        if self.db_adapter is None:
            try:
                from flask_mongoengine import MongoEngine

                if isinstance(db, MongoEngine):
                    self.db_adapter = MongoDbAdapter(app, db)
                    self.db_type = 'MongoDB'
            except ImportError:
                pass  # Ignore ImportErrors

        # Check if db is a Flywheel instance
        if self.db_adapter is None:
            try:
                from flask_flywheel import Flywheel

                if isinstance(db, Flywheel):
                    self.db_adapter = DynamoDbAdapter(app, db)
                    self.db_type = 'DynamoDB'
            except ImportError:
                pass  # Ignore ImportErrors

    def create_user(self, **kwargs):
        user = self.user_manager.UserClass(**kwargs)
        return user

    def create_user_email(self, user, **kwargs):
        # If User and UserEmail are separate classes
        if self.user_manager.EmailClass:
            user_email = self.user_manager.UserEmailClass(user=user, **kwargs)

        # If there is only one User class
        else:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user_email = user

        return user_email

    def find_user_and_user_email_by_email(self, email):
        if self.user_manager.EmailClass:
            user_email = self.db_adapter.find_object(self.user_manager.UserEmailClass, email=email.lower())
            if user_email:
                user = user_email.user
            else:
                user = None
        else:
            user = self.db_adapter.find_object(self.user_manager.UserClass, email=email.lower())
            user_email = user
        return (user, user_email)

    def find_user_by_username(self, username):
        return self.db_adapter.find_object(self.user_manager.UserClass, username=username)

    def save_user_and_user_email(self, user, user_email):
        if self.user_manager.EmailClass:
            self.db_adapter.save_object(user_email)
        else:
            user.email = user_email.email
        self.db_adapter.save_object(user)

    def commit(self):
        self.db_adapter.commit()


    # Role management methods
    # -----------------------

    def add_user_role(self, user, role_name, RoleClass=None):
        """ Add a ``role_name`` role to ``user``."""
        return self.db_adapter.add_user_role(user, role_name, RoleClass)

    def get_user_roles(self, user):
        """Retrieve a list of user role names.

        .. note::

            Database management methods.
        """
        return self.db_adapter.get_user_roles(user)


    # Database management methods
    # ---------------------------

    def create_all_tables(self):
        """Create database tables for all known database data-models."""
        return self.db_adapter.create_all_tables()

    def drop_all_tables(self):
        """Drop all tables.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        return self.db_adapter.drop_all_tables()

