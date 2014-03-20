===============
Customize Three
===============

Level Three customizations require editing of Python files. You must rely on
your own test suites to make sure that Flask-User operations have not been broken.

* `Customizing Password and Username validators`_
* `Customizing Password hashing`_
* `Customizing Token generation`_
* `Customizing View functions`_

Customizing Password and Username Validators
--------------------------------------------
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

    user_manager = UserManager(db_adapter,
            password_validator=my_password_validator,
            username_validator=my_username_validator)
    user_manager.init_app(app)

Customizing Password Hashing
----------------------------
Flask-User makes use of passlib's CryptContext to provide password hashing.

**Default CryptContext**

By default, the following built-in CryptContext is used:

::

    CryptContext(schemes=[app.config['USER_PASSWORD_HASH']])

You can change the hashing algorithm by setting an application config setting to any
algorithm supported by passlib:

::

    USER_PASSWORD_HASH = 'pbkdf2_sha512'

See `PassLib Quick Start <http://pythonhosted.org//passlib/new_app_quickstart.html>`_.

**Custom CryptContext**

You can supply your own CryptContext by setting an attribute on the Flask-User's UserManager object:

::

    my_crypt_context = CryptContext(schemes=['bcrypt'])
    user_manager = UserManager(db_adapter,
            password_crypt_context=my_crypt_context)
    user_manager.init_app(app)


**Backward compatibility with Flask-Security**
Flask-Security performs a SHA512 HMAC prior to calling passlib. To continue using passwords that have
been generated with Flask-Security, add the following settings to your application config:

::

    # Keep the following Flask-Security settings
    SECURITY_PASSWORD_HASH = ...
    SECURITY_PASSWORD_SALT = ...

    # Set Flask-Security backward compatibility mode
    USER_PASSWORD_HASH_MODE = 'Flask-Security'
    USER_PASSWORD_HASH      = SECURITY_PASSWORD_HASH
    USER_PASSWORD_SALT      = SECURITY_PASSWORD_SALT

Customizing Token Generation
----------------------------
To be documented.

Customizing View Functions
--------------------------
The built-in View Functions contain considerable business logic, so we recommend first
trying the approach of :ref:`customizingformtemplates`
before making use of customized View Functions.

Custom view functions are specified by setting an attribute on the Flask-User's UserManager object::

    # View functions
    user_manager = UserManager(db_adapter,
            change_password_view_function   =my_view_function1,
            change_username_view_function   =my_view_function2,
            confirm_email_view_function     =my_view_function3,
            forgot_password_view_function   =my_view_function4,
            login_view_function             =my_view_function5,
            logout_view_function            =my_view_function6,
            register_view_function          =my_view_function7,
            reset_password_view_function    =my_view_function8)
    user_manager.init_app(app)

