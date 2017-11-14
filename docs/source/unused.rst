

Misc
====

Status
------

| Flask-User |release| is quite stable and is used in production environments.
| It is marked as a Beta release because the API is subject to small changes.
| We appreciate it if you would enter issues and
  enhancement requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.

.. .. image:: https://img.shields.io/pypi/v/Flask-User.svg
..     :target: https://pypi.python.org/pypi/Flask-User
..
.. .. image:: https://img.shields.io/travis/lingthio/Flask-User.svg
..     :target: https://travis-ci.org/lingthio/Flask-User
..
.. .. image:: https://img.shields.io/pypi/l/Flask-User.svg
..     :target: https://pypi.python.org/pypi/Flask-User

Demo
----
The `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_ showcases Flask-User.
To protect against spam mis-use, all email features have been disabled.
(If you're the first visitor in the last hour, it may take a few seconds for Heroku to start this service)


Contact Information
-------------------
Ling Thio - ling.thio [at] gmail.com

Feeling generous? `Tip me on Gittip <https://www.gittip.com/lingthio/>`_


Revision History
----------------
* v1.0.0 Initial version

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Acknowledgements
----------------
This project would not be possible without the use of the following amazing offerings:

* `Flask <http://flask.pocoo.org/>`_
* `Flask-BabelEx <https://pythonhosted.org/Flask-BabelEx/#flask.ext.babelex.Babel.localeselector>`_ and `Flask-Babel <http://babel.pocoo.org/>`_
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Mail <http://pythonhosted.org/flask-mail/>`_
* `SQLAlchemy <http://www.sqlalchemy.org/>`_ and `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
* `WTForms <http://wtforms.readthedocs.org/en/latest/>`_ and `Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_

Contributors
------------
- https://github.com/neurosnap : Register by invitation only
- https://github.com/lilac : Chinese translation
- https://github.com/cranberyxl : Bugfix for login_endpoint & macros.label
- https://github.com/markosys : Early testing and feedback

Customize
=========

Flask-User has been designed with full customization in mind, and and here is a list of
behaviors that can be customized as needed:

* `Emails`_
* `Registration Form`_
* `Labels and Messages`_
* `Form Templates`_
* `View functions`_
* `Password and Username validators`_
* `Password hashing`_
* `Token generation`_


Labels and Messages
-------------------
The following can be customized by editing the English Babel translation file:

* Flash messages (one-time system messages)
* Form field labels
* Validation messages

See :doc:`internationalization`



Registration Form
-----------------

We recommend asking for as little information as possible during user registration,
and to only prompt new users for additional information *after* the registration process has been completed.

Some Websites, however, do want to ask for additional information in the registration form itself.

Flask-User (v0.4.5 and up) has the capability to store extra registration fields in the User or the UserProfile records.

**Extra registration fields in the User data-model**

Extra fields must be defined in the User data-model::

    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
        email = db.Column(db.String(255), nullable=False, default='')
        password = db.Column(db.String(255), nullable=False, default='')
        # Extra data-model fields
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name  = db.Column(db.String(50), nullable=False, default='')

        def is_active(self):
          return self.is_enabled

    db_adapter = SQLAlchemyAdapter(db, UserClass=User)

A custom RegisterForm must be defined with field names
**exactly matching** the names of the data-model fields::

    class MyRegisterForm(RegisterForm):
        first_name = StringField('First name', validators=[DataRequired('First name is required')])
        last_name  = StringField('Last name',  validators=[DataRequired('Last name is required')])

    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

A custom ``templates/flask_user/register.html`` file must be copied and defined with the extra fields.
See :ref:`customizingformtemplates`.

When a new user submits the Register form, Flask-User examines the field names of the
form and the User data-model. For each matching field name, the form field value
will be stored in the corresponding User field.

`See Github repository; example_apps/register_form_app <https://github.com/lingthio/Flask-User/tree/master/example_apps/register_form_app>`_

**Extra registration fields in UserProfile data-model**

