"""Manager for generating and verifying tokens.

This module contains a manager class to generate and verify tokens.

:copyright: (c) 2013 by Ling Thio
:author: Ling Thio (ling.thio@gmail.com)
:license: Simplified BSD License, see LICENSE.txt for more details.
"""

import base64
from cryptography.fernet import Fernet, InvalidToken
import string

# Constants used by _encode_int() and _decode_int()
# URL-safe characters are letters, digits, '-', '_', '.', '~'.
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SEPARATOR = '$'

class TokenManager(object):
    """Generate and verify timestamped, signed and encrypted tokens. """

    # *** Public methods ***

    def __init__(self, flask_secret_key):
        """Initialize the TokenManager class

        Args:
            flask_secret_key (str): The secret key used to encrypt and decrypt tokens.
                This is typically Flask's SECRET_KEY setting.
                Preferably 32 bytes or longer, but spaces will be padded if needed.
        """

        # Generate a 32-byte base-64 key from the Flask SECRET_KEY
        long_key = flask_secret_key.encode() + b' '*32    # Make sure the key is at least 32 bytes long
        key32 = long_key[:32]
        base64_key32 = base64.urlsafe_b64encode(key32)

        # Create a Fernet cypher to encrypt data -- basically AES128 in CBC mode,
        # Encrypt, timestamp, sign, and base64-encode
        self.fernet = Fernet(base64_key32)

    def generate_token(self, *args):
        """ Converts a list of integers or strings, specified by ``*args``, into an encrypted, timestamped, and signed token.

        The default implementation:

        - encode string items as-is,
        - encode integer items as base-64 strings with a '#' character in front,
        - concatenate encoded items with a '$' separator, and
        - use ``cryptograpy.fernet.Fernet()`` to timestamp, sign, and encrypt the concatenated string.

        ``generate_token('abc', 123, 'xyz')`` encrypts the concatenated string ``'abc$#B7$xyz'``
        into an encrypted token.
        """
        token = self._encrypt_data_items(*args)
        return token

    def verify_token(self, token, expiration_in_seconds):
        """ Verify token signature, verify token expiration, and decrypt token.

            Returns None on expired or invalid tokens. Returns a list of strings and integers on success."""

        try:
            data_items = self._decrypt_data_items(token, expiration_in_seconds)
        except InvalidToken:
            data_items = None

        return data_items

    # *** Private methods ***

    def _encrypt_data_items(self, *args):
        """ Encodes a list of data items (*args). Each item can be a string or an integer. """
        str_list = []

        # Integers are encoded into a #Short-string. Strings are used as-is.
        for arg in args:
            if isinstance(arg, int):
                str = '#' + self._encode_int(arg)   # encode integers as #Short-string
            else:
                str = arg                           # use strings as-is
            str_list.append(str)

        # Concatenate strings with '$' separators
        concatenated_str = SEPARATOR.join(str_list)

        # Convert string to bytes
        concatenated_bytes = concatenated_str.encode()

        # Encrypt, timestamp, sign, and base64-encode
        encrypted_bytes = self.fernet.encrypt(concatenated_bytes)

        # Convert bytes to string
        encrypted_str = encrypted_bytes.decode('utf-8')

        # Remove '=' padding if needed
        token_str = encrypted_str.strip('=')
        return token_str

    def _decrypt_data_items(self, token_str, expiration_in_seconds):
        # Add '=' padding if needed
        if len(token_str) % 4:
            token_str += '=' * (4 - len(token_str) % 4)

        # Convert string to bytes
        encrypted_bytes = token_str.encode()

        # Base-64-decode, verify signature, verify expiration, and decrypt
        concatenated_bytes = self.fernet.decrypt(encrypted_bytes, expiration_in_seconds)
        concatenated_str = concatenated_bytes.decode('utf-8')

        # Split concatenated string into list of strings
        str_list = concatenated_str.split('$')

        # #Short-strings are decoded into integers. Strings are used as-is.
        data_items = []
        for str in str_list:
            if len(str)>=1 and str[0]=='#':         # decode #Short-strings to integers
                item = self._decode_int(str[1:])
            else:
                item = str                          # use strings as-is
            data_items.append(item)

        # Return list of data items
        return data_items

    def _encode_int(self, n):
        """ Encodes an integer into a short Base64 string """
        str = []
        while True:
            n, r = divmod(n, BASE)
            str.append(ALPHABET[r])
            if n == 0: break
        return ''.join(reversed(str))

    def _decode_int(self, str):
        """ Decodes a short Base64 string into an integer """
        n = 0
        for c in str:
            n = n * BASE + ALPHABET_REVERSE[c]
        return n
