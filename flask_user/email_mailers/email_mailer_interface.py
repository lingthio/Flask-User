""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function

from flask_user import ConfigError


class EmailMailerInterface(object):
    """ Define the EmailMailer interface to send email_templates through specific email mailers."""

    def __init__(self, app):
        """
        Ensure that USER_EMAIL_SENDER_EMAIL is configured.

        Args:
            app(Flask): The Flask application instance.
        """
        self.sender_name = app.config.get('USER_EMAIL_SENDER_NAME', None)
        self.sender_email = app.config.get('USER_EMAIL_SENDER_EMAIL', None)

        # Ensure that USER_EMAIL_SENDER_EMAIL is set
        if not self.sender_email:
            raise ConfigError('Config setting USER_EMAIL_SENDER_EMAIL is missing.')
        # Simplistic email address verification
        if '@' not in self.sender_email:
            raise ConfigError('Config setting USER_EMAIL_SENDER_EMAIL is not a valid email address.')

    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via an email mailer.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """
        raise NotImplementedError
