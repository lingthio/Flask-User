"""This module implements the EmailAdapter interface for SMTP.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function
import smtplib
import socket

from flask import current_app

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import ConfigError, EmailError
from flask_user.email_adapters import EmailAdapterInterface


class SMTPEmailAdapter(EmailAdapterInterface):
    """ Implements the EmailAdapter interface to send emails with SMTP using Flask-Mail."""
    def __init__(self, app):
        """Check config settings and setup Flask-Mail.

        Args:
            app(Flask): The Flask application instance.
        """

        super(SMTPEmailAdapter, self).__init__(app)

        # Setup Flask-Mail
        try:
            from flask_mail import Mail
        except ImportError:
            raise ConfigError(
                "The Flask-Mail package is missing. Install Flask-Mail with 'pip install Flask-Mail'.")
        self.mail = Mail(app)

    def send_email_message(self, recipient, subject, html_message, text_message, sender_email, sender_name):
        """ Send email message via Flask-Mail.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        # Construct sender from sender_name and sender_email
        sender = '"%s" <%s>' % (sender_name, sender_email) if sender_name else sender_email

        # Send email via SMTP except when we're testing
        if not current_app.testing:  # pragma: no cover
            try:
                # Prepare email message
                from flask_mail import Message
                message = Message(
                    subject,
                    sender=sender,
                    recipients=[recipient],
                    html=html_message,
                    body=text_message)

                # Send email message
                self.mail.send(message)

            # Print helpful error messages on exceptions
            except (socket.gaierror, socket.error) as e:
                raise EmailError('SMTP Connection error: Check your MAIL_SERVER and MAIL_PORT settings.')
            except smtplib.SMTPAuthenticationError:
                raise EmailError('SMTP Authentication error: Check your MAIL_USERNAME and MAIL_PASSWORD settings.')

