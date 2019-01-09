"""This module implements the TOTPManager for Flask-User.
It uses onetimepass to generate URI and verify OTP tokens.
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
        #TODO check if username is enabled, otherwise use email instead
        #TODO compensate for spaces in APP_NAME
        app_name = self.user_manager.USER_APP_NAME
        return 'otpauth://totp/{0}:{1}?secret={2}&issuer={0}'.format(app_name, current_user.username, current_user.totp_secret)

    def verify_totp_token(self, totp_token):
        return onetimepass.valid_totp(totp_token, current_user.totp_secret)

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
