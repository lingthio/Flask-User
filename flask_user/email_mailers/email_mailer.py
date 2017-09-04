""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function
import smtplib
import socket


# Define the SendMailError exception
class SendEmailError(Exception):
    pass


class EmailMailer(object):
    """ Define the EmailMailer interface to send email_templates through specific email mailers."""

    def __init__(self, app, sender_email=None, sender_name=None):
        """Setup an email mailer.

        Args:
            app: The Flask application instance.
            sender_email: The sender's email address.
            sender_name: The sender's name.

        The from: field will appear as "{{sender_name}} <{{sender_email}}>".
        """
        raise NotImplementedError

    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via an email mailer.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """
        raise NotImplementedError
