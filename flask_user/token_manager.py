"""This module implements the TokenManager for Flask-User.
It uses cryptography to generate and verify tokens.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

import base64
import string

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import ConfigError

class TokenManager(object):
    """Generate and verify timestamped, signed and encrypted tokens. """

    # *** Constants ***

    # URL-safe characters are letters, digits, '-', '_', '.', '~'.
    ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'
    ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
    BASE = len(ALPHABET)
    INTEGER_PREFIX = '~'
    SEPARATOR = '|'

    # *** Public methods ***

    def __init__(self, app):
        """Check config settings and initialize the Fernet encryption cypher.

        Fernet is basically AES128 in CBC mode, with a timestamp and a signature.

        Args:
            app(Flask): The Flask application instance.
        """

        self.app = app

        # Use the applications's SECRET_KEY if flask_secret_key is not specified.
        flask_secret_key = app.config.get('SECRET_KEY', None)
        if not flask_secret_key:
            raise ConfigError('Config setting SECRET_KEY is missing.')

        # Print a warning if SECRET_KEY is too short
        key = flask_secret_key.encode()
        if len(key)<32:
            print('WARNING: Flask-User TokenManager: SECRET_KEY is shorter than 32 bytes.')
            key = key + b' '*32    # Make sure the key is at least 32 bytes long

        key32 = key[:32]
        base64_key32 = base64.urlsafe_b64encode(key32)

        # Create a Fernet cypher to encrypt data -- basically AES128 in CBC mode,
        # Encrypt, timestamp, sign, and base64-encode
        from cryptography.fernet import Fernet
        self.fernet = Fernet(base64_key32)

    def generate_token(self, *args):
        """ Convert a list of integers or strings, specified by ``*args``, into an encrypted, timestamped, and signed token.

        Note: strings may not contain any ``'|'`` characters, nor start with a ``'~'`` character
        as these are used as separators and integer indicators for encoding.

        Example:

        ::

            # Combine User ID with last 8 bytes of their password
            # to invalidate tokens when passwords change.
            user_id = user.id
            password_ends_with = user.password[-8:0]
            token = token_manager.generate_token(user_id, password_ends_with)
        """
        concatenated_str = self.encode_data_items(*args)
        token = self.encrypt_string(concatenated_str)
        return token

    def verify_token(self, token, expiration_in_seconds=None):
        """ Verify token signature, verify token expiration, and decrypt token.

        | Returns None if token is expired or invalid.
        | Returns a list of strings and integers on success.

        Implemented as::

            concatenated_str = self.decrypt_string(token, expiration_in_seconds)
            data_items = self.decode_data_items(concatenated_str)
            return data_items

        Example:

        ::

            # Verify that a User with ``user_id`` has a password that ends in ``password_ends_with``.
            token_is_valid = False
            data_items = token_manager.verify(token, expiration_in_seconds)
            if data_items:
                user_id = data_items[0]
                password_ends_with = data_items[1]
                user = user_manager.db_manager.get_user_by_id(user_id)
                token_is_valid = user and user.password[-8:]==password_ends_with
        """

        from cryptography.fernet import InvalidToken

        try:
            concatenated_str = self.decrypt_string(token, expiration_in_seconds)
            data_items = self.decode_data_items(concatenated_str)
        except InvalidToken:
            data_items = None

        return data_items

    def encrypt_string(self, concatenated_str):
        """Timestamp, sign and encrypt a string into a token using ``cryptography.fernet.Fernet()``."""

        # Convert string to bytes
        concatenated_bytes = concatenated_str.encode()

        # Encrypt, timestamp, sign, and base64-encode
        encrypted_bytes = self.fernet.encrypt(concatenated_bytes)

        # Convert bytes to string
        encrypted_str = encrypted_bytes.decode('utf-8')

        # Remove '=' padding if needed
        token_str = encrypted_str.strip('=')
        return token_str

    def decrypt_string(self, token_str, expiration_in_seconds=None):
        """Verify signature, verify timestamp, and decrypt a token using ``cryptography.fernet.Fernet()``."""

        # Add '=' padding if needed
        if len(token_str) % 4:
            token_str += '=' * (4 - len(token_str) % 4)

        # Convert string to bytes
        encrypted_bytes = token_str.encode()

        # Verify signature, verify expiration, and decrypt using ``cryptography.fernet.Fernet()``
        concatenated_bytes = self.fernet.decrypt(encrypted_bytes, expiration_in_seconds)
        concatenated_str = concatenated_bytes.decode('utf-8')

        return concatenated_str

    def encode_data_items(self, *args):
        """ Encodes a list of integers and strings into a concatenated string.

        - encode string items as-is.
        - encode integer items as base-64 with a ``'~'`` prefix.
        - concatenate encoded items with a ``'|'`` separator.

        Example:
            ``encode_data_items('abc', 123, 'xyz')`` returns ``'abc|~B7|xyz'``
        """
        str_list = []
        for arg in args:

            # encode string items as-is
            if isinstance(arg, str):
                arg_str = arg

            # encode integer items as base-64 strings with a '~' character in front
            elif isinstance(arg, int):
                arg_str = self.INTEGER_PREFIX + self.encode_int(arg)

            # convert other types to string
            else:
                arg_str = str(arg)

            str_list.append(arg_str)

        # Concatenate strings with '|' separators
        concatenated_str = self.SEPARATOR.join(str_list)

        return concatenated_str

    def decode_data_items(self, concatenated_str):
        """Decodes a concatenated string into a list of integers and strings.

        Example:
            ``decode_data_items('abc|~B7|xyz')`` returns ``['abc', 123, 'xyz']``
        """

        data_items = []
        str_list = concatenated_str.split(self.SEPARATOR)
        for str in str_list:

            # '~base-64-strings' are decoded into integers.
            if len(str)>=1 and str[0]==self.INTEGER_PREFIX:
                item = self.decode_int(str[1:])

            # Strings are decoded as-is.
            else:
                item = str

            data_items.append(item)

        # Return list of data items
        return data_items

    def encode_int(self, n):
        """ Encodes an integer into a short Base64 string.

        Example:
            ``encode_int(123)`` returns ``'B7'``.
        """
        str = []
        while True:
            n, r = divmod(n, self.BASE)
            str.append(self.ALPHABET[r])
            if n == 0: break
        return ''.join(reversed(str))

    def decode_int(self, str):
        """ Decodes a short Base64 string into an integer.

        Example:
            ``decode_int('B7')`` returns ``123``.
        """
        n = 0
        for c in str:
            n = n * self.BASE + self.ALPHABET_REVERSE[c]
        return n
