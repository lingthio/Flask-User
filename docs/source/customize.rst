===========
Customizing
===========
Flask-User has been designed with customization in mind, and here is a list of
behaviors that can be customized as needed.

* Emails (Subject lines, HTML messages and Text messages)
* Features and Settings
* Field labels
* Flash messages
* Form classes
* Form templates,
* Password hashing algorithms,
* Token generator,
* URLs
* Validation messages
* Validator (password validator, username validator)
* View functions,

Overview
--------
Built-in Flask-User behavior can be customized in one of two ways:

* by setting an application config setting, or
* by setting a user_manager attribute

::

    # Application Config Settings
    app.config['USER_ENABLE_CONFIRM_EMAIL'] = True                      # Set custom config settings
    app.config['USER_CONFIRM_EMAIL_EXPIRATION'] = 5*24*3600  # 5 days
    user_manager = UserManager(db_adapter)
    user_manager.init_app(app)                                          # Ready to use config settings

    # user_manager attributes
    user_manager = UserManager(db_adapter)                              # Set built-in attributes
    user_manager.password_validator = my_password_validator             # Overwrite custom attributes
    user_manager.username_validator = my_username_validator
    user_manager.init_app(app)                                          # Ready to use attributes

Emails
------
All user management Emails can be customized by copying the default Jinja2 email templates
from flask_user's ``/templates/flask_user/emails`` dir to your application's ``/templates/flask_user/emails`` dir.

Emails are sent as multipart messages with a subject, HTML message body and a Text message body. HTML capable
email clients will display the HTML message body while Text-only email clients will display the Text message body.

Each part has a corresponding base template::

    templates/flask_user/emails/base_subject.txt
    templates/flask_user/emails/base_message.html
    templates/flask_user/emails/base_message.txt

The base templates are used to define email elements that are similar in all types of email messages.

| If, for example, for every email you want to:
| - Set the background color and padding,
| - Start with a logo and salutation, and
| - End with a signature,
| you can define ``templates/flask_user/emails/base_message.html`` like so

::

    <div style="background-color: #f4f2dd; padding: 10px;">
        <p><img src="http://example.com/static/images/email-logo.png"></p>
        <p>Dear Customer,</p>
        {% block message %}{% endblock %}
        <p>Sincerely,<br/>
        The Flask-User Team</p>
    </div>

and define the confirmation specific messages in ``templates/flask_user/emails/confirmation_message.html`` like so::

    {% extends "flask_user/emails/base_message.html" %}

    {% block message %}
    <p>Thank you for registering with Flask-User.</p>
    <p>Visit the link below to complete your registration:</p>
    <p><a href="{{ confirmation_link }}">Confirm your email address</a>.</p>
    <p>If you did not initiate this registration, you may safely ignore this email.</p>
    {% endblock %}

The email template files, along with available template variables listed below:

* templates/flask_user/confirmation_[subject.txt|message.html|message.txt]
    * ``user`` - For example: ``{{ user.email }}``
    * ``confirmation_link`` - For example: ``{{ confirmation_link }}``
* templates/flask_user/reset_password_[subject.txt|message.html|message.txt]
    * ``user`` - For example: ``{{ user.email }}``
    * ``reset_password_link`` - For example: ``{{ reset_password_link }}``

Features and Settings
---------------------
Features and settings can be customized through the application's config::

    # Features                      # Default   # Comments
    USER_ENABLE_CHANGE_PASSWORD     = True      # Allow users to change their password
    USER_ENABLE_CHANGE_USERNAME     = True      # Allow users to change their username
                                                # Only valid if USER_LOGIN_WITH_USERNAME == True
    USER_ENABLE_CONFIRM_EMAIL       = False     # Require users to confirm their email
                                                # Only valid if USER_ENABLE_REGISTRATION == True
    USER_ENABLE_FORGOT_PASSWORD     = False     # Allow users to reset their passwords
    USER_ENABLE_REGISTRATION        = True      # Allow new users to registers
    USER_ENABLE_REQUIRE_INVITATION  = False     # Require an invitation to register new users
                                                # Not yet implemented

    # Settings                      # Default    # Comments
    USER_CONFIRM_EMAIL_EXPIRATION   = 2*24*3600  # Confirmation expiration in seconds (2 days)
    USER_LOGIN_WITH_USERNAME        = False      # Login with username instead of email
    USER_REGISTER_WITH_EMAIL        = True       # Prompt for email during registration
                                                 # Only useful in when USER_LOGIN_WITH_USERNAME == True
                                                 # Must be True if USER_ENABLE_CONFIRM_EMAIL == True
    USER_RESET_PASSWORD_EXPIRATION  = 2*24*3600  # Reset password expiration in seconds (2 days)
    USER_RETYPE_PASSWORD            = True

Field Labels
------------
The built-in Form field labels can be customized by editing the 'en' Babel translation file. [To be documented]

Flash messages
--------------
Flash messages are those one-time system messages that appear on the next page.

| The built-in Flash messages can be customized by editing the 'en' Babel translation file.
| The Flash category (``success``, ``info``, ``warning`` or ``danger``) can not be customized.

[To be documented]

Form Classes
------------
The built-in Form Classes contain considerable form validation logic, so we recommend first
trying the approach of `Customizing Form Templates`_
before making use of customized Form Classes.

Custom Form classes are specified by setting an attribute on the Flask-User's UserManager object::

    # Forms
    user_manager.change_password_form = my_form1
    user_manager.change_username_form = my_form2
    user_manager.forgot_password_form = my_form3
    user_manager.login_form           = my_form4
    user_manager.register_form        = my_form5
    user_manager.reset_password_form  = my_form6

If you do require customized Form Classes, we recommend deriving from the base classes
defined in flask.ext.user.forms and to always call the base validate() function::

    from flask.ext.user.forms import RegisterForm

    MyRegisterForm(RegisterForm):
        # Add custom field
        phone = StringField(Phone')

    def validate():
        if not super(MyRegisterForm, self).validate()
            return False
        # Do some custom form validation
        return True

Form Templates
--------------
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

Password Hashing
----------------
Flask-User makes use of passlib's CryptContext to provide password hashing.

By default, the following built-in CryptContext is used::
    CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')

You can supply your own CryptContext by setting an attribute on the Flask-User's UserManager object::

    user_manager.crypt_context = my_crypt_context

Token Generator
---------------
TBD.

URLs
----
URLs can be customized through the application's config::

    # URLs                              # Defaults
    USER_CHANGE_PASSWORD_URL            = '/user/change-password'
    USER_CHANGE_USERNAME_URL            = '/user/change-username'
    USER_CONFIRM_EMAIL_URL              = '/user/confirm-email/<token>'
    USER_FORGOT_PASSWORD_URL            = '/user/forgot-password'
    USER_LOGIN_URL                      = '/user/login'
    USER_LOGOUT_URL                     = '/user/logout'
    USER_REGISTER_URL                   = '/user/register'
    USER_RESEND_CONFIRMATION_EMAIL_URL  = '/user/resend-confirmation-email'
    USER_RESET_PASSWORD_URL             = '/user/reset-password/<token>'

Validation messages
-------------------
The built-in Form validation messages be customized by editing the 'en' Babel translation file. [To be documented]

Validators
----------
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

View Functions
--------------
The built-in View Functions contain considerable business logic, so we recommend first
trying the approach of `Customizing Form Templates`_
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

