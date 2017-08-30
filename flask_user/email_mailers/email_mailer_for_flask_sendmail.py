""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function

from .email_mailer import EmailMailer, SendEmailError


class EmailMailerForFlaskSendmail(EmailMailer):
    """ Implements the EmailMailer interface to send emails with sendmail using Flask-Sendmail."""
    def __init__(self, app, sender_email=None, sender_name=None):
        """Setup Flask-Sendemail.

        Args:
            app: The Flask application instance.
            sender_email: The sender's email address.
            sender_name: The sender's name.

        The from: field will appear as "{{sender_name}} <{{sender_email}}>".
        """

        try:
            from flask_sendmail import Mail
        except:
            raise SendEmailError(
                "Flask-Sendmail has not been installed. Install Flask-Sendmail or use a different mailer package.")
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


