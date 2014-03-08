"""
    flask_user.forms
    ----------------
    This module defines default Flask-User forms.

    Forms are based on the WTForms module.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from flask import current_app
from flask.ext.login import current_user
from flask.ext.wtf import Form

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField
from wtforms import validators, ValidationError

from .translations import lazy_gettext as _

# **************************
# ** Validation Functions **
# **************************

def password_validator(form, field):
    """
    Password must have one lowercase letter, one uppercase letter and one digit.

    A custom password validator can be specified:
        user_manager = UserManager.init(db_adapter)
        user_manager.password_validator = my_custom_password_validator
        user_manager.init_app(app)
    """
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
    """
    Username must cont at least 3 alphanumeric characters long

    A custom username validator can be specified:
        user_manager = UserManager.init(db_adapter)
        user_manager.username_validator = my_custom_username_validator
        user_manager.init_app(app)
    """
    username = field.data
    username_length=len(username)
    if username_length < 3:
        raise ValidationError(_('Username must be at least 3 characters long'))
    if not username.isalnum():
        raise ValidationError(_('Username may only contain letters and numbers'))

def unique_username_validator(form, field):
    """
    Username must be unqiue
    """
    user_manager =  current_app.user_manager
    if not user_manager.db_adapter.username_is_available(field.data):
        raise ValidationError(_('This Username is no longer available. Please try another one.'))


def unique_email_validator(form, field):
    """
    Username must be unqiue
    """
    user_manager =  current_app.user_manager
    if not user_manager.db_adapter.email_is_available(field.data):
        raise ValidationError(_('This Email is no longer available. Please try another one.'))

# ***********
# ** Forms **
# ***********

class ChangeUsernameForm(Form):
    new_username = StringField(_('New Username'), validators=[
        validators.Required(_('Username is required')),
        unique_username_validator,
    ])
    old_password = PasswordField(_('Old Password'), validators=[
        validators.Required(_('Old Password is required')),
    ])
    next = HiddenField()
    submit = SubmitField(_('Change Username'))

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
        if not current_user or not user_manager.password_crypt_context.verify(self.old_password.data, current_user.password):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True


class ChangePasswordForm(Form):
    old_password = PasswordField(_('Old Password'), validators=[
        validators.Required(_('Old Password is required')),
        ])
    new_password = PasswordField(_('New Password'), validators=[
        validators.Required(_('New Password is required')),
        ])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))
        ])
    next = HiddenField()
    submit = SubmitField(_('Change Password'))

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
        if not current_user or not user_manager.password_crypt_context.verify(self.old_password.data, current_user.password):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # All is well
        return True


class ForgotPasswordForm(Form):
    email = StringField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email')),
        ])
    submit = SubmitField(_('Send reset password email'))


class LoginForm(Form):
    username = StringField(_('Username'), validators=[
        validators.Required(_('Username is required')),
    ])
    email = StringField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email'))
    ])
    password = PasswordField(_('Password'), validators=[
        validators.Required(_('Password is required')),
    ])
    remember = BooleanField(_('Remember me'))
    next = HiddenField()
    submit = SubmitField(_('Sign in'))

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

        # Retrieve User by username or email
        if user_manager.enable_username:
            user = user_manager.db_adapter.find_user_by_username(self.username.data)
        else:
            user = user_manager.db_adapter.find_user_by_email(self.email.data)

        # Verify user and password
        if not user or not user_manager.password_crypt_context.verify(self.password.data, user.password):
            if user_manager.enable_username:
                self.username.errors.append(_('Incorrect Username and Password'))
            else:
                self.email.errors.append(_('Incorrect Email and Password'))
            self.password.errors.append('')
            return False

        # All is well
        return True


class RegisterForm(Form):
    password_validator_added = False

    username = StringField(_('Username'), validators=[
        validators.Required(_('Username is required')),
        unique_username_validator,
        ])
    email = StringField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator,
        ])
    password = PasswordField(_('Password'), validators=[
        validators.Required(_('Password is required')),
        ])
    retype_password = PasswordField(_('Retype Password'), validators=[
        validators.EqualTo('password', message=_('Password and Retype Password did not match'))
        ])
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

class ResetPasswordForm(Form):
    new_password = PasswordField(_('New Password'), validators=[
        validators.Required(_('New Password is required')),
        ])
    retype_password = PasswordField(_('Retype New Password'), validators=[
        validators.EqualTo('new_password', message=_('New Password and Retype Password did not match'))
        ])
    next = HiddenField()
    submit = SubmitField(_('Change Password'))

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
