"""This module implements the DBManager for Flask-User.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from .db_adapters import DynamoDbAdapter, MongoDbAdapter, SQLDbAdapter
from flask_user import current_user, ConfigError

class DBManager(object):
    """Manage DB objects."""

    def __init__(self, app, db, UserClass, UserEmailClass=None, UserInvitationClass=None, RoleClass=None):
        """Initialize the appropriate DbAdapter, based on the ``db`` parameter type."""
        self.app = app
        self.db = db
        self.UserClass = UserClass
        self.UserEmailClass = UserEmailClass
        self.UserInvitationClass = UserInvitationClass
        self.RoleClass = RoleClass

        self.user_manager = app.user_manager
        self.db_adapter = None

        # Check if db is a SQLAlchemy instance
        if self.db_adapter is None:
            try:
                from flask_sqlalchemy import SQLAlchemy

                if isinstance(db, SQLAlchemy):
                    self.db_adapter = SQLDbAdapter(app, db)
            except ImportError:
                pass  # Ignore ImportErrors

        # Check if db is a MongoEngine instance
        if self.db_adapter is None:
            try:
                from flask_mongoengine import MongoEngine

                if isinstance(db, MongoEngine):
                    self.db_adapter = MongoDbAdapter(app, db)
            except ImportError:
                pass  # Ignore ImportErrors

        # Check if db is a Flywheel instance
        if self.db_adapter is None:
            try:
                from flask_flywheel import Flywheel

                if isinstance(db, Flywheel):
                    self.db_adapter = DynamoDbAdapter(app, db)
            except ImportError:
                pass  # Ignore ImportErrors

        # Check self.db_adapter
        if self.db_adapter is None:
            raise ConfigError(
                'No Flask-SQLAlchemy, Flask-MongoEngine or Flask-Flywheel installed.'\
                ' You must install one of these Flask extensions.')


    def add_user(self, **kwargs):
        if 'email' in kwargs:
            kwargs['email'] = kwargs['email'].lower()
        if 'username' in kwargs:
            kwargs['username'] = kwargs['username'].lower()
        user = self.UserClass(**kwargs)
        self.db_adapter.add_object2(user)
        return user

    def add_user_email(self, user, **kwargs):
        if 'email' in kwargs:
            kwargs['email'] = kwargs['email'].lower()
        # If User and UserEmail are separate classes
        if self.UserEmailClass:
            user_email = self.UserEmailClass(user=user, **kwargs)
            self.db_adapter.add_object2(user_email)

        # If there is only one User class
        else:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user_email = user

        return user_email

    def add_user_invitation(self, **kwargs):
        if 'email' in kwargs:
            kwargs['email'] = kwargs['email'].lower()
        user_invitation = self.UserInvitationClass(**kwargs)
        self.db_adapter.add_object2(user_invitation)
        return user_invitation

    def commit(self):
        self.db_adapter.commit()

    def delete_object(self, object):
        self.db_adapter.delete_object(object)

    def get_user_and_user_email_by_id(self, user_or_user_email_id):
        if self.UserEmailClass:
            user_email = self.db_adapter.get_object(self.UserEmailClass, user_or_user_email_id)
            if user_email:
                user = user_email.user
            else:
                user = None
        else:
            user = self.db_adapter.get_object(self.UserClass, user_or_user_email_id)
            user_email = user
        return (user, user_email)

    def get_user_and_user_email_by_email(self, email):
        if self.UserEmailClass:
            # Although with v0.9+ we store lowercase emails and usernames,
            # To be backwards compatible with v0.6 data we still need to use ifind for SQLAlchemy data
            if isinstance(self.db_adapter, SQLDbAdapter):
                user_email = self.db_adapter.ifind_first_object(self.UserEmailClass, email=email)
            else:
                user_email = self.db_adapter.find_first_object(self.UserEmailClass, email=email.lower())
            if user_email:
                user = user_email.user
            else:
                user = None
        else:
            # Although with v0.9+ we store lowercase emails and usernames,
            # To be backwards compatible with v0.6 data we still need to use ifind for SQLAlchemy data
            if isinstance(self.db_adapter, SQLDbAdapter):
                user = self.db_adapter.ifind_first_object(self.UserClass, email=email)
            else:
                user = self.db_adapter.find_first_object(self.UserClass, email=email.lower())
            user_email = user
        return (user, user_email)

    def find_user_by_username(self, username):
        # Although with v0.9+ we store lowercase emails and usernames,
        # To be backwards compatible with v0.6 data we still need to use ifind for SQLAlchemy data
        if isinstance(self.db_adapter, SQLDbAdapter):
            return self.db_adapter.ifind_first_object(self.UserClass, username=username)
        else:
            return self.db_adapter.find_first_object(self.UserClass, username=username.lower())

    def find_user_emails(self, user):
        user_emails = self.db_adapter.find_objects(self.UserEmailClass, user_id=user.id)
        return user_emails

    def get_primary_user_email(self, user):
        """Retrieve the email from User object or the primary UserEmail object (if multiple emails
        per user are enabled)."""
        if self.UserEmailClass:
            user_email = self.db_adapter.find_first_object(
                self.UserEmailClass,
                user_id=user.id,
                is_primary=True)
            return user_email
        else:
            return user

    def get_user_by_id(self, id):
        return self.db_adapter.get_object(self.UserClass, id=id)

    def get_user_email_by_id(self, id):
        """Retrieve a UserEmail object by ID."""
        return self.db_adapter.get_object(self.UserEmailClass, id)

    def get_user_invitation_by_id(self, id):
        return self.db_adapter.get_object(self.UserInvitationClass, id=id)

    def save_user_and_user_email(self, user, user_email):
        if self.UserEmailClass:
            self.db_adapter.save_object(user_email)
        self.db_adapter.save_object(user)

    def save_object(self, object):
        self.db_adapter.save_object(object)

    # Return True if ENABLE_EMAIL and ENABLE_CONFIRM_EMAIL and email has been confirmed.
    # Return False otherwise
    def user_has_confirmed_email(self, user):
        """| Return True if user has a confirmed email.
        | Return False otherwise."""
        if not self.user_manager.USER_ENABLE_EMAIL: return True
        if not self.user_manager.USER_ENABLE_CONFIRM_EMAIL: return True

        db_adapter = self.db_adapter

        # Handle multiple emails per user: Find at least one confirmed email
        if self.UserEmailClass:
            has_confirmed_email = False
            user_emails = db_adapter.find_objects(self.UserEmailClass, user_id=user.id)
            for user_email in user_emails:
                if user_email.email_confirmed_at:
                    has_confirmed_email = True
                    break

        # Handle single email per user
        else:
            has_confirmed_email = True if user.email_confirmed_at else False

        return has_confirmed_email

    def username_is_available(self, new_username):
        """Check if ``new_username`` is still available.

        | Returns True if ``new_username`` does not exist or belongs to the current user.
        | Return False otherwise.
        """

        # Return True if new_username equals current user's username
        if self.user_manager.call_or_get(current_user.is_authenticated):
            if new_username == current_user.username:
                return True

        # Return True if new_username does not exist,
        # Return False otherwise.
        return self.find_user_by_username(new_username) == None



    # Role management methods
    # -----------------------

    def add_user_role(self, user, role_name):
        """ Add a ``role_name`` role to ``user``."""
        if isinstance(self.db_adapter, SQLDbAdapter):
            # user.roles is a list of Role IDs
            # Get or add role
            role = self.db_adapter.find_first_object(self.RoleClass, name=role_name)
            if not role:
                role = self.db_adapter.add_object(self.RoleClass, name=role_name)
            user.roles.append(role)
        else:
            # user.roles is a list of role names
            user.roles.append(role_name)

    def get_user_roles(self, user):
        """Retrieve a list of user role names.

        .. note::

            Database management methods.
        """
        if isinstance(self.db_adapter, SQLDbAdapter):
            # user.roles is a list of Role IDs
            return [role.name for role in user.roles]
        else:
            # user.roles is a list of role names
            user_roles = user.roles

        return user_roles

    def delete_role_name(self, role_name):
        if isinstance(self.db_adapter, SQLDbAdapter):
            role = self.db_adapter.find_first_object(self.user_manager.db_manager.RoleClass, name=role_name)
            if role:
                self.db_adapter.delete_object(role)


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

