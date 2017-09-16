"""This module implements the EmailAdapter interface for sendmail.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import current_app, ConfigError
from flask_user.email_adapters import EmailAdapterInterface


class SendmailEmailAdapter(EmailAdapterInterface):
    """ Implements the EmailAdapter interface to send emails with sendmail using Flask-Sendmail."""
    def __init__(self, app, sender_email=None, sender_name=None):
        """Check config settings and setup Flask-Sendemail.

        Args:
            app(Flask): The Flask application instance.
        """

        super(SendmailEmailAdapter, self).__init__(app)

        # Setup Flask-Mail
        try:
            from flask_sendmail import Mail
        except ImportError:
            raise ConfigError(
                "The Flask-Sendmail package is missing. Install Flask-Sendmail with 'pip install Flask-Sendmail'.")
        self.mail = Mail(app)

    def send_email_message(self, recipient, subject, html_message, text_message, sender_email, sender_name):
        """ Send email message via Flask-Sendmail.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        if not current_app.testing:  # pragma: no cover

            # Prepare email message
            from flask_sendmail import Message
            message = Message(
                subject,
                recipients=[recipient],
                html=html_message,
                body=text_message)

            # Send email message
            self.mail.send(message)


