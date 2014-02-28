"""
    flask_user.passwords
    --------------------
    This module contains Flask-User functions that deal hashing and verifying passwords.

    It's a thin layer on top of passlib.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from passlib.context import CryptContext

crypt_context = CryptContext(
        schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'],
        default='bcrypt',
        all__vary_rounds = 0.1,
        )

