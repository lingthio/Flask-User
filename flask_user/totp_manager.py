"""This module implements the TOTPManager for Flask-User.
It generates the users URI and uses onetimepass to verify TOTP tokens.
"""

# Adapted from https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask
# Author Jason Hines <jason@hinesnetwork.com>

from io import BytesIO
import onetimepass
import pyqrcode
from flask_login import current_user


class TOTPManager(object):
    """Time-based One Time Password URI generation and verify with onetimepass"""
    def __init__(self, app):
        self.app = app
        self.user_manager = app.user_manager
        
    def get_totp_uri(self):
        """Generate URI for User"""
        app_name = ''.join(self.user_manager.USER_APP_NAME.split())
        if self.user_manager.USER_ENABLE_USERNAME:
            user = current_user.username
            if not user and self.user_manager.USER_ENABLE_EMAIL:
                user = current_user.email

            return 'otpauth://totp/{0}:{1}?secret={2}&issuer={0}'.format(app_name, user, current_user.totp_secret)

    def verify_totp_token(self, user, totp_token):
        return onetimepass.valid_totp(totp_token, user.totp_secret)

    def get_totp_qrcode(self):
        """ render TOTP qrcode """
        url = pyqrcode.create(self.get_totp_uri())
        stream = BytesIO()
        url.svg(stream, scale=5)
        return stream.getvalue(), 200, {
            'Content-Type': 'image/svg+xml',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'}
