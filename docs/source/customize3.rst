=================
Customizing Three
=================

Level Three customizations require editing of Python files. You must rely on
your own test suites to make sure that Flask-User operations have not been broken.

* `Password and Username validators`_
* `Password hashing`_
* `Token generation`_
* `View functions`_

Password and Username Validators
--------------------------------
Flask-User comes standard
with a password validator (at least 6 chars, 1 upper case letter, 1 lower case letter, 1 digit) and
with a username validator (at least 3 alphanumeric characters).

Custom validators can be specified by setting an attribute on the Flask-User's UserManager object::

    def my_password_validator(form, field):
        password = field.data
        if len(password) < 8:
            raise ValidationError(_('Password must have at least 8 characters'))

    def my_username_validator(form, field):
        username = field.data
        if len(username) < 4:
            raise ValidationError(_('Username must be at least 4 characters long'))
        if not username.isalnum():
            raise ValidationError(_('Username may only contain letters and numbers'))

    user_manager = UserManager(db_adapter)
    user_manager.password_validator = my_password_validator
    user_manager.username_validator = my_username_validator
    user_manager.init_app(app)

Password Hashing
----------------
Flask-User makes use of passlib's CryptContext to provide password hashing.

By default, the following built-in CryptContext is used::
    CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')

You can supply your own CryptContext by setting an attribute on the Flask-User's UserManager object::

    user_manager.crypt_context = my_crypt_context

Token Generation
----------------
To be documented.

View Functions
--------------
The built-in View Functions contain considerable business logic, so we recommend first
trying the approach of Customizing `Form Templates`_
before making use of customized View Functions.

Custom view functions are specified by setting an attribute on the Flask-User's UserManager object::

    # View functions
    user_manager.change_password_view_function
    user_manager.change_username_view_function
    user_manager.confirm_email_view_function
    user_manager.forgot_password_view_function
    user_manager.login_view_function
    user_manager.logout_view_function
    user_manager.register_view_function
    user_manager.resend_confirmation_email_view_function
    user_manager.reset_password_view_function

