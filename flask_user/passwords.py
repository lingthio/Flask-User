""" This file hashes and verifies passwords for Flask-User.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from __future__ import print_function
import hashlib
import hmac
import base64

def generate_sha512_hmac(password_salt, password):
    """ Generate SHA512 HMAC -- for compatibility with Flask-Security """
    return base64.b64encode(hmac.new(password_salt, password.encode('utf-8'), hashlib.sha512).digest())

def hash_password(user_manager, password):
    """ Generate hashed password using SHA512 HMAC and the USER_PASSWORD_HASH hash function."""
    # Handle plaintext storage
    if user_manager.password_hash == 'plaintext':
        return password
    # Generate SHA512 HMAC -- For compatibility with Flask-Security
    if user_manager.password_hash_mode == 'Flask-Security':
        password = generate_sha512_hmac(user_manager.password_salt, password)
    # Use passlib to hash password
    hashed_password = user_manager.password_crypt_context.encrypt(password)

    return hashed_password

def verify_password(user_manager, password, hashed_password):
    """ Verify password with previously hashed password.
        Returns True on matching password.
        Returns False otherwise."""
    # Handle plaintext storage
    if user_manager.password_hash == 'plaintext':
        return password==hashed_password
    # Generate SHA512 HMAC -- For compatibility with Flask-Security
    if user_manager.password_hash_mode == 'Flask-Security':
        password = generate_sha512_hmac(user_manager.password_salt, password)

    return user_manager.password_crypt_context.verify(password, hashed_password)

