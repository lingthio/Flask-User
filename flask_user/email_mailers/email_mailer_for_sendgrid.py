""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function
import smtplib
import socket

from .email_mailer import EmailMailer, SendEmailError


class EmailMailerForSendgrid(EmailMailer):
    """ Implements the EmailMailer interface to send emails with SendGrid Web API v3 using sendgrid-python."""
    def __init__(self, app, sender_email=None, sender_name=None):
        """Setup SendGrid Web API v3.

        Args:
            app: The Flask application instance.
            sender_email: The sender's email address.
            sender_name: The sender's name.

        The from: field will appear as "{{sender_name}} <{{sender_email}}>".
        """

        try:
            from flask_mail import Mail
        except:
            raise SendEmailError(
                "sendgrid-python has not been installed. Install sendgrid-python or use a different mailer package.")
        self.mail = Mail(app)

    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via sendgrid-python.

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
            raise SendEmailError('SMTP Connection error: Check your MAIL_SERVER and MAIL_PORT settings.')
        except smtplib.SMTPAuthenticationError:
            raise SendEmailError('SMTP Authentication error: Check your MAIL_USERNAME and MAIL_PASSWORD settings.')

