"""This module implements the EmailMailer interface for sendmail.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import ConfigError, EmailError
from flask_user.email_mailers import EmailMailerInterface


class SendmailEmailMailer(EmailMailerInterface):
    """ Implements the EmailMailer interface to send emails with sendmail using Flask-Sendmail."""
    def __init__(self, app, sender_email=None, sender_name=None):
        """Check config settings and setup Flask-Sendemail.

        Args:
            app(Flask): The Flask application instance.
        """

        # Check config settings
        super(SendmailEmailMailer, self).__init__(app)

        # Setup Flask-Mail
        try:
            from flask_sendmail import Mail
        except ImportError:
            raise ConfigError(
                "Flask-Sendmail has not been installed. Install Flask-Sendmail with 'pip install Flask-Sendmail' or use a different EmailMailer.")
        self.mail = Mail(app)

    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via Flask-Sendmail.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        from flask_sendmail import Message

        # Prepare email message
        message = Message(
            subject,
            recipients=[recipient],
            html=html_message,
            body=text_message)

        # Send email message
        self.mail.send(message)


