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
    def __init__(self, db, UserClass, RoleClass=None, ProfileClass=None, EmailClass=None):
        self.db = db
        self.UserClass = UserClass          # email, password, etc.
        self.ProfileClass = ProfileClass    # For Additional registration fields
        self.RoleClass = RoleClass          # For role based authorization
        self.EmailClass = EmailClass        # For multiple emails per user

    def find_user_by_email(self, email): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_email() has not been implemented')

    def find_user_by_username(self, username): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_username() has not been implemented')

    def set_object_fields(self, object, **kwargs):
        for key,value in kwargs.items():
            if hasattr(object, key):
                setattr(object, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(object), key))

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

    # def get_email(self, user):
    #     return user.email


class SQLAlchemyAdapter(DBInterface):
    """
    This object is used to shield Flask-User from SQLAlchemy specific dependencies.
    """
    def __init__(self, db, UserClass, RoleClass=None, ProfileClass=None, EmailClass=None):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass, RoleClass, ProfileClass, EmailClass)

    def add_user(self, **kwargs):
        """
        Adds a user record.
        """
        user = self.UserClass(**kwargs)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    # TODO: multiple_emails_per_user
    # def add_email(self, **kwargs):
    #     """
    #     Adds an email record for the multiple emails per user feature
    #     """
    #     email = self.EmailClass(**kwargs)
    #     self.db.session.add(email)
    #     self.db.session.commit()
    #     return email

    def confirm_email(self, object_id):
        """
        Mark the user record as active and sets confirmed_at to utcnow().
        object_id can either be a user_id or an email_id for the multiple_emails_per_user feature
        """
        if not self.EmailClass:
            user = self.find_user_by_id(object_id)
            if user:
                if not user.active:
                    user.active = True
                    if hasattr(user, 'confirmed_at'):
                        user.confirmed_at = datetime.utcnow()
                    self.db.session.commit()
            else:                                               # pragma: no cover
                assert False, "Invalid user id "+str(object_id)
        else:
            raise NotImplementedError   # TODO:
        return user

    def set_object_fields(self, object, **kwargs):
        super(SQLAlchemyAdapter, self).set_object_fields(object, **kwargs)
        self.db.session.commit()

    # def set_username(self, user, username):
    #     user.username = username
    #     self.db.session.commit()
    #
    # def set_password(self, user, hashed_password):
    #     user.password = hashed_password
    #     self.db.session.commit()
    #
    # def set_reset_password_token(self, user, token):
    #     user.reset_password_token = token
    #     self.db.session.commit()

    def find_user_by_id(self, user_id):
        return self.UserClass.query.filter(self.UserClass.id==user_id).first()

    def find_user_by_email(self, email):
        if self.EmailClass:
            raise NotImplementedError   # TODO:
            # return self.EmailClass.query.filter(self.EmailClass.email.ilike(email)).first()
        else:
            return self.UserClass.query.filter(self.UserClass.email.ilike(email)).first()

    def find_user_by_username(self, username):
        return self.UserClass.query.filter(self.UserClass.username.ilike(username)).first()

