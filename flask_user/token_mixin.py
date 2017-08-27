""" This file contains functions to generate and verify tokens for Flask-User.
    Tokens contain an encoded user ID and a signature. The signature is managed by the itsdangerous module.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from itsdangerous import BadSignature, SignatureExpired, TimestampSigner

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class TokenMixin(object):

    # *** Public methods ***

    # Called by UserManager.init_app()
    def init_token_mixin(self, secret):
        """ Create a cypher to encrypt IDs and a signer to sign tokens."""
        # Create cypher to encrypt IDs
        # and ensure >=16 characters
        trailer = b'0123456789abcdef'
        if isinstance(secret, bytes):
            key = secret + trailer
        else:
            key = secret.encode("utf-8") + trailer
        self.cipher = AES.new(key[0:16], AES.MODE_ECB)

        # Create signer to sign tokens
        self.signer = TimestampSigner(secret)

    def generate_token(self, id):
        """ Return token with id, timestamp and signature"""
        # In Python3 we must make sure that bytes are converted to strings.
        # Hence the addition of '.decode()'
        return self.signer.sign(self._encrypt_id(id)).decode()

    def verify_token(self, token, expiration_in_seconds):
        """ Verify token and return (is_valid, has_expired, id).
            Returns (True, False, id) on success.
            Returns (False, True, None) on expired tokens.
            Returns (False, False, None) on invalid tokens."""
        try:
            data = self.signer.unsign(token, max_age=expiration_in_seconds)
            is_valid = True
            has_expired = False
            id = self._decrypt_id(data)
        except SignatureExpired:
            is_valid = False
            has_expired = True
            id = None
        except BadSignature:
            is_valid = False
            has_expired = False
            id = None
        return (is_valid, has_expired, id)

    # *** Private methods ***

    def _encrypt_id(self, id):
        """ Encrypts integer ID to url-safe base64 string."""
        hex_str = format(id, 'x')                                 # Convert integer to hex string
        hex_bytes = hex_str.encode()                              # Convert to bytes
        padded_bytes = pad(hex_bytes, 16)                         # Pad to multiples of 16
        encrypted_bytes = self.cipher.encrypt(padded_bytes)       # Encrypt
        encrypted_id = base64.urlsafe_b64encode(encrypted_bytes)  # Convert to URL-safe string

        # For debug purposes
        # print('TokenMixin._encrypt_id()')
        # print('hex_str', hex_str)
        # print('hex_bytes', hex_bytes)
        # print('padded_bytes', padded_bytes)
        # print('encrypted_bytes', encrypted_bytes)
        # print('encrypted_id', encrypted_id)

        return encrypted_id

    def _decrypt_id(self, encrypted_id):
        """ Decrypts url-safe base64 string to integer ID"""
        # Convert strings and unicode strings to bytes if needed
        if hasattr(encrypted_id, 'encode'):
            encrypted_id = encrypted_id.encode('ascii', 'ignore')

        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_id)  # Convert to bytes
            padded_bytes = self.cipher.decrypt(encrypted_bytes)       # Decrypt
            hex_bytes = unpad(padded_bytes, 16)                       # Remove padding
            id = int(hex_bytes, 16)                                   # Convert hex to integer

            # For debug purposes
            # print('TokenMixin._decrypt_id()')
            # print('encrypted_id', encrypted_id)
            # print('encrypted_bytes', encrypted_bytes)
            # print('padded_bytes', padded_bytes)
            # print('hex_bytes', hex_bytes)
            # print('id', id)

            return id
        except Exception as e:                      # pragma: no cover
            print('!!!Exception in _decrypt_id()!!!:', e)
            return 0

