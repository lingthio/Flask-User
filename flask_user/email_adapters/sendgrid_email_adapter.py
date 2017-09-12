"""This module implements the EmailAdapter interface for SendGrid.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import current_app, ConfigError
from flask_user.email_adapters import EmailAdapterInterface

class SendgridEmailAdapter(EmailAdapterInterface):
    """ Implements the EmailAdapter interface to send emails with SendGrid Web API v3 using sendgrid-python."""
    def __init__(self, app):
        """Check config settings and setup SendGrid Web API v3.

        Args:
            app(Flask): The Flask application instance.
        """

        super(SendgridEmailAdapter, self).__init__(app)

        # Setup sendgrid-python
        try:
            from sendgrid import SendGridAPIClient
        except ImportError:
            raise ConfigError(
                "sendgrid-python has not been installed. Install sendgrid-python with 'pip install sendgrid' or use a different EmailAdapter.")

        pass    # TODO


    def send_email_message(self, recipient, subject, html_message, text_message, sender_email, sender_name):
        """ Send email message via sendgrid-python.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        if not current_app.testing:  # pragma: no cover
            try:
                from sendgrid.helpers.mail import Email, Content, Substitution, Mail
                pass    # TODO
            except ImportError:
                pass    # TODO

