"""This module defines the EmailAdapter interface.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

from flask_user import ConfigError


class EmailAdapterInterface(object):
    """ Define the EmailAdapter interface to send emails through various email services."""

    def __init__(self, app):
        """
        Args:
            app(Flask): The Flask application instance.
        """
        pass

    def send_email_message(self, recipient, subject, html_message, text_message, sender_email, sender_name):
        """ Send email message via an email mailer.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """
        raise NotImplementedError
