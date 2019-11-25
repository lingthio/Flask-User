""" This file defines and validates Flask-User forms. Forms are based on the WTForms module.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from flask import current_app
from flask_login import current_user

# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField
from wtforms import validators, ValidationError

from .translation_utils import lazy_gettext as _    # map _() to lazy_gettext()


# ****************
# ** Validators **
# ****************

def password_validator(form, field):
    current_app.user_manager.password_validator(form, field)


def username_validator(form, field):
    current_app.user_manager.username_validator(form, field)


def unique_username_validator(form, field):
    """ Ensure that Username is unique. This validator may NOT be customized."""
    user_manager =  current_app.user_manager
    if not user_manager.db_manager.username_is_available(field.data):
        raise ValidationError(_('This Username is already in use. Please try another one.'))


def unique_email_validator(form, field):
    """ Username must be unique. This validator may NOT be customized."""
    user_manager =  current_app.user_manager
    if not user_manager.email_is_available(field.data):
        raise ValidationError(_('This Email is already in use. Please try another one.'))


# ***********
# ** Forms **
# ***********

class AddEmailForm(FlaskForm):
    """Add an email address form."""
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])
    submit = SubmitField(_('Add Email'))


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    old_password = PasswordField(_('Old Password'), validators=[
        validators.DataRequired(_('Old Password is required')),
        ])
    new_password = PasswordField(_('New Password'), validators=[
        validators.DataRequired(_('New Password is required')),
        password_validator,
        ])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))
        ])
    submit = SubmitField(_('Change password'))

    def validate(self):
        # Use feature config to remove unused form fields
        user_manager =  current_app.user_manager
        if not user_manager.USER_REQUIRE_RETYPE_PASSWORD:
            delattr(self, 'retype_password')

        # # Add custom password validator if needed
        # has_been_added = False
        # for v in self.new_password.validators:
        #     if v==user_manager.password_validator:
        #         has_been_added = True
        # if not has_been_added:
        #     self.new_password.validators.append(user_manager.password_validator)

        # Validate field-validators
        if not super(ChangePasswordForm, self).validate(): return False

        # Verify current_user and current_password
        if not current_user or not user_manager.verify_password(self.old_password.data, current_user.password):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True


class ChangeUsernameForm(FlaskForm):
    """Change username form."""
    new_username = StringField(_('New Username'), validators=[
        validators.DataRequired(_('Username is required')),
        username_validator,
        unique_username_validator,
    ])
    old_password = PasswordField(_('Old Password'), validators=[
        validators.DataRequired(_('Old Password is required')),
    ])
    submit = SubmitField(_('Change username'))

    def validate(self):
        user_manager =  current_app.user_manager

        # # Add custom username validator if needed
        # has_been_added = False
        # for v in self.new_username.validators:
        #     if v==user_manager.username_validator:
        #         has_been_added = True
        # if not has_been_added:
        #     self.new_username.validators.append(user_manager.username_validator)

        # Validate field-validators
        if not super(ChangeUsernameForm, self).validate(): return False

        # Verify current_user and current_password
        if not current_user or not user_manager.verify_password(self.old_password.data, current_user.password):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True


class EditUserProfileForm(FlaskForm):
    """Edit user profile form."""

    first_name = StringField(_('First name'), validators=[validators.DataRequired()])
    last_name = StringField(_('Last name'), validators=[validators.DataRequired()])

    submit = SubmitField(_('Update'))


class LoginForm(FlaskForm):
    """Login form."""
    next = HiddenField()         # for login.html
    reg_next = HiddenField()     # for login_or_register.html

    username = StringField(_('Username'), validators=[
        validators.DataRequired(_('Username is required')),
    ])
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email'))
    ])
    password = PasswordField(_('Password'), validators=[
        validators.DataRequired(_('Password is required')),
    ])
    remember_me = BooleanField(_('Remember me'))

    submit = SubmitField(_('Sign in'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        user_manager =  current_app.user_manager
        if user_manager.USER_ENABLE_USERNAME and user_manager.USER_ENABLE_EMAIL:
            # Renamed 'Username' label to 'Username or Email'
            self.username.label.text = _('Username or Email')

    def validate(self):
        # Remove fields depending on configuration
        user_manager =  current_app.user_manager
        if user_manager.USER_ENABLE_USERNAME:
            delattr(self, 'email')
        else:
            delattr(self, 'username')

        # Validate field-validators
        if not super(LoginForm, self).validate():
            return False

        # Find user by username and/or email
        user = None
        user_email = None
        if user_manager.USER_ENABLE_USERNAME:
            # Find user by username
            user = user_manager.db_manager.find_user_by_username(self.username.data)

            # Find user by email address (username field)
            if not user and user_manager.USER_ENABLE_EMAIL:
                user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(self.username.data)

        else:
            # Find user by email address (email field)
            user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(self.email.data)

        # Handle successful authentication
        if user and user_manager.verify_password(self.password.data, user.password):
            return True                         # Successful authentication

        # Handle unsuccessful authentication
        # Email, Username or Email/Username depending on settings
        if user_manager.USER_ENABLE_USERNAME and user_manager.USER_ENABLE_EMAIL:
            username_or_email_field = self.username
            username_or_email_text = (_('Username/Email'))
            show_does_not_exist = user_manager.USER_SHOW_EMAIL_DOES_NOT_EXIST or user_manager.USER_SHOW_USERNAME_DOES_NOT_EXIST
        elif user_manager.USER_ENABLE_USERNAME:
            username_or_email_field = self.username
            username_or_email_text = (_('Username'))
            show_does_not_exist = user_manager.USER_SHOW_USERNAME_DOES_NOT_EXIST
        else:
            username_or_email_field = self.email
            username_or_email_text = (_('Email'))
            show_does_not_exist = user_manager.USER_SHOW_EMAIL_DOES_NOT_EXIST

        # Show 'username/email does not exist' or 'incorrect password' error message
        if show_does_not_exist:
            if not user:
                message = _('%(username_or_email)s does not exist', username_or_email=username_or_email_text)
                username_or_email_field.errors.append(message)
            else:
                self.password.errors.append(_('Incorrect Password'))

        # Always show 'incorrect username/email or password' error message for additional security
        else:
            message = _('Incorrect %(username_or_email)s and/or Password', username_or_email=username_or_email_text)
            username_or_email_field.errors.append(message)
            self.password.errors.append(message)

        return False                                # Unsuccessful authentication


class RegisterForm(FlaskForm):
    """Register new user form."""
    password_validator_added = False

    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html

    username = StringField(_('Username'), validators=[
        validators.DataRequired(_('Username is required')),
        username_validator,
        unique_username_validator])
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])
    password = PasswordField(_('Password'), validators=[
        validators.DataRequired(_('Password is required')),
        password_validator])
    retype_password = PasswordField(_('Retype Password'), validators=[
        validators.EqualTo('password', message=_('Password and Retype Password did not match'))])
    invite_token = HiddenField(_('Token'))

    submit = SubmitField(_('Register'))

    def validate(self):
        # remove certain form fields depending on user manager config
        user_manager =  current_app.user_manager
        if not user_manager.USER_ENABLE_USERNAME:
            delattr(self, 'username')
        if not user_manager.USER_ENABLE_EMAIL:
            delattr(self, 'email')
        if not user_manager.USER_REQUIRE_RETYPE_PASSWORD:
            delattr(self, 'retype_password')
        # # Add custom username validator if needed
        # if user_manager.USER_ENABLE_USERNAME:
        #     has_been_added = False
        #     for v in self.username.validators:
        #         if v==user_manager.username_validator:
        #             has_been_added = True
        #     if not has_been_added:
        #         self.username.validators.append(user_manager.username_validator)
        # # Add custom password validator if needed
        # has_been_added = False
        # for v in self.password.validators:
        #     if v==user_manager.password_validator:
        #         has_been_added = True
        # if not has_been_added:
        #     self.password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(RegisterForm, self).validate():
            return False
        # All is well
        return True


class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""
    email = StringField(_('Your email address'), validators=[
        validators.DataRequired(_('Email address is required')),
        validators.Email(_('Invalid Email address')),
        ])
    submit = SubmitField(_('Send reset password email'))

    def validate_email(form, field):
        user_manager =  current_app.user_manager
        if user_manager.USER_SHOW_EMAIL_DOES_NOT_EXIST:
            user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(field.data)
            if not user:
                raise ValidationError(_('%(username_or_email)s does not exist', username_or_email=_('Email')))


class ResendEmailConfirmationForm(FlaskForm):
    """Resend email confirmation form."""
    email = StringField(_('Your email address'), validators=[
        validators.DataRequired(_('Email address is required')),
        validators.Email(_('Invalid Email address')),
        ])
    submit = SubmitField(_('Resend email confirmation email'))


class ResetPasswordForm(FlaskForm):
    """Reset password form."""
    new_password = PasswordField(_('New Password'), validators=[
        validators.DataRequired(_('New Password is required')),
        password_validator,
        ])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))])
    next = HiddenField()
    submit = SubmitField(_('Change password'))

    def validate(self):
        # Use feature config to remove unused form fields
        user_manager =  current_app.user_manager
        if not user_manager.USER_REQUIRE_RETYPE_PASSWORD:
            delattr(self, 'retype_password')
        # # Add custom password validator if needed
        # has_been_added = False
        # for v in self.new_password.validators:
        #     if v==user_manager.password_validator:
        #         has_been_added = True
        # if not has_been_added:
        #     self.new_password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(ResetPasswordForm, self).validate(): return False
        # All is well
        return True


class InviteUserForm(FlaskForm):
    """Invite new user form."""
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email'))])
    next = HiddenField()
    submit = SubmitField(_('Invite!'))


# Manually Add translation strings from QuickStart apps that use string templates
_sign_in = _('Sign in')
_sign_out = _('Sign out')
_home_page = _('Home Page')
_profile_page = _('User profile')
_member_page = _('Member Page')
_admin_page = _('Admin Page')

