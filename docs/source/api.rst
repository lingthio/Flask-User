Flask-User API
==============
* `UserManager`_
* `SQLAlchemyAdapter()`_
* `Config Settings`_
* `Template variables`_
* `Template functions`_
* `Signals`_

UserManager
-----------

UserManager()
~~~~~~~~~~~~~
::

    from flask_user import UserManager

    user_manager = UserManager(
            app = None,                     # typically from app=Flask() or None

            # Forms
            add_email_form                  = forms.AddEmailForm,
            change_username_form            = forms.ChangeUsernameForm,
            forgot_password_form            = forms.ForgotPasswordForm,
            login_form                      = forms.LoginForm,
            register_form                   = forms.RegisterForm,
            resend_confirm_email_form       = forms.ResendConfirmEmailForm,
            reset_password_form             = forms.ResetPasswordForm,

            # Validators
            username_validator              = forms.username_validator,
            password_validator              = forms.password_validator,

            # View functions
            change_password_view_function   = views.change_password,
            change_username_view_function   = views.change_username,
            confirm_email_view_function     = views.confirm_email,
            email_action_view_function      = views.email_action,
            forgot_password_view_function   = views.forgot_password,
            login_view_function             = views.login,
            logout_view_function            = views.logout,
            manage_emails_view_function     = views.manage_emails,
            register_view_function          = views.register,
            resend_confirm_email_view_function = views.resend_confirm_email_view_function,
            reset_password_view_function    = views.reset_password,
            user_profile_view_function      = views.user_profile,
            unauthenticated_view_function   = views.unauthenticated,
            unauthorized_view_function      = views.unauthorized,

            # Miscellaneous
            login_manager                   = LoginManager(),
            password_crypt_context          = None,
            send_email_function             = emails.send_email,
            token_manager                   = tokens.TokenManager(),
            )

Typical use:

::

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager, SQLAlchemyAdapter

    def create_app():
        app = Flask(__name__)           # Initialize Flask
        db = SQLAlchemy(app)            # Setup SQLAlchemy

        # Define custom UserManager class
        class CustomUserManager(UserManager):
            def customize(self, app):
                # Customize the DB Adapter for SQLAlchemy with this User model
                self.db_adapter = SQLAlchemyAdapter(db, User)
                # Customize Flask-User settings
                self.enable_email = True

        # Setup Flask-User
        user_manager = CustomUserManager(app)

As an a alternative, user_manager.init_app(app) can be used::

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager, SQLAlchemyAdapter

    # Define custom UserManager class
    class CustomUserManager(UserManager):
        def customize(self, app):
            # Customize the DB Adapter for SQLAlchemy with this User model
            self.db_adapter = SQLAlchemyAdapter(db, User)
            # Customize Flask-User settings
            self.enable_email = True

    db = SQLAlchemy(app)                            # Setup SQLAlchemy
    user_manager = CustomUserManager(UserManager)   # Setup Flask-User

    def create_app():
        app = Flask(__name__)           # Initialize Flask
        db.init_app(app)                # Initialize SQLAlchemy
        user_manager.init_app(app)      # Initialize Flask-User

Work in progress. See :doc:`basic_app` for now.

SQLAlchemyAdapter()
-------------------
Flask-User shields itself from database operations through a DBAdapter.
It ships with a SQLAlchemyAdapter, but the API is very simple, so other adapters
can be easily added.

::

    class SQLAlchemyAdapter(DBAdapter):
        """ This object shields Flask-User from database specific functions. """

        def get_object(self, ObjectClass, pk):
            """ Retrieve one object specified by the primary key 'pk' """

        def find_all_objects(self, ObjectClass, **kwargs):
            """ Retrieve all objects matching the case sensitive filters in 'kwargs'. """

        def find_first_object(self, ObjectClass, **kwargs):
            """ Retrieve the first object matching the case sensitive filters in 'kwargs'. """

        def ifind_first_object(self, ObjectClass, **kwargs):
            """ Retrieve the first object matching the case insensitive filters in 'kwargs'. """

        def add_object(self, ObjectClass, **kwargs):
            """ Add an object with fields and values specified in kwargs. """

        def update_object(self, object, **kwargs):
            """ Update an object with fields and values specified in kwargs. """

        def delete_object(self, object):
            """ Delete an object. """

        def commit(self):
            """ Commit an Add, Update or Delete. """

Config Settings
---------------
.. include:: includes/config_features.txt

.. include:: includes/config_settings.txt

.. include:: includes/config_urls.txt

.. include:: includes/config_endpoints.txt

.. include:: includes/config_email_templates.txt

.. include:: includes/config_form_templates.txt

.. _sqlalchemyadapter:

Template variables
------------------
The following template variables are available for use in email and form templates:

.. include:: includes/template_variables.txt

Template functions
------------------
The following template functions are available for use in email and form templates:

.. include:: includes/template_functions.txt

hash_password()
~~~~~~~~~~~~~~~
::

    user_manager.hash_password(password)
    # Returns hashed 'password' using the configured password hash
    # Config settings: USER_PASSWORD_HASH_MODE = 'passlib'
    #                  USER_PASSWORD_HASH      = 'bcrypt'
    #                  USER_PASSWORD_SALT      = SECRET_KEY


verify_password()
~~~~~~~~~~~~~~~~~
::

    user_manager.verify_password(password, user)
    # Returns True if 'password' matches the user's 'hashed password'
    # Returns False otherwise.

Signals
-------
.. include:: includes/signals.txt
