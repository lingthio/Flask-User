Customization
=============
Flask-User has been designed with full customization in mind, and and here is a list of
behaviors that can be customized as needed:

* `Features`_
* `Settings`_
* `Emails`_
* `Registration Form`_
* `Labels and Messages`_
* `Form Classes`_
* `Form Templates`_
* `View functions`_
* `Password and Username validators`_
* `Password hashing`_
* `URLs`_
* `Endpoints`_
* `Email template filenames`_
* `Form template filenames`_
* `Token generation`_


Features
--------
The following Features can be customized through the application's config:

.. include:: includes/config_features.txt

The following config settings have been renamed and are now obsolete. Please rename to the new setting.

::

    # Obsoleted setting             # New setting
    USER_ENABLE_EMAILS              USER_ENABLE_EMAIL
    USER_ENABLE_USERNAMES           USER_ENABLE_USERNAME
    USER_ENABLE_RETYPE_PASSWORDS    USER_ENABLE_RETYPE_PASSWORD
    USER_LOGIN_WITH_USERNAME        USER_ENABLE_USERNAME
    USER_REGISTER_WITH_EMAIL        USER_ENABLE_EMAIL
    USER_RETYPE_PASSWORD            USER_ENABLE_RETYPE_PASSWORD


Settings
--------
The following Settings can be customized through the application's config:

.. include:: includes/config_settings.txt

Labels and Messages
-------------------
The following can be customized by editing the English Babel translation file:

* Flash messages (one-time system messages)
* Form field labels
* Validation messages

See :doc:`internationalization`


Emails
------
Emails are generated using Flask Jinja2 template files.
Flask will first look for template files in the application's ``templates`` directory
before looking in Flask-User's ``templates`` directory.

Emails can thus be customized by copying the built-in Email template files
from the Flask-User directory to your application's directory
and editing the new copy.

Flask-User typically installs in the ``flask_user`` sub-directory of the Python packages directory.
The location of this directory depends on Python, virtualenv and pip
and can be determined with the following command::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

Let's assume that:

* The Python packages dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/``
* The Flask-User dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/``
* Your app directory is: ``~/path/to/YOURAPP/YOURAPP``
  (your application directory typically contains the 'static' and 'templates' sub-directories).

