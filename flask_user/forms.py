from flask import current_app
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user
from flask.ext.wtf import Form

from wtforms import BooleanField, HiddenField, PasswordField, SelectField, SubmitField, TextAreaField, TextField
from wtforms import validators, ValidationError

# **************************
# ** Validation Functions **
# **************************

def password_validator(form, field):
    """
    Password must have one lowercase letter, one uppercase letter and one digit
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
    um = current_app.user_manager
    if not um.db_adapter.username_is_available(field.data):
        raise ValidationError(_('This Username is no longer available. Please try another one.'))


def unique_email_validator(form, field):
    """
    Username must be unqiue
    """
    um = current_app.user_manager
    if not um.db_adapter.email_is_available(field.data):
        raise ValidationError(_('This Email is no longer available. Please try another one.'))

# ***********
# ** Forms **
# ***********

class RegisterForm(Form):
    password_validator_added = False

    username = TextField(_('Username'), validators=[
        validators.Required(_('Username is required')),
        username_validator,
        unique_username_validator,
        ])
    email = TextField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator,
        ])
    password = PasswordField(_('Password'), validators=[
        validators.Required(_('Password is required')),
        ])
    retype_password = PasswordField(_('Retype Password'))
    submit = SubmitField(_('Register'))

    def validate(self):
        # Use user_manager config to remove unused form fields
        um = current_app.user_manager
        if um.login_with_username:
            delattr(self, 'email')
        else:
            delattr(self, 'username')
        if not um.register_with_retype_password:
            delattr(self, 'retype_password')

        # Add custom password validator if needed
        has_been_added = False
        for v in self.password.validators:
            if v==um.password_validator:
                has_been_added = True
        if not has_been_added:
            self.password.validators.append(um.password_validator)

        # Validate field-validators
        if not super(RegisterForm, self).validate():
            return False

        # Make sure retype password matches
        if um.register_with_retype_password and self.retype_password.data!=self.password.data:
            self.password.errors.append(_('Password and Retype Password did not match'))
            self.retype_password.errors.append('')
            return False

        # All is well
        return True

class LoginForm(Form):
    username = TextField(_('Username'), validators=[
        validators.Required(_('Username is required')),
    ])
    email = TextField(_('Email'), validators=[
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
        # Use feature config to remove unused form fields
        um = current_app.user_manager
        if um.login_with_username:
            delattr(self, 'email')
        else:
            delattr(self, 'username')

        # Validate field-validators
        if not super(LoginForm, self).validate():
            return False

        # Retrieve User by username or email
        if um.login_with_username:
            user = um.db_adapter.find_user_by_username(self.username.data)
        else:
            user = um.db_adapter.find_user_by_email(self.email.data)

        # Verify user and password
        if not user or not um.crypt_context.verify(self.password.data, user.password):
            if um.login_with_username:
                self.username.errors.append(_('Incorrect Username and Password'))
            else:
                self.email.errors.append(_('Incorrect Email and Password'))
            self.password.errors.append('')
            return False

        # All is well
        return True


class ChangeUsernameForm(Form):
    new_username = TextField(_('New Username'), validators=[
        validators.Required(_('Username is required')),
        username_validator,
        unique_username_validator,
    ])
    old_password = PasswordField(_('Old Password'), validators=[
        validators.Required(_('Old Password is required')),
    ])
    next = HiddenField()
    submit = SubmitField(_('Change Username'))

    def validate(self):
        um = current_app.user_manager

        # Validate field-validators
        if not super(ChangeUsernameForm, self).validate():
            return False

        # Verify current_user and current_password
        if not current_user or not um.crypt_context.verify(self.old_password.data, current_user.password):
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
    retype_password = PasswordField(_('Retype New Password'))
    next = HiddenField()
    submit = SubmitField(_('Change Password'))

    def validate(self):
        # Use feature config to remove unused form fields
        um = current_app.user_manager
        if not um.change_password_with_retype_password:
            delattr(self, 'retype_password')

        # Add custom password validator if needed
        has_been_added = False
        for v in self.new_password.validators:
            if v==um.password_validator:
                has_been_added = True
        if not has_been_added:
            self.new_password.validators.append(um.password_validator)

        # Validate field-validators
        if not super(ChangePasswordForm, self).validate():
            return False

        # Verify current_user and current_password
        if not current_user or not um.crypt_context.verify(self.old_password.data, current_user.password):
            self.old_password.errors.append(_('Old Password is incorrect'))
            return False

        # Make sure retype password matches
        if um.change_password_with_retype_password and self.retype_password.data!=self.new_password.data:
            self.new_password.errors.append(_('New Password and Retype Password did not match'))
            self.retype_password.errors.append('')
            return False

        # All is well
        return True
