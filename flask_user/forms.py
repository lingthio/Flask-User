""" This file defines and validates Flask-User forms. Forms are based on the WTForms module.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

import string
from flask import current_app
from flask_login import current_user

# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField
from wtforms import validators, ValidationError
from .translations import lazy_gettext as _

# **************************
# ** Validation Functions **
# **************************

def password_validator(form, field):
    """ Password must have one lowercase letter, one uppercase letter and one digit. """
    # Convert string to list of characters
    password = list(field.data)
    password_length = len(password)

    # Count lowercase, uppercase and numbers
    lowers = uppers = digits = 0
    for ch in password:
        if ch.islower(): lowers+=1
        if ch.isupper(): uppers+=1
        if ch.isdigit(): digits+=1

    # Password must have one lowercase letter, one uppercase letter and one digit
    is_valid = password_length>=6 and lowers and uppers and digits
    if not is_valid:
        raise ValidationError(_('Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))

def username_validator(form, field):
    """ Username must cont at least 3 alphanumeric characters long"""
    username = field.data
    if len(username) < 3:
        raise ValidationError(_('Username must be at least 3 characters long'))
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._'
    chars = list(username)
    for char in chars:
        if char not in valid_chars:
            raise ValidationError(_("Username may only contain letters, numbers, '-', '.' and '_'"))

def unique_username_validator(form, field):
    """ Username must be unique"""
    user_manager =  current_app.user_manager
    if not user_manager.username_is_available(field.data):
        raise ValidationError(_('This Username is already in use. Please try another one.'))


def unique_email_validator(form, field):
    """ Username must be unique"""
    user_manager =  current_app.user_manager
    if not user_manager.email_is_available(field.data):
        raise ValidationError(_('This Email is already in use. Please try another one.'))

# ***********
# ** Forms **
# ***********

class AddEmailForm(FlaskForm):
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])
    submit = SubmitField(_('Add Email'))

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_('Old Password'), validators=[
        validators.DataRequired(_('Old Password is required')),
        ])
    new_password = PasswordField(_('New Password'), validators=[
        validators.DataRequired(_('New Password is required')),
        ])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))
        ])
    next = HiddenField()
    submit = SubmitField(_('Change password'))

    def validate(self):
        # Use feature config to remove unused form fields
        user_manager =  current_app.user_manager
        if not user_manager.enable_retype_password:
            delattr(self, 'retype_password')

        # Add custom password validator if needed
        has_been_added = False
        for v in self.new_password.validators:
            if v==user_manager.password_validator:
                has_been_added = True
        if not has_been_added:
            self.new_password.validators.append(user_manager.password_validator)

        # Validate field-validators
        if not super(ChangePasswordForm, self).validate():
            return False

        # Verify current_user and current_password
        if not current_user or not user_manager.verify_password(self.old_password.data, current_user):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True

class ChangeUsernameForm(FlaskForm):
    new_username = StringField(_('New Username'), validators=[
        validators.DataRequired(_('Username is required')),
        unique_username_validator,
    ])
    old_password = PasswordField(_('Old Password'), validators=[
        validators.DataRequired(_('Old Password is required')),
    ])
    next = HiddenField()
    submit = SubmitField(_('Change username'))

    def validate(self):
        user_manager =  current_app.user_manager

        # Add custom username validator if needed
        has_been_added = False
        for v in self.new_username.validators:
            if v==user_manager.username_validator:
                has_been_added = True
        if not has_been_added:
            self.new_username.validators.append(user_manager.username_validator)

        # Validate field-validators
        if not super(ChangeUsernameForm, self).validate():
            return False

        # Verify current_user and current_password
        if not current_user or not user_manager.verify_password(self.old_password.data, current_user):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True

class ForgotPasswordForm(FlaskForm):
    email = StringField(_('Your email address'), validators=[
        validators.DataRequired(_('Email address is required')),
        validators.Email(_('Invalid Email address')),
        ])
    submit = SubmitField(_('Send reset password email'))

    def validate_email(form, field):
        user_manager =  current_app.user_manager
        if user_manager.show_username_email_does_not_exist:
            user, user_email = user_manager.find_user_by_email(field.data)
            if not user:
                raise ValidationError(_('%(username_or_email)s does not exist', username_or_email=_('Email')))


class LoginForm(FlaskForm):
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
        if user_manager.enable_username and user_manager.enable_email:
            # Renamed 'Username' label to 'Username or Email'
            self.username.label.text = _('Username or Email')

    def validate(self):
        # Remove fields depending on configuration
        user_manager =  current_app.user_manager
        if user_manager.enable_username:
            delattr(self, 'email')
        else:
            delattr(self, 'username')

        # Validate field-validators
        if not super(LoginForm, self).validate():
            return False

        # Find user by username and/or email
        user = None
        user_email = None
        if user_manager.enable_username:
            # Find user by username
            user = user_manager.find_user_by_username(self.username.data)

            # Find user by email address (username field)
            if not user and user_manager.enable_email:
                user, user_email = user_manager.find_user_by_email(self.username.data)

        else:
            # Find user by email address (email field)
            user, user_email = user_manager.find_user_by_email(self.email.data)

        # Handle successful authentication
        if user and user_manager.get_password(user) and user_manager.verify_password(self.password.data, user):
            return True                         # Successful authentication

        # Handle unsuccessful authentication
        # Email, Username or Email/Username depending on settings
        if user_manager.enable_username and user_manager.enable_email:
            username_or_email_field = self.username
            username_or_email_text = (_('Username/Email'))
        elif user_manager.enable_username:
            username_or_email_field = self.username
            username_or_email_text = (_('Username'))
        else:
            username_or_email_field = self.email
            username_or_email_text = (_('Email'))

        # Show 'username/email does not exist error message
        if user_manager.show_username_email_does_not_exist:
            if not user:
                message = _('%(username_or_email)s does not exist', username_or_email=username_or_email_text)
                username_or_email_field.errors.append(message)
            else:
                self.password.errors.append(_('Incorrect Password'))

        # Hide 'username/email does not exist error message for additional security
        else:
            message = _('Incorrect %(username_or_email)s and/or Password', username_or_email=username_or_email_text)
            username_or_email_field.errors.append(message)
            self.password.errors.append(message)

        return False                                # Unsuccessful authentication


class RegisterForm(FlaskForm):
    password_validator_added = False

    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html

    username = StringField(_('Username'), validators=[
        validators.DataRequired(_('Username is required')),
        unique_username_validator])
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])
    password = PasswordField(_('Password'), validators=[
        validators.DataRequired(_('Password is required'))])
    retype_password = PasswordField(_('Retype Password'), validators=[
        validators.EqualTo('password', message=_('Password and Retype Password did not match'))])
    invite_token = HiddenField(_('Token'))

    submit = SubmitField(_('Register'))

    def validate(self):
        # remove certain form fields depending on user manager config
        user_manager =  current_app.user_manager
        if not user_manager.enable_username:
            delattr(self, 'username')
        if not user_manager.enable_email:
            delattr(self, 'email')
        if not user_manager.enable_retype_password:
            delattr(self, 'retype_password')
        # Add custom username validator if needed
        if user_manager.enable_username:
            has_been_added = False
            for v in self.username.validators:
                if v==user_manager.username_validator:
                    has_been_added = True
            if not has_been_added:
                self.username.validators.append(user_manager.username_validator)
        # Add custom password validator if needed
        has_been_added = False
        for v in self.password.validators:
            if v==user_manager.password_validator:
                has_been_added = True
        if not has_been_added:
            self.password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(RegisterForm, self).validate():
            return False
        # All is well
        return True

class ResendConfirmEmailForm(FlaskForm):
    email = StringField(_('Your email address'), validators=[
        validators.DataRequired(_('Email address is required')),
        validators.Email(_('Invalid Email address')),
        ])
    submit = SubmitField(_('Resend email confirmation email'))

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(_('New Password'), validators=[
        validators.DataRequired(_('New Password is required'))])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))])
    next = HiddenField()
    submit = SubmitField(_('Change password'))

    def validate(self):
        # Use feature config to remove unused form fields
        user_manager =  current_app.user_manager
        if not user_manager.enable_retype_password:
            delattr(self, 'retype_password')
        # Add custom password validator if needed
        has_been_added = False
        for v in self.new_password.validators:
            if v==user_manager.password_validator:
                has_been_added = True
        if not has_been_added:
            self.new_password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(ResetPasswordForm, self).validate():
            return False
        # All is well
        return True

class InviteForm(FlaskForm):
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email'))])
    next = HiddenField()
    submit = SubmitField(_('Invite!'))
