from flask import current_app
from flask.ext.wtf import Form
from wtforms import BooleanField, HiddenField, PasswordField, SelectField, SubmitField, TextAreaField, TextField
from wtforms import validators, ValidationError

#from flask.ext.babel import lazy_gettext as _
def _(text):
    return text

# **************************
# ** Validation Functions **
# **************************

# Password must have one lowercase letter, one uppercase letter and one digit
def _is_acceptable_password(password_string):
    # Convert string to list of characters
    password = list(password_string)
    password_length = len(password)

    # Count lowercase, uppercase and numbers
    lowers = uppers = digits = 0
    for ch in password:
        if ch.islower(): lowers+=1
        if ch.isupper(): uppers+=1
        if ch.isdigit(): digits+=1

    # Password must have one lowercase letter, one uppercase letter and one digit
    return password_length>=6 and lowers and uppers and digits

# Password must have one lowercase letter, one uppercase letter and one digit
def password_validator(form, field):
    if not _is_acceptable_password(field.data):
        raise ValidationError(_('Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))

# ***********
# ** Forms **
# ***********

class RegisterForm(Form):
    password_validator_added = False
    username = TextField(_('Username'), validators=[
        validators.Required(_('Username is required')),
        validators.Length(min=3, message=_('Username must be at least 3 characters long')),
    ])
    email = TextField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email'))
    ])
    password = PasswordField(_('Password'), validators=[
        validators.Required(_('Password is required')),
    ])
    retype_password = PasswordField(_('Retype Password'))
    submit = SubmitField(_('Sign in'))

    def validate(self):
        # Use user_manager config to remove unused form fields
        um = current_app.user_manager
        if not um.login_with_username:
            delattr(self, 'username')
        if not um.login_with_email:
            delattr(self, 'email')
        if not um.register_with_retype_password:
            delattr(self, 'retype_password')

        # Add custom validator if needed
        has_been_added = False
        for v in self.password.validators:
            if v==um.password_validator:
                has_been_added = True
        if not has_been_added:
            self.password.validators.append(um.password_validator)

        # Validate remaining form fields
        if not super(RegisterForm, self).validate():
            return False

        # Make sure retype password matches
        if um.register_with_retype_password and self.retype_password.data!=self.password.data:
            self.password.errors.append(_('Password and Retype Password do not match'))
            self.retype_password.errors.append('')
            return False
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
        # User feature config to remove unused form fields
        am = current_app.user_manager
        if not am.login_with_username:
            delattr(self, 'username')
        if not am.login_with_email:
            delattr(self, 'email')

        # Validate remaining form fields
        if not super(LoginForm, self).validate():
            return False

        # Retrieve User by username or email
        if am.login_with_username:
            user = am.db_adapter.find_user_by_username(self.username.data)
        elif am.login_with_email:
            user = am.db_adapter.find_user_by_email(self.email.data)
        else:
            user = None

        # Verify user and password
        if not user or not am.crypt_context.verify(self.password.data, user.password):
            if am.login_with_username:
                self.username.errors.append(_('Incorrect Username and Password'))
            elif am.login_with_email:
                self.email.errors.append(_('Incorrect Email and Password'))
            self.password.errors.append('')
            return False

        # All is well
        return True
