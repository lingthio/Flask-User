"""This module implements the EmailManager for Flask-User.
It uses Jinja2 to render email subject and email message.
It uses the EmailAdapter interface to send emails.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from flask import render_template, url_for

from flask_user import ConfigError

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class EmailManager(object):
    """ Send emails via the configured EmailAdapter ``user_manager.email_adapter``. """

    def __init__(self, app):
        """
        Args:
            app(Flask): The Flask application instance.
        """
        self.app = app
        self.user_manager = app.user_manager
        self.sender_name = self.user_manager.USER_EMAIL_SENDER_NAME
        self.sender_email = self.user_manager.USER_EMAIL_SENDER_EMAIL

        # Ensure that USER_EMAIL_SENDER_EMAIL is set
        if not self.sender_email:
            raise ConfigError('Config setting USER_EMAIL_SENDER_EMAIL is missing.')

        # Simplistic email address verification
        if '@' not in self.sender_email:
            raise ConfigError('Config setting USER_EMAIL_SENDER_EMAIL is not a valid email address.')


    def send_confirm_email_email(self, user, user_email):
        """Send the 'email confirmation' email."""
        
        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_ENABLE_CONFIRM_EMAIL: return

        # The confirm_email email is sent to a specific user_email.email or user.email
        email = user_email.email if user_email else user.email

        # Generate a confirm_email_link
        object_id = user_email.id if user_email else user.id
        token = self.user_manager.generate_token(object_id)
        confirm_email_link = url_for('user.confirm_email', token=token, _external=True)

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_CONFIRM_EMAIL_TEMPLATE,
            confirm_email_link=confirm_email_link,
        )

    def send_password_changed_email(self, user):
        """Send the 'password has changed' notification email."""

        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_SEND_PASSWORD_CHANGED_EMAIL: return

        # Notification emails are sent to the user's primary email address
        user_or_user_email_object = self.user_manager.db_manager.get_primary_user_email_object(user)
        email = user_or_user_email_object.email

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_PASSWORD_CHANGED_EMAIL_TEMPLATE,
        )

    def send_reset_password_email(self, user, user_email):
        """Send the 'reset password' email."""

        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        assert self.user_manager.USER_ENABLE_FORGOT_PASSWORD

        # The reset_password email is sent to a specific user_email.email or user.email
        email = user_email.email if user_email else user.email

        # Generate a reset_password_link
        token = self.user_manager.generate_token(user.id)
        reset_password_link = url_for('user.reset_password', token=token, _external=True)

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_RESET_PASSWORD_EMAIL_TEMPLATE,
            reset_password_link=reset_password_link,
        )

    def send_invite_user_email(self, user, user_invitation):
        """Send the 'user invitation' email."""

        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_ENABLE_INVITE_USER: return

        # The user param points to the inviter
        # The user_invitation param points to the invitee
        invited_by_user = user

        # Use the invitation email
        email = user_invitation.email

        # Create a dummy user object to an empty name for the invitee
        user = self.user_manager.db_manager.UserClass(email=email)

        # Generate a accept_invitation_link
        token = self.user_manager.generate_token(user_invitation.id)
        accept_invitation_link = url_for('user.register', token=token, _external=True)

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_INVITE_USER_EMAIL_TEMPLATE,
            accept_invitation_link=accept_invitation_link,
            invited_by_user=invited_by_user,
        )

    def send_registered_email(self, user, user_email, request_email_confirmation):
        """Send the 'user has registered' notification email."""

        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_SEND_REGISTERED_EMAIL: return

        # The registered email is sent to a specific user_email.email or user.email
        email = user_email.email if user_email else user.email

        # Add a request to confirm email if needed
        if request_email_confirmation:
            # Generate a confirm_email_link
            token = self.user_manager.generate_token(user_email.id if user_email else user.id)
            confirm_email_link = url_for('user.confirm_email', token=token, _external=True)
        else:
            confirm_email_link = None

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_REGISTERED_EMAIL_TEMPLATE,
            confirm_email_link=confirm_email_link,
        )

    def send_username_changed_email(self, user):
        """Send the 'username has changed' notification email."""

        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_SEND_USERNAME_CHANGED_EMAIL: return

        # Notification emails are sent to the user's primary email address
        user_or_user_email_object = self.user_manager.db_manager.get_primary_user_email_object(user)
        email = user_or_user_email_object.email

        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_USERNAME_CHANGED_EMAIL_TEMPLATE,
        )

    def _render_and_send_email(self, email, user, template_filename, **kwargs):
        # Add some variables to the template context
        kwargs['app_name'] = self.user_manager.USER_APP_NAME
        kwargs['email'] = email
        kwargs['user'] = user
        kwargs['user_manager'] = self.user_manager

        # Render subject and remove newlines from subject
        subject = render_template(template_filename+'_subject.txt', **kwargs)
        subject = subject.replace('\n', ' ')
        subject = subject.replace('\r', ' ')
        # Render HTML message
        html_message = render_template(template_filename+'_message.html', **kwargs)
        # Render text message
        text_message = render_template(template_filename+'_message.txt', **kwargs)

        # Send email via configured EmailAdapter
        self.user_manager.email_adapter.send_email_message(
            email, subject, html_message, text_message,
            self.sender_email, self.sender_name)


