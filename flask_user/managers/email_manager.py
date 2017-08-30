""" This file contains email sending functions for Flask-User.
    It uses Jinja2 to render email subject and email message. It uses Flask-Mail to send email.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


import smtplib
import socket
from flask import current_app, render_template

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class EmailManager(object):
    """ SendEmailMixin provides email sending methods using Flask-Mail """

    def __init__(self, user_manager, send_email_function):
        self.user_manager = user_manager
        self.send_email_function = send_email_function
        if not self.send_email_function:
            self.send_email_function = self.send_email

    def send_email(self, recipient, subject, html_message, text_message):
        # Send email using the configured EmailAdapter.
        self.user_manager.email_adapter.send_email_message(
            recipient, subject, html_message, text_message,
        )

    def send_email_confirm_email(self, user, user_email, confirm_email_link):
        # Verify certain conditions
        if not self.user_manager.enable_email: return
        if not self.user_manager.send_registered_email and not self.user_manager.enable_confirm_email: return

        # Retrieve email address from User or UserEmail object
        email = user_email.email if user_email else user.email
        assert(email)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.confirm_email_email_template,
                user=user,
                app_name=self.user_manager.app_name,
                confirm_email_link=confirm_email_link)

        # Send email message using Flask-Mail
        self.send_email_function(email, subject, html_message, text_message)

    def send_email_forgot_password(self, user, user_email, reset_password_link):
        # Verify certain conditions
        if not self.user_manager.enable_email: return
        assert self.user_manager.enable_forgot_password

        # Retrieve email address from User or UserEmail object
        email = user_email.email if user_email else user.email
        assert(email)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.forgot_password_email_template,
                user=user,
                app_name=self.user_manager.app_name,
                reset_password_link=reset_password_link)

        # Send email message using Flask-Mail
        self.send_email_function(email, subject, html_message, text_message)

    def send_email_password_changed(self, user):
        # Verify certain conditions
        if not self.user_manager.enable_email: return
        if not self.user_manager.send_password_changed_email: return

        # Retrieve email address from User or UserEmail object
        user_email = self.get_primary_user_email(user)
        assert(user_email)
        email = user_email.email
        assert(email)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.password_changed_email_template,
                user=user,
                app_name=self.user_manager.app_name)

        # Send email message using Flask-Mail
        self.send_email_function(email, subject, html_message, text_message)

    def send_email_registered(self, user, user_email, confirm_email_link):    # pragma: no cover
        # Verify certain conditions
        if not self.user_manager.enable_email: return
        if not self.user_manager.send_registered_email: return

        # Retrieve email address from User or UserEmail object
        email = user_email.email if user_email else user.email
        assert(email)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.registered_email_template,
                user=user,
                app_name=self.user_manager.app_name,
                confirm_email_link=confirm_email_link)

        # Send email message using Flask-Mail
        self.send_email_function(email, subject, html_message, text_message)

    def send_email_username_changed(self, user):  # pragma: no cover
        # Verify certain conditions
        if not self.user_manager.enable_email: return
        if not self.user_manager.send_username_changed_email: return

        # Retrieve email address from User or UserEmail object
        user_email = self.get_primary_user_email(user)
        assert(user_email)
        email = user_email.email
        assert(email)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.username_changed_email_template,
                user=user,
                app_name=self.user_manager.app_name)

        # Send email message using Flask-Mail
        self.send_email_function(email, subject, html_message, text_message)

    def send_email_invite(self, user, accept_invite_link):
        if not self.user_manager.enable_email: return

        # Render subject, html message and text message
        subject, html_message, text_message = _render_email(
                self.user_manager.invite_email_template,
                user=user,
                app_name=self.user_manager.app_name,
                accept_invite_link=accept_invite_link)

        # Send email message using Flask-Mail
        self.send_email_function(user.email, subject, html_message, text_message)



def send_email_via_flask_mail(recipient, subject, html_message, text_message):
    """ Send email via Flask-Mail.

    Args:
        recipient: Email address or tuple of (Name, Email-address).
        subject: Subject line.
        html_message: The message body in HTML.
        text_message: The message body in plain text.
    """

    # Define the SendMailError exception
    class SendEmailError(Exception):
        pass

    # Make sure that Flask-Mail has been installed
    try:
        from flask_mail import Message
    except:
        raise SendEmailError("Flask-Mail has not been installed. Use 'pip install Flask-Mail' to install Flask-Mail.")

    # Make sure that Flask-Mail has been initialized
    mail_engine = current_app.extensions.get('mail', None)
    if not mail_engine:
        raise SendEmailError(
            'Flask-Mail has not been initialized. Initialize Flask-Mail or disable USER_SEND_PASSWORD_CHANGED_EMAIL, USER_SEND_REGISTERED_EMAIL and USER_SEND_USERNAME_CHANGED_EMAIL')

    try:

        # Construct Flash-Mail message
        message = Message(subject,
                          recipients=[recipient],
                          html=html_message,
                          body=text_message)
        mail_engine.send(message)

    # Print helpful error messages on exceptions
    except (socket.gaierror, socket.error) as e:
        raise SendEmailError('SMTP Connection error: Check your MAIL_SERVER and MAIL_PORT settings.')
    except smtplib.SMTPAuthenticationError:
        raise SendEmailError('SMTP Authentication error: Check your MAIL_USERNAME and MAIL_PASSWORD settings.')


def _render_email(filename, **kwargs):
    # Render subject
    subject = render_template(filename+'_subject.txt', **kwargs)
    # Make sure that subject lines do not contain newlines
    subject = subject.replace('\n', ' ')
    subject = subject.replace('\r', ' ')
    # Render HTML message
    html_message = render_template(filename+'_message.html', **kwargs)
    # Render text message
    text_message = render_template(filename+'_message.txt', **kwargs)

    return (subject, html_message, text_message)