The built-in Email template files can be copied like so::

    cd ~/path/to/YOURAPP/YOURAPP
    mkdir -p templates/flask_user/emails
    cp ~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/emails/* templates/flask_user/emails/.

Flask-User currently offers the following email messages::

    confirm_email     # Sent after a user submitted a registration form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CONFIRM_EMAIL = True

    forgot_password   # Sent after a user submitted a forgot password form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_FORGOT_PASSWORD = True

    password_changed  # Sent after a user submitted a change password or reset password form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CHANGE_PASSWORD = True
                      # - Requires USER_SEND_PASSWORD_CHANGED_EMAIL = True

    registered        # Sent to users after they submitted a registration form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CONFIRM_EMAIL = False
                      # - Requires USER_SEND_REGISTERED_EMAIL = True

    username_changed  # Sent after a user submitted a change username form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CHANGE_USERNAME = True
                      # - Requires USER_SEND_USERNAME_CHANGED_EMAIL = True

Each email type has three email template files.
The 'registered' email for example has the following files::

    templates/flask_user/emails/registered_subject.txt   # The email subject line
    templates/flask_user/emails/registered_message.html  # The email message in HTML format
    templates/flask_user/emails/registered_message.txt   # The email message in Text format

Each file is extended from the base template file::

    templates/flask_user/emails/base_subject.txt
    templates/flask_user/emails/base_message.html
    templates/flask_user/emails/base_message.txt

The base template files are used to define email elements that are similar in all types of email messages.

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

and define the confirmation specific messages in ``templates/flask_user/emails/confirm_email_message.html`` like so::

    {% extends "flask_user/emails/base_message.html" %}

    {% block message %}
    <p>Thank you for registering with Flask-User.</p>
    <p>Visit the link below to complete your registration:</p>
    <p><a href="{{ confirm_email_link }}">Confirm your email address</a>.</p>
    <p>If you did not initiate this registration, you may safely ignore this email.</p>
    {% endblock %}

The email template files, along with available template variables listed below:

* Template variables available in any email template
    * ``user_manager`` - For example: ``{% if user_manager.enable_confirm_email %}``
    * ``user`` - For example: ``{{ user.email }}``
* templates/flask_user/confirm_email_[subject.txt|message.html|message.txt]
    * ``confirm_email_link`` - For example: ``{{ confirm_email_link }}``
* templates/flask_user/forgot_password_[subject.txt|message.html|message.txt]
    * ``reset_password_link`` - For example: ``{{ reset_password_link }}``
* templates/flask_user/password_changed_[subject.txt|message.html|message.txt]
    * n/a
* templates/flask_user/registered_[subject.txt|message.html|message.txt]
    * n/a
* templates/flask_user/username_changed_[subject.txt|message.html|message.txt]
    * n/a

If you need other email notifications, please enter a feature request to our Github issue tracker. Thank you.


Registration Form
-----------------

We recommend asking for as little information as possible during user registration,
and to only prompt new users for additional information *after* the registration process has been completed.

Some Websites, however, do want to ask for additional information in the registration form itself.

Flask-User (v0.4.5 and up) has the capability to store extra registration fields in the User or the UserProfile records.

**Extra registration fields in the User model**

Extra fields must be defined in the User model::

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
        email = db.Column(db.String(255), nullable=False, default='')
        password = db.Column(db.String(255), nullable=False, default='')
        # Extra model fields
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name  = db.Column(db.String(50), nullable=False, default='')

        def is_active(self):
          return self.is_enabled

    db_adapter = SQLAlchemyAdapter(db, UserClass=User)

A custom RegisterForm must be defined with field names
**exactly matching** the names of the model fields::

    class MyRegisterForm(RegisterForm):
        first_name = StringField('First name', validators=[Required('First name is required')])
        last_name  = StringField('Last name',  validators=[Required('Last name is required')])

    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

A custom ``templates/flask_user/register.html`` file must be copied and defined with the extra fields.
See :ref:`customizingformtemplates`.

When a new user submits the Register form, Flask-User examines the field names of the
form and the User model. For each matching field name, the form field value
will be stored in the corresponding User field.

`See Github repository; example_apps/register_form_app <https://github.com/lingthio/Flask-User/tree/master/example_apps/register_form_app>`_

**Extra registration fields in UserProfile model**

* Add extra fields to the User data model
* Extend a custom MyRegisterForm class from the built-in flask.ext.user.forms.RegisterForm class.
  See :ref:`customizingformclasses`.
* Add extra fields to the form **using identical field names**.
* Specify your custom registration form: ``user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)``
* Copy the built-in ``templates/flask_user/register.html`` to your application's templates/flask_user directory.
  See :ref:`customizingformtemplates`.
* Add the extra form fields to register.html


.. _customizingformclasses:

Form Classes
------------

Forms can be customized by sub-classing one of the following built-in Form classes::

    flask.ext.user.forms.AddEmailForm
    flask.ext.user.forms.ChangeUsernameForm
    flask.ext.user.forms.ChangePasswordForm
    flask.ext.user.forms.ForgotPasswordForm
    flask.ext.user.forms.LoginForm
    flask.ext.user.forms.RegisterForm
    flask.ext.user.forms.ResetPasswordForm

and specifying the custom form in the call to UserManager()::

    from flask.ext.user.forms import RegisterForm

    class MyRegisterForm(RegisterForm):
        first_name = StringField('First name')
        last_name = StringField('Last name')

    user_manager = UserManager(db_adapter, app,
            register_form = MyRegisterForm)

See also :ref:`customizingformtemplates`.


.. _customizingformtemplates:

Form Templates
--------------
Forms are generated using Flask Jinja2 template files.
Flask will first look for template files in the application's ``templates`` directory
before looking in Flask-User's ``templates`` directory.

Forms can thus be customized by copying the built-in Form template files
from the Flask-User directory to your application's directory
and editing the new copy.

Flask-User typically installs in the ``flask_user`` sub-directory of the Python packages directory.
The location of this directory depends on Python, virtualenv and pip
and can be determined with the following command::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

Let's assume that:

* The Python packages dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/``
* The Flask-User dir is: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/``
* Your app directory is: ``~/path/to/YOURAPP/YOURAPP``
  (your application directory typically contains the 'static' and 'templates' sub-directories).

Forms can be customized by copying the form template files like so::

    cd ~/path/to/YOURAPP/YOURAPP
    mkdir -p templates/flask_user
    cp ~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/*.html templates/flask_user/.

and by editing the copies to your liking.

The following form template files resides in the ``templates`` directory and can be customized::

    base.html                             # root template

    flask_user/member_base.html           # extends base.html
    flask_user/change_password.html       # extends flask_user/member_base.html
    flask_user/change_username.html       # extends flask_user/member_base.html
    flask_user/manage_emails.html         # extends flask_user/member_base.html
    flask_user/user_profile.html          # extends flask_user/member_base.html

    flask_user/public_base.html           # extends base.html
    flask_user/forgot_password.html       # extends flask_user/public_base.html
    flask_user/login.html                 # extends flask_user/public_base.html
    flask_user/login_or_register.html     # extends flask_user/public_base.html
    flask_user/register.html              # extends flask_user/public_base.html
    flask_user/resend_confirm_email.html  # extends flask_user/public_base.html
    flask_user/reset_password.html        # extends flask_user/public_base.html

If you'd like the Login form and the Register form to appear on one page,
you can use the following application config settings::

    # Place the Login form and the Register form on one page:
    # Only works for Flask-User v0.4.9 and up
    USER_LOGIN_TEMPLATE                     = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE                  = 'flask_user/login_or_register.html'


See also :ref:`customizingformclasses`.


Password and Username Validators
--------------------------------
Flask-User comes standard
with a password validator (at least 6 chars, 1 upper case letter, 1 lower case letter, 1 digit) and
with a username validator (at least 3 characters in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._").

Custom validators can be specified by setting an attribute on the Flask-User's UserManager object::

    from wtforms.validators import ValidationError

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

    user_manager = UserManager(db_adapter,
            password_validator=my_password_validator,
            username_validator=my_username_validator)
    user_manager.init_app(app)

Password hashing
----------------

To hash a password, Flask-User:

* calls ``user_manager.hash_password()``,
* which calls ``user_manager.password_crypt_context``,
* which is initialized to ``CryptContext(schemes=[app.config['USER_PASSWORD_HASH']])``,
* where ``USER_PASSWORD_HASH = 'bcrypt'``.

See http://pythonhosted.org/passlib/new_app_quickstart.html

Developers can customize the password hashing in the following ways:

**By changing an application config setting**::

    USER_PASSWORD_HASH = 'sha512_crypt'

**By changing the crypt_context**::

    my_password_crypt_context = CryptContext(
            schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512', 'plaintext'])
    user_manager = UserManager(db_adapter, app,
            password_crypt_context=my_password_crypt_context)

**By sub-classing hash_password()**::

    class MyUserManager(UserManager):
        def hash_password(self, password):
            return self.password

        def verify_password(self, password, user)
            return self.hash_password(password) == self.get_password(user)

**Backward compatibility with Flask-Security**

Flask-Security performs a SHA512 HMAC prior to calling passlib. To continue using passwords that have
been generated with Flask-Security, add the following settings to your application config:

::

    # Keep the following Flaks and Flask-Security settings the same
    SECRET_KEY = ...
    SECURITY_PASSWORD_HASH = ...
    SECURITY_PASSWORD_SALT = ...

    # Set Flask-Security backward compatibility mode
    USER_PASSWORD_HASH_MODE = 'Flask-Security'
    USER_PASSWORD_HASH      = SECURITY_PASSWORD_HASH
    USER_PASSWORD_SALT      = SECURITY_PASSWORD_SALT

View Functions
--------------
The built-in View Functions contain considerable business logic, so we recommend first
trying the approach of :ref:`customizingformtemplates`
before making use of customized View Functions.

Custom view functions are specified by setting an attribute on the Flask-User's UserManager object::

    # View functions
    user_manager = UserManager(db_adapter,
            change_password_view_function      = my_view_function1,
            change_username_view_function      = my_view_function2,
            confirm_email_view_function        = my_view_function3,
            email_action_view_function         = my_view_function4,
            forgot_password_view_function      = my_view_function5,
            login_view_function                = my_view_function6,
            logout_view_function               = my_view_function7,
            manage_emails_view_function        = my_view_function8,
            register_view_function             = my_view_function9,
            resend_confirm_email_view_function = my_view_function10,
            reset_password_view_function       = my_view_function11,
            )
    user_manager.init_app(app)

URLs
----
URLs can be customized through the application's config

.. include:: includes/config_urls.txt


Endpoints
---------
Endpoints can be customized through the application's config

.. include:: includes/config_endpoints.txt


Email Template filenames
------------------------
Email template filenames can be customized through the application's config

.. include:: includes/config_email_templates.txt

These path settings are relative to the application's ``templates`` directory.


Form Template filenames
-----------------------
Form template filenames can be customized through the application's config

.. include:: includes/config_form_templates.txt

These path settings are relative to the application's ``templates`` directory.

Token Generation
----------------
To be documented.




