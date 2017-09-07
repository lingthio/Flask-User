""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import ConfigError, EmailError
from flask_user.email_mailers import EmailMailerInterface

class SendgridEmailMailer(EmailMailerInterface):
    """ Implements the EmailMailer interface to send email_templates with SendGrid Web API v3 using sendgrid-python."""
    def __init__(self, app):
        """Check config settings and setup SendGrid Web API v3.

        Args:
            app(Flask): The Flask application instance.
        """

        # Check config settings
        super(SendgridEmailMailer, self).__init__(app)

        # Setup sendgrid-python
        try:
            from sendgrid import SendGridAPIClient
        except ImportError:
            raise ConfigError(
                "sendgrid-python has not been installed. Install sendgrid-python with 'pip install sendgrid' or use a different EmailMailer.")

        pass    # TODO


    def send_email_message(self, recipient, subject, html_message, text_message):
        """ Send email message via sendgrid-python.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        from sendgrid.helpers.mail import Email, Content, Substitution, Mail
        try:
            pass    # TODO
        except ImportError:
            pass    # TODO

