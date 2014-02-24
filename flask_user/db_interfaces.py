"""
    flask_user.db_interfaces
    ------------------------
    This module abstracts database/ORM specific code for Flask-User.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from datetime import datetime

from flask_login import current_user

class DBInterface(object):
    """
    This object is used to shield Flask-User from ORM specific dependencies.
    It's used as the base class for ORM specific adapters like SQLAlchemyAdapter.
    """
    def __init__(self, db, UserClass, EmailClass=None):
        self.db = db
        self.UserClass = UserClass
        if not EmailClass:
            EmailClass = UserClass
        self.EmailClass = EmailClass

    def find_user_by_email(self, email): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_email() has not been implemented')

    def find_user_by_username(self, username): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_username() has not been implemented')

    def email_is_available(self, new_email):
        """
        Return True if new_email does not exist.
        Return False otherwise.
        """
        # See if new_email is available
        return self.find_user_by_email(new_email)==None

    def username_is_available(self, new_username, old_username=''):
        """
        Return True if new_username does not exist or if new_username equals old_username.
        Return False otherwise.
        """
        # To avoid user confusion, we allow the old email if the user is currently logged in
        if current_user.is_authenticated():
            old_username = current_user.username
        else:
            old_username = ''
        # See if new_username is available
        return new_username==old_username or self.find_user_by_username(new_username)==None

    def verify_reset_password_token(self, user, token):
        return user.reset_password_token == token

    def get_email(self, user):
        return user.email


class SQLAlchemyAdapter(DBInterface):
    """
    This object is used to shield Flask-User from SQLAlchemy specific dependencies.
    """
    def __init__(self, db, UserClass, EmailClass=None):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass, EmailClass)

    def add_user(self, **kwargs):
        """
        Adds a user record.
        """
        user = self.UserClass(**kwargs)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def confirm_user(self, user_id):
        """
        Mark the user record as active and sets email_confirmed_at to utcnow().
        """
        user = self.find_user_by_id(user_id)
        if user:
            if not user.active:
                user.active = True
                if hasattr(user, 'email_confirmed_at'):
                    user.email_confirmed_at = datetime.utcnow()
                self.db.session.commit()
        else:                                               # pragma: no cover
            assert False, "Invalid user id "+str(user_id)

    def set_username(self, user, username):
        user.username = username
        self.db.session.commit()

    def set_password(self, user, hashed_password):
        user.password = hashed_password
        self.db.session.commit()

    def set_reset_password_token(self, user, token):
        user.reset_password_token = token
        self.db.session.commit()

    def find_user_by_id(self, user_id):
        return self.EmailClass.query.filter(self.EmailClass.id==user_id).first()

    def find_user_by_email(self, email):
        return self.EmailClass.query.filter(self.EmailClass.email.ilike(email)).first()

    def find_user_by_username(self, username):
        return self.UserClass.query.filter(self.UserClass.username.ilike(username)).first()

