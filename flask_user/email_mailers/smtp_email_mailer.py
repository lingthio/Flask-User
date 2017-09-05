""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function
import smtplib
import socket

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import ConfigError, EmailError
from flask_user.email_mailers import EmailMailerInterface


class SMTPEmailMailer(EmailMailerInterface):
    """ Implements the EmailMailer interface to send email_templates with SMTP using Flask-Mail."""
    def __init__(self, app):
        """Check config settings and setup Flask-Mail.

        Args:
            app(Flask): The Flask application instance.
        """

        # Check config settings
        super(SMTPEmailMailer, self).__init__(app)

        # Setup Flask-Mail
        try:
            from flask_mail import Mail
        except :
            raise ConfigError(
                "Flask-Mail has not been installed. Install Flask-Mail with 'pip install Flask-Mail' or use a different EmailMailer.")
        self.mail = Mail(app)

    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via Flask-Mail.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        from flask_mail import Message
        try:
            # Prepare email message
            message = Message(
                subject,
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