* Add extra fields to the User data-model
* Extend a custom MyRegisterForm class from the built-in flask_user.forms.RegisterForm class.
* Add extra fields to the form **using identical field names**.
* Specify your custom registration form: ``user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)``
* Copy the built-in ``templates/flask_user/register.html`` to your application's templates/flask_user directory.
* Add the extra form fields to register.html



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

    flask_user/_authorized_base.html           # extends base.html
    flask_user/change_password.html       # extends flask_user/_authorized_base.html
    flask_user/change_username.html       # extends flask_user/_authorized_base.html
    flask_user/manage_emails.html         # extends flask_user/_authorized_base.html
    flask_user/edit_user_profile.html          # extends flask_user/_authorized_base.html

    flask_user/_public_base.html           # extends base.html
    flask_user/forgot_password.html       # extends flask_user/_public_base.html
    flask_user/login.html                 # extends flask_user/_public_base.html
    flask_user/login_or_register.html     # extends flask_user/_public_base.html
    flask_user/register.html              # extends flask_user/_public_base.html
    flask_user/request_email_confirmation.html  # extends flask_user/_public_base.html
    flask_user/reset_password.html        # extends flask_user/_public_base.html

If you'd like the Login form and the Register form to appear on one page,
you can use the following application config settings::

    # Place the Login form and the Register form on one page:
    # Only works for Flask-User v0.4.9 and up
    USER_LOGIN_TEMPLATE                     = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE                  = 'flask_user/login_or_register.html'




Password and Username Validators
--------------------------------
Flask-User comes standard
with a password validator (at least 6 chars, 1 upper case letter, 1 lower case letter, 1 digit) and
with a username validator (at least 3 characters in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._").

Custom validators can be specified by setting an property on the Flask-User's UserManager object::

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
            schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'])
    user_manager = UserManager(db_adapter, app,
            password_crypt_context=my_password_crypt_context)

**By sub-classing hash_password()**::

    class MyUserManager(UserManager):
        def hash_password(self, password):
            return self.password

        def verify_password(self, password, password_hash)
            return self.hash_password(password) == password_hash

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

Custom view functions are specified by setting an property on the Flask-User's UserManager object::

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
            resend_email_confirmation_view_function = my_view_function10,
            reset_password_view_function       = my_view_function11,
            )
    user_manager.init_app(app)

Token Generation
----------------
To be documented.



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

.. _CustomizingSQLDbAdapter:

SQLDbAdapter
-------------------
Flask-User uses SQLDbAdapter and installs Flask-SQLAlchemy by default.
No customization is required to work with SQL databases.

Configure the ``SQLALCHEMY_DATABASE_URI`` setting in your app config to point to the desired server and database.

--------

.. _CustomizingMongoDbAdapter:

MongoDbAdapter
--------------------
Flask-User ships with a MongoDbAdapter, but Flask-MongoEngine must be installed manually::

    pip install Flask-MongeEngine

and minor customization is required to use and configure the MongoDbAdapter::

    # Setup Flask-MongoEngine
    from Flask-MongoEngine import MongoEngine
    db = MongoEngine(app)

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided MongoDbAdapter
            from flask_user.db_adapters import MongoDbAdapter
            self.db_adapter = MongoDbAdapter(app, db)

    # Define the User document
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):

        # User authentication information
        username = db.StringField(default='')
        email = db.StringField(default='')
        password = db.StringField()
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configure the ``MONGODB_SETTINGS`` setting in your app config to point to the desired server and database.


--------

.. _CustomizingSMTPEmailAdapter:

SMTPEmailAdapter
----------------
Flask-User uses the SMTPEmailAdapter and install Flask-Mail by default.
No customization is required to use SMTPEmailAdapter to send emails via SMTP.

Configure the ``MAIL_...`` settings in your app config to point to the desired SMTP server and account.

--------

.. _CustomizingSendmailEmailAdapter:

SendmailEmailAdapter
--------------------
Flask-User ships with a SendmailEmailAdapter, but Flask-Sendmail must be installed manually::

    pip install Flask-Sendmail

and minor customization is required use to SendmailEmailAdapter to send emails via ``sendmail``.::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided SendmailEmailAdapter
            from flask_user.email_adapters import SendmailEmailAdapter
            self.email_adapter = SendmailEmailAdapter(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

No configuration is required (other than setting up sendmail on your system).

---------

.. _CustomizingSendgridEmailAdapter:

SendgridEmailAdapter
--------------------
Flask-User ships with a SendgridEmailAdapter, but sendgrid-python needs to be installed manually::

    pip install sendgrid

and minor customization is required to use SendgridEmailAdapter to send emais via SendGrid::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided SendgridEmailAdapter
            from flask_user.email_adapters import SendgridEmailAdapter
            self.email_adapter = SendgridEmailAdapter(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configuration: TBD.

