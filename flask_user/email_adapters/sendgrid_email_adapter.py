"""This module implements the EmailAdapter interface for SendGrid.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user import current_app, ConfigError
from flask_user.email_adapters import EmailAdapterInterface

SENDGRID_IMPORT_ERROR_MESSAGE = 'The sendgrid package is missing. Install sendgrid with "pip install sendgrid".'

class SendgridEmailAdapter(EmailAdapterInterface):
    """ Implements the EmailAdapter interface to send emails with SendGrid Web API v3 using sendgrid-python."""
    def __init__(self, app):
        """Check config settings and setup SendGrid Web API v3.

        Args:
            app(Flask): The Flask application instance.
        """

        super(SendgridEmailAdapter, self).__init__(app)

        sendgrid_api_key = app.config.get('SENDGRID_API_KEY')
        if not sendgrid_api_key:
            raise ConfigError(
                "The SENDGRID_API_KEY setting is missing. Set SENDGRID_API_KEY in your app config.")

        # Setup sendgrid-python
        try:
            from sendgrid import SendGridAPIClient
            self.sg = SendGridAPIClient(apikey=sendgrid_api_key)
        except ImportError:
            raise ConfigError(SENDGRID_IMPORT_ERROR_MESSAGE)


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
                # Prepare Sendgrid helper objects
                from sendgrid.helpers.mail import Email, Content, Substitution, Mail
                from_email = Email(sender_email, sender_name)
                to_email = Email(recipient)
                text_content = Content('text/plain', text_message)
                html_content = Content('text/html', html_message)
                # Prepare Sendgrid Mail object
                # Note: RFC 1341: text must be first, followed by html
                mail = Mail(from_email, subject, to_email, text_content)
                mail.add_content(html_content)
                # Send mail via the Sendgrid API
                response = self.sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except ImportError:
                raise ConfigError(SENDGRID_IMPORT_ERROR_MESSAGE)
            except Exception as e:
                print(e)
                print(e.body)
                raise

