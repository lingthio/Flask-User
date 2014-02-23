=========
Customize
=========
Flask-User can be customized:
- by setting application config settings, or
- by setting an attribute on Flask-User's UserManager object.

Application config settings must be set *before* calling ``user_manager.init_app(app)``.

UserManager attributes must be set *after* calling ``user_manager = UserManager(db_adapter)`` and
*before* calling ``user_manager.init_app(app)``.

Customizing Features
--------------------
Features can be customized through the application's config::

    # Features
    USER_ENABLE_CHANGE_PASSWORD     = True
    USER_ENABLE_CHANGE_USERNAME     = True
    USER_ENABLE_FORGOT_PASSWORD     = True
    USER_ENABLE_REGISTRATION        = True
    USER_REQUIRE_EMAIL_CONFIRMATION = True
    USER_REQUIRE_INVITATION         = False

Customizing Settings
--------------------
Settings can be customized through the application's config::

    # Settings
    USER_CONFIRM_EMAIL_EXPIRATION   = 2*24*3600  # 2 days
    USER_LOGIN_WITH_USERNAME        = False
    USER_REGISTER_WITH_EMAIL        = True
    USER_RESET_PASSWORD_EXPIRATION  = 2*24*3600  # 2 days
    USER_RETYPE_PASSWORD            = True

Customizing URLs
----------------
URLs can be customized through the application's config::

    # URLs
    USER_CHANGE_PASSWORD_URL            = '/user/change-password'
    USER_CHANGE_USERNAME_URL            = '/user/change-username'
    USER_CONFIRM_EMAIL_URL              = '/user/confirm-email/<token>'
    USER_FORGOT_PASSWORD_URL            = '/user/forgot-password'
    USER_LOGIN_URL                      = '/user/login'
    USER_LOGOUT_URL                     = '/user/logout'
    USER_REGISTER_URL                   = '/user/register'
    USER_RESEND_CONFIRMATION_EMAIL_URL  = '/user/resend-confirmation-email'
    USER_RESET_PASSWORD_URL             = '/user/reset-password/<token>'

Customizing Emails
------------------
Emails (subject, HTML message and Text message) can be customized by copying the default email templates to the application's ``templates/flask_user/emails`` dir.

* templates/flask_user/emails/base_[message.html|message.txt|subject.txt]
* templates/flask_user/emails/confirmation_[message.html|message.txt|subject.txt]
* templates/flask_user/emails/reset_password_[message.html|message.txt|subject.txt]

Email templates can make full use of Jinja2.

Common elements can be managed from a single place using the base templates.

Customizing Form Templates
--------------------------
Forms can be customized by copying the default form templates to the application's ``templates/flask_user`` dir.

In addition, the location of each form template file can be set in the application's config::

    # Form template files
    USER_CHANGE_USERNAME_TEMPLATE           = 'flask_user/change_username.html'
    USER_CHANGE_PASSWORD_TEMPLATE           = 'flask_user/change_password.html'
    USER_FORGOT_PASSWORD_TEMPLATE           = 'flask_user/forgot_password.html'
    USER_LOGIN_TEMPLATE                     = 'flask_user/login.html'
    USER_REGISTER_TEMPLATE                  = 'flask_user/register.html'
    USER_RESEND_CONFIRMATION_EMAIL_TEMPLATE = 'flask_user/resend_confirmation_email.html'
    USER_RESET_PASSWORD_TEMPLATE            = 'flask_user/reset_password.html'

Form templates can make full use of Jinja2.

Customizing Form Classes
------------------------
If customizing form templates is not enough, Flask-User allows custom Form classes to be specified by setting
an attribute on the Flask-User's UserManager object::

    # Forms
    user_manager.change_password_form = my_form1
    user_manager.change_username_form = my_form2
    user_manager.forgot_password_form = my_form3
    user_manager.login_form           = my_form4
    user_manager.register_form        = my_form5
    user_manager.reset_password_form  = my_form6

Customizing Validators
----------------------
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

Customizing View Functions
--------------------------
Custom view functions can be specified by setting an attribute on the Flask-User's UserManager object::

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

Customizing Password Hashing Methods
------------------------------------
Flask-User makes use of passlib's CryptContext to provide password hashing.

By default, the following CryptContext is used::
    CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')

You can supply your own CrytpContext by setting an attribute on the Flask-User's UserManager object::

    user_manager.crypt_context = my_crypt_context

