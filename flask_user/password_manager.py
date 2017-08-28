""" This file hashes and verifies passwords for Flask-User.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from __future__ import print_function
from passlib.context import CryptContext
import hashlib
import hmac
import base64

from flask import current_app


def generate_sha512_hmac(self, password_salt, password):
    """ Generate SHA512 HMAC -- for compatibility with Flask-Security """
    return base64.b64encode(hmac.new(password_salt, password.encode('utf-8'), hashlib.sha512).digest())


# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class PasswordManager(object):
    """ PasswordMixin provides password management methods using passlib """

    # Called by UserManager.init_app()
    def __init__(self, password_crypt_context, password_hash_scheme, password_hash_mode, password_salt):
        self.password_crypt_context = password_crypt_context
        self.password_hash_scheme = password_hash_scheme
        self.password_hash_mode = password_hash_mode
        self.password_salt = password_salt

        # Create passlib's CryptContext if needed
        if not self.password_crypt_context:
            self.password_crypt_context = CryptContext(
                    schemes=[self.password_hash_scheme])

    def hash_password(self, password):
        """ Generate hashed password using SHA512 HMAC and the USER_PASSWORD_HASH hash function."""

        # Pre-generate SHA512 HMAC -- For compatibility with Flask-Security
        if self.password_hash_mode == 'Flask-Security':
            password = generate_sha512_hmac(self.password_salt, password)

        # Use passlib's CryptContext to hash password
        hashed_password = self.password_crypt_context.encrypt(password)

        return hashed_password


    def verify_user_password(self, user, password):
        """ Verify password with user's hashed password.
            Returns True on matching password.
            Returns False otherwise."""

        # Perform some Python magic to allow for:
        # - v0.6  verify_user_password(password, user), and
        # - v0.9+ verify_user_password(user, password) parameter order
        if isinstance(user, (b''.__class__, u''.__class__)):
            # Flask-User v0.6 used verify_user_password(password, user)
            temp = user
            user = password
            password = temp

        # Hashed password is stored with the User model or the UserAuth model
        user_manager = current_app.user_manager
        if user_manager.UserAuthModel and hasattr(user_manager.UserModel, 'user_auth'):
            hashed_password = user.user_auth.password
        else:
            hashed_password = user.password

        # Pre-generate SHA512 HMAC -- For compatibility with Flask-Security
        if self.password_hash_mode == 'Flask-Security':
            password = generate_sha512_hmac(self.password_salt, password)

        # Use passlib's CryptContext to verify
        return self.password_crypt_context.verify(password, hashed_password)


    def update_user_hashed_password(self, user, hashed_password):
        # Hashed password is stored with the User model or the UserAuth model
        user_manager = current_app.user_manager
        object = user.user_auth if user_manager.UserAuthModel and hasattr(user_manager.UserModel, 'user_auth') else user
        user_manager.db_adapter.update_object(object, password=hashed_password)
        user_manager.db_adapter.commit()


