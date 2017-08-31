""" Flask-User is a customizable user account management extension for Flask.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.



from flask import Blueprint, current_app, Flask, render_template
from flask_login import LoginManager, current_user

from flask_user.email_manager import EmailManager
from flask_user.password_manager import PasswordManager
from flask_user.token_manager import TokenManager
from . import forms
from . import translations
from . import views
from .translations import get_translations

__version__ = '0.9'


def _call_or_get(function_or_property):
    return function_or_property() if callable(function_or_property) else function_or_property


def _flask_user_context_processor():
    """ Make 'user_manager' available to Jinja2 templates"""
    return dict(
        user_manager=current_app.user_manager,
        call_or_get=_call_or_get)


# Define custom Exception
class ConfigurationError(Exception):
    pass




    # The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class UserManager():
    """ Customizable User Authentication and Management.
    """

    # ***** default config settings *****

    Section_one = "Default feature settings." #:

    #: | Allow users to login and register with an email address
    USER_ENABLE_EMAIL = True

    #: | Require users to confirm their email.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_CONFIRM_EMAIL = True

    #: | Allow users to associate multiple email addresses with one user account.
    #: | Depends on USER_ENABLE_EMAIL=True
    USER_ENABLE_MULTIPLE_EMAILS = False

    #: | Allow users to login without a confirmed email address.
    #: | Depends on USER_ENABLE_EMAIL=True.
    #: | Make sure to protect vulnerable views using @confirm_email_required.
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = False


    #: | Allow users to login and register with a username
    USER_ENABLE_USERNAME = True

    #: | Allow users to change their username or not.
    #: | Depends on USER_ENABLE_USERNAME=True.
    USER_ENABLE_CHANGE_USERNAME = True


    #: | Allow users to change their password.
    USER_ENABLE_CHANGE_PASSWORD = True

    #: | Allow users to reset their passwords.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_FORGOT_PASSWORD = True

    #: | Require users to retype their password.
    #: | Affects registration, change password and reset password forms.
    USER_ENABLE_RETYPE_PASSWORD = True


    #: | Allow unknown users to register.
    USER_ENABLE_REGISTER = True

    #: | Remember user sessions across browser restarts.
    USER_ENABLE_REMEMBER_ME = True,

    Section_two = "Default settings." #:

    #: The application name displayed in email templates and page template footers.
    USER_APP_NAME = 'USER_APP_NAME'


    #: Automatic sign-in if the user session has not expired.
    USER_AUTO_LOGIN = True

    #: Automatic sign-in after a user confirms their email address.
    USER_AUTO_LOGIN_AFTER_CONFIRM = True

    #: Automatic sign-in after a user registers.
    USER_AUTO_LOGIN_AFTER_REGISTER = True

    #: Automatic sign-in after a user resets their password.
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True

    #: Automatic sign-in at the login form (if the user session has not expired).
    USER_AUTO_LOGIN_AT_LOGIN = True

    #: | Send notification email after a password change.
    #: | Requires USER_ENABLE_EMAIL=True.
    USER_SEND_PASSWORD_CHANGED_EMAIL = True

    #: | Send notification email after a registration.
    #: | Requires USER_ENABLE_EMAIL=True.
    USER_SEND_REGISTERED_EMAIL = True

    #: | Send notification email after a username change.
    #: | Requires USER_ENABLE_EMAIL=True.
    USER_SEND_USERNAME_CHANGED_EMAIL = True

    #: Password hash scheme.
    #: Accepts valid pass hash schemes such as 'bcrypt', 'pbkdf2_sha512', 'sha512_crypt' or 'argon2'.
    USER_PASSWORD_HASH = 'bcrypt'

    #: | Only invited users may register.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_REQUIRE_INVITATION = False

    #: | Show 'Email does not exist' message instead of 'Incorrect Email or password'.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SHOW_EMAIL_DOES_NOT_EXIST = False

    #: | Show 'Username does not exist' message instead of 'Incorrect Username or password'.
    #: | Depends on USER_ENABLE_USERNAME=True.
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False

    #: | Email confirmation token expiration in seconds.
    #: | Default is 2 days (2*24*3600 seconds).
    USER_CONFIRM_EMAIL_EXPIRATION = 2*24*3600

    #: | Invitation token expiration in seconds.
    #: | Default is 90 days (90*24*3600 seconds).
    USER_INVITE_EXPIRATION = 90*24*3600

    #: | Reset password token expiration in seconds.
    #: | Default is 2 days (2*24*3600 seconds).
    USER_RESET_PASSWORD_EXPIRATION = 2*24*3600

    Section_three = "Default URLs." #:

    USER_CHANGE_PASSWORD_URL = '/user/change-password' #:
    USER_CHANGE_USERNAME_URL = '/user/change-username' #:
    USER_CONFIRM_EMAIL_URL = '/user/confirm-email/<token>' #:
    USER_EMAIL_ACTION_URL = '/user/email/<id>/<action>' #:
    USER_FORGOT_PASSWORD_URL = '/user/forgot-password' #:
    USER_INVITE_URL = '/user/invite' #:
    USER_LOGIN_URL = '/user/sign-in' #:
    USER_LOGOUT_URL = '/user/sign-out' #:
    USER_MANAGE_EMAILS_URL = '/user/manage-emails' #:
    USER_REGISTER_URL = '/user/register' #:
    USER_RESEND_CONFIRM_EMAIL_URL = '/user/resend-confirm-email' #:
    USER_RESET_PASSWORD_URL = '/user/reset-password/<token>' #:
    USER_USER_PROFILE_URL = '/user/profile' #:

    Section_four = "Default template files." #:

    USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html' #:
    USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html' #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'flask_user/forgot_password.html' #:
    USER_INVITE_TEMPLATE = 'flask_user/invite.html' #:
    USER_INVITE_ACCEPT_TEMPLATE = 'flask_user/register.html' #:
    USER_LOGIN_TEMPLATE = 'flask_user/login.html' #:
    USER_MANAGE_EMAILS_TEMPLATE = 'flask_user/manage_emails.html' #:
    USER_REGISTER_TEMPLATE = 'flask_user/register.html' #:
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'flask_user/resend_confirm_email.html' #:
    USER_RESET_PASSWORD_TEMPLATE = 'flask_user/reset_password.html' #:
    USER_USER_PROFILE_TEMPLATE = 'flask_user/user_profile.html' #:

    Section_five = "Default email template files." #:

    USER_CONFIRM_EMAIL_EMAIL_TEMPLATE = 'flask_user/emails/confirm_email' #:
    USER_FORGOT_PASSWORD_EMAIL_TEMPLATE = 'flask_user/emails/forgot_password' #:
    USER_INVITE_EMAIL_TEMPLATE = 'flask_user/emails/invite' #:
    USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/password_changed' #:
    USER_REGISTERED_EMAIL_TEMPLATE = 'flask_user/emails/registered' #:
    USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/username_changed' #:

    Section_six = "Default endpoints." #:

    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_CHANGE_USERNAME_ENDPOINT = '' #:
    USER_AFTER_CONFIRM_ENDPOINT = '' #:
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_LOGIN_ENDPOINT = '' #:
    USER_AFTER_REGISTER_ENDPOINT = '' #:
    USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT = '' #:
    USER_AFTER_RESET_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_INVITE_ENDPOINT = '' #:
    USER_UNCONFIRMED_EMAIL_ENDPOINT = '' #:
    USER_UNAUTHORIZED_ENDPOINT = '' #:
    USER_AFTER_LOGOUT_ENDPOINT = 'user.login' #:
    USER_UNAUTHENTICATED_ENDPOINT = 'user.login' #:

    # ***** Initialization methods *****

    def __init__(self, app=None, db=None, UserClass=None, **kwargs):
        """
        Args:
            app(Flask): The Flask application instance.
            db: An Object-Database Mapper instance such as SQLAlchemy or MongoAlchemy.
            UserClass: The User class (*not* an instance!).

        Keyword Args:
            UserEmailClass: The optional UserEmail class (*not* an instance!).
                Required for the 'multiple emails per user' feature.
            UserInvitationClass: The optional UserInvitation class (*not* an instance!).
                Required for the 'register by invitation' feature.

        Example:
            ``user_manager = UserManager(app, db, User)``
        """

        #see http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code """
        self.app = app
        if app:
            self.init_app(app, db, UserClass, **kwargs)

    def init_app(self, app, db, UserClass,
                 UserInvitationClass=None,
                 UserEmailClass=None,
                add_email_form=forms.AddEmailForm,
                 change_password_form=forms.ChangePasswordForm,
                 change_username_form=forms.ChangeUsernameForm,
                 forgot_password_form=forms.ForgotPasswordForm,
                 login_form=forms.LoginForm,
                 register_form=forms.RegisterForm,
                 resend_confirm_email_form=forms.ResendConfirmEmailForm,
                 reset_password_form=forms.ResetPasswordForm,
                 invite_form=forms.InviteForm,
                 # Validators
                username_validator=forms.username_validator,
                 password_validator=forms.password_validator,
                 # View functions
                render_function=render_template,
                 change_password_view_function=views.change_password,
                 change_username_view_function=views.change_username,
                 confirm_email_view_function=views.confirm_email,
                 email_action_view_function=views.email_action,
                 forgot_password_view_function=views.forgot_password,
                 login_view_function=views.login,
                 logout_view_function=views.logout,
                 manage_emails_view_function=views.manage_emails,
                 register_view_function=views.register,
                 resend_confirm_email_view_function = views.resend_confirm_email,
                 reset_password_view_function = views.reset_password,
                 unconfirmed_email_view_function = views.unconfirmed,
                 unauthenticated_view_function = views.unauthenticated,
                 unauthorized_view_function = views.unauthorized,
                 user_profile_view_function = views.user_profile,
                 invite_view_function = views.invite,
                 # Misc
                 login_manager = None,
                 password_crypt_context = None,
                 make_safe_url_function = views.make_safe_url):

        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

        # Bind Flask-User to app
        app.user_manager = self

        # Save DB and Class params
        self.db = db
        self.UserClass = UserClass
        self.UserEmailClass = UserEmailClass
        self.UserInvitationClass = UserInvitationClass

        # Define default settings
        default_enable_mail = True
        default_user_enable_username = True
        default_auto_login = True
        default_home_endpoint = ''
        default_login_endpoint = 'user.login'
        default_settings = dict(
            #: What happens to this docstring?
            USER_ENABLE_CHANGE_PASSWORD = True,
            USER_ENABLE_EMAIL = default_enable_mail,
            USER_ENABLE_CONFIRM_EMAIL = default_enable_mail,
            USER_ENABLE_FORGOT_PASSWORD = default_enable_mail,
            USER_ENABLE_INVITATION = False,
            USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = False,
            USER_ENABLE_MULTIPLE_EMAILS = False,
            USER_ENABLE_REGISTER = True,
            USER_ENABLE_REMEMBER_ME=True,
            USER_ENABLE_RETYPE_PASSWORD = True,
            USER_ENABLE_USERNAME = default_user_enable_username,
            USER_ENABLE_CHANGE_USERNAME = default_user_enable_username,

            USER_APP_NAME = 'USER_APP_NAME',
            USER_AUTO_LOGIN = default_auto_login,
            USER_AUTO_LOGIN_AFTER_CONFIRM = default_auto_login,
            USER_AUTO_LOGIN_AFTER_REGISTER = default_auto_login,
            USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = default_auto_login,
            USER_AUTO_LOGIN_AT_LOGIN = default_auto_login,
            USER_CONFIRM_EMAIL_EXPIRATION = 2 * 24 * 3600,  # 2 days
            USER_INVITE_EXPIRATION = 90 * 24 * 3600,  # 90 days
            USER_PASSWORD_HASH = 'bcrypt',
            USER_RESET_PASSWORD_EXPIRATION = 2 * 24 * 3600,  # 2 days
            USER_REQUIRE_INVITATION = False,
            USER_SHOW_EMAIL_DOES_NOT_EXIST = True,
            USER_SHOW_USERNAME_DOES_NOT_EXIST = True,
            USER_SEND_PASSWORD_CHANGED_EMAIL = True,
            USER_SEND_REGISTERED_EMAIL = True,
            USER_SEND_USERNAME_CHANGED_EMAIL = True,

            USER_CHANGE_PASSWORD_URL = '/user/change-password',
            USER_CHANGE_USERNAME_URL = '/user/change-username',
            USER_CONFIRM_EMAIL_URL = '/user/confirm-email/<token>',
            USER_EMAIL_ACTION_URL = '/user/email/<id>/<action>',
            USER_FORGOT_PASSWORD_URL = '/user/forgot-password',
            USER_INVITE_URL = '/user/invite',
            USER_LOGIN_URL = '/user/sign-in',
            USER_LOGOUT_URL = '/user/sign-out',
            USER_MANAGE_EMAILS_URL = '/user/manage-emails',
            USER_REGISTER_URL = '/user/register',
            USER_RESEND_CONFIRM_EMAIL_URL = '/user/resend-confirm-email',
            USER_RESET_PASSWORD_URL = '/user/reset-password/<token>',
            USER_USER_PROFILE_URL = '/user/profile',

            USER_AFTER_CHANGE_PASSWORD_ENDPOINT = default_home_endpoint,
            USER_AFTER_CHANGE_USERNAME_ENDPOINT = default_home_endpoint,
            USER_AFTER_CONFIRM_ENDPOINT = default_home_endpoint,
            USER_AFTER_FORGOT_PASSWORD_ENDPOINT = default_home_endpoint,
            USER_AFTER_LOGIN_ENDPOINT = default_home_endpoint,
            USER_AFTER_LOGOUT_ENDPOINT = default_login_endpoint,
            USER_AFTER_REGISTER_ENDPOINT = default_home_endpoint,
            USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT = default_home_endpoint,
            USER_AFTER_RESET_PASSWORD_ENDPOINT = default_home_endpoint,
            USER_AFTER_INVITE_ENDPOINT = default_home_endpoint,
            USER_UNCONFIRMED_EMAIL_ENDPOINT = default_home_endpoint,
            USER_UNAUTHENTICATED_ENDPOINT = default_login_endpoint,
            USER_UNAUTHORIZED_ENDPOINT = default_home_endpoint,

            USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html',
            USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html',
            USER_FORGOT_PASSWORD_TEMPLATE = 'flask_user/forgot_password.html',
            USER_INVITE_TEMPLATE = 'flask_user/invite.html',
            USER_INVITE_ACCEPT_TEMPLATE = 'flask_user/register.html',
            USER_LOGIN_TEMPLATE = 'flask_user/login.html',
            USER_MANAGE_EMAILS_TEMPLATE = 'flask_user/manage_emails.html',
            USER_REGISTER_TEMPLATE = 'flask_user/register.html',
            USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'flask_user/resend_confirm_email.html',
            USER_RESET_PASSWORD_TEMPLATE = 'flask_user/reset_password.html',
            USER_USER_PROFILE_TEMPLATE = 'flask_user/user_profile.html',

            USER_CONFIRM_EMAIL_EMAIL_TEMPLATE = 'flask_user/emails/confirm_email',
            USER_FORGOT_PASSWORD_EMAIL_TEMPLATE = 'flask_user/emails/forgot_password',
            USER_INVITE_EMAIL_TEMPLATE = 'flask_user/emails/invite',
            USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/password_changed',
            USER_REGISTERED_EMAIL_TEMPLATE = 'flask_user/emails/registered',
            USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/username_changed',

            # Deprecated:
            # USER_PASSWORD_HASH_MODE='passlib',
            # USER_PASSWORD_SALT=app.config.get('SECRET_KEY', None),
        )

        # Set UserManager settings from app.config and default_settings
        for name, default_value in default_settings.items():
            setattr(self, name, app.config.get(name, default_value))

        # Configure a DbAdapter based on the class of the 'db' parameter
        self.db_adapter = None
        # Check if db is a SQLAlchemy instance
        if self.db_adapter is None:
            try:
                from flask_sqlalchemy import SQLAlchemy
                if isinstance(db, SQLAlchemy):
                    from .db_adapters import DbAdapterForSQLAlchemy
                    self.db_adapter = DbAdapterForSQLAlchemy(db)
            except:
                pass
        # Check if db is a MongoAlchemy instance
        if self.db_adapter is None:
            try:
                from flask_mongoalchemy import MongoAlchemy
                if isinstance(db, MongoAlchemy):
                    from .db_adapters import DbAdapterForMongoAlchemy
                    self.db_adapter = DbAdapterForMongoAlchemy(db)
            except:
                pass

        # Configure EmailMailerForFlaskMail as the defaule email mailer
        from .email_mailers.email_mailer_for_flask_mail import EmailMailerForFlaskMail
        self.email_mailer = EmailMailerForFlaskMail(app)

        # Initialize Translations -- Only if Flask-Babel has been installed
        if hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.install_gettext_callables(
                    lambda x: get_translations().ugettext(x),
                    lambda s, p, n: get_translations().ungettext(s, p, n),
                    newstyle=True)
        else:
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations()

        # Allow CustomUserManager to customize settings and methods
        self.customize(app)

        # Initialize default settings, when they haven't been set
        self._create_default_settings(app)

        # Make sure the settings are valid -- raise ConfigurationError if not
        self._check_settings()

        # Forms
        self._create_default_attr('add_email_form', add_email_form)
        self._create_default_attr('change_password_form', change_password_form)
        self._create_default_attr('change_username_form', change_username_form)
        self._create_default_attr('forgot_password_form', forgot_password_form)
        self._create_default_attr('login_form', login_form)
        self._create_default_attr('register_form', register_form)
        self._create_default_attr('resend_confirm_email_form', resend_confirm_email_form)
        self._create_default_attr('reset_password_form', reset_password_form)
        self._create_default_attr('invite_form', invite_form)
        # Validators
        self._create_default_attr('username_validator', username_validator)
        self._create_default_attr('password_validator', password_validator)
        # View functions
        self._create_default_attr('render_function', render_function)
        self._create_default_attr('change_password_view_function', change_password_view_function)
        self._create_default_attr('change_username_view_function', change_username_view_function)
        self._create_default_attr('confirm_email_view_function', confirm_email_view_function)
        self._create_default_attr('email_action_view_function', email_action_view_function)
        self._create_default_attr('forgot_password_view_function', forgot_password_view_function)
        self._create_default_attr('login_view_function', login_view_function)
        self._create_default_attr('logout_view_function', logout_view_function)
        self._create_default_attr('manage_emails_view_function', manage_emails_view_function)
        self._create_default_attr('register_view_function', register_view_function)
        self._create_default_attr('resend_confirm_email_view_function', resend_confirm_email_view_function)
        self._create_default_attr('reset_password_view_function', reset_password_view_function)
        self._create_default_attr('unconfirmed_email_view_function', unconfirmed_email_view_function)
        self._create_default_attr('unauthenticated_view_function', unauthenticated_view_function)
        self._create_default_attr('unauthorized_view_function', unauthorized_view_function)
        self._create_default_attr('user_profile_view_function', user_profile_view_function)
        self._create_default_attr('invite_view_function', invite_view_function)
        # Misc
        self._create_default_attr('login_manager', login_manager)
        self._create_default_attr('password_crypt_context', password_crypt_context)
        self._create_default_attr('make_safe_url_function', make_safe_url_function)

        # Setup PasswordManager
        self.password_manager = PasswordManager(self.password_crypt_context, self.USER_PASSWORD_HASH, self.USER_PASSWORD_HASH_MODE, self.USER_PASSWORD_SALT)

        # Setup EmailManager
        self.email_manager = EmailManager(self)

        # Setup TokenManager
        self.token_manager = TokenManager(app.config['SECRET_KEY'])

        # Setup default LoginManager using Flask-Login
        if not self.login_manager:
            self.login_manager = LoginManager(app)
            self.login_manager.login_view = 'user.login'

            # Flask-Login calls this function to retrieve a User record by user ID.
            # Note: user_id is a UNICODE string returned by UserMixin.get_id().
            # See https://flask-login.readthedocs.org/en/latest/#how-it-works
            @self.login_manager.user_loader
            def load_user_by_user_token(user_token):
                user = self.UserClass.get_user_by_token(user_token, 3600)
                return user


        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add URL routes
        self._add_url_routes(app)

        # Add context processor
        app.context_processor(_flask_user_context_processor)

        # Prepare for translations
        _ = translations.gettext


    def customize(self, app):
        """ Override default Flask-User behavior with custom behavior.

        ::

            # Customize Flask-User
            class CustomUserManager(UserManager):

                def customize():
                    # Add custom settings here
                    # Note: This can also be changed in the applicationc config file.
                    self.USER_ENABLE_EMAIL = True
                    self.USER_ENABLE_USERNAME = False

                    # Add custom behavior here
                    self.token_manager = MyJwtTokenManager()
                    self.email_manager = MySendGridEmailManager()

            # Setup Flask-User
            user_manager = MyCustomFlaskUser(app, db, User)
        """

        pass
    
    
    def _create_default_settings(self, app):
        """ Set default app.config settings, but only if they have not been set before """
        # sets self.attribute = self.ATTRIBUTE or app.config.USER_ATTRIBUTE or default_value

        # Create default features
        self._create_default_setting('USER_ENABLE_CHANGE_PASSWORD',     app, True)
        self._create_default_setting('USER_ENABLE_EMAIL',               app, True)
        self._create_default_setting('USER_ENABLE_CONFIRM_EMAIL',       app, self.USER_ENABLE_EMAIL)
        self._create_default_setting('USER_ENABLE_FORGOT_PASSWORD',     app, self.USER_ENABLE_EMAIL)
        self._create_default_setting('USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL', app, False)
        self._create_default_setting('USER_ENABLE_MULTIPLE_EMAILS',     app, False)
        self._create_default_setting('USER_ENABLE_REGISTER',            app, True)
        self._create_default_setting('USER_ENABLE_REMEMBER_ME',         app, True)
        self._create_default_setting('USER_ENABLE_RETYPE_PASSWORD',     app, True)
        self._create_default_setting('USER_ENABLE_USERNAME',            app, True)
        self._create_default_setting('USER_ENABLE_CHANGE_USERNAME',     app, self.USER_ENABLE_USERNAME)

        # Create default settings
        self._create_default_setting('APP_NAME',                   app, 'MyApp')
        self._create_default_setting('auto_login',                 app, True)
        self._create_default_setting('USER_AUTO_LOGIN_AFTER_CONFIRM',   app, self.auto_login)
        self._create_default_setting('USER_AUTO_LOGIN_AFTER_REGISTER',  app, self.auto_login)
        self._create_default_setting('USER_AUTO_LOGIN_AFTER_RESET_PASSWORD', app, self.auto_login)
        self._create_default_setting('USER_AUTO_LOGIN_AT_LOGIN',        app, self.auto_login)
        self._create_default_setting('USER_CONFIRM_EMAIL_EXPIRATION',   app, 2 * 24 * 3600)  # 2 days
        self._create_default_setting('USER_INVITE_EXPIRATION',          app, 90 * 24 * 3600)  # 90 days
        self._create_default_setting('USER_PASSWORD_HASH_MODE',         app, 'passlib')
        self._create_default_setting('USER_PASSWORD_HASH',       app, 'bcrypt')
        self._create_default_setting('USER_PASSWORD_SALT',              app, app.config['SECRET_KEY'])
        self._create_default_setting('USER_PASSWORD_EXPIRATION',  app, 2 * 24 * 3600)  # 2 days
        self._create_default_setting('USER_ENABLE_INVITATION',          app, False)
        self._create_default_setting('USER_REQUIRE_INVITATION',         app, False)
        self._create_default_setting('USER_SEND_PASSWORD_CHANGED_EMAIL',app, self.USER_ENABLE_EMAIL)
        self._create_default_setting('USER_SEND_REGISTERED_EMAIL',      app, self.USER_ENABLE_EMAIL)
        self._create_default_setting('USER_SEND_USERNAME_CHANGED_EMAIL',app, self.USER_ENABLE_EMAIL)
        self._create_default_setting('USER_SHOW_EMAIL_DOES_NOT_EXIST', app, self.USER_ENABLE_REGISTER)
        self._create_default_setting('USER_SHOW_USERNAME_DOES_NOT_EXIST', app, self.USER_ENABLE_REGISTER)

        # Create default URLs
        self._create_default_setting('base_url',                   app, '/user')
        self._create_default_setting('USER_CHANGE_PASSWORD_URL',        app, self.base_url+'/change-password')
        self._create_default_setting('USER_CHANGE_USERNAME_URL',        app, self.base_url+'/change-username')
        self._create_default_setting('USER_CHANGE_CONFIRM_EMAIL_URL',          app, self.base_url+'/confirm-email/<token>')
        self._create_default_setting('USER_EMAIL_ACTION_URL',           app, self.base_url+'/email/<id>/<action>')
        self._create_default_setting('USER_FORGOT_PASSWORD_URL',        app, self.base_url+'/forgot-password')
        self._create_default_setting('USER_LOGIN_URL',                  app, self.base_url+'/sign-in')
        self._create_default_setting('USER_LOGOUT_URL',                 app, self.base_url+'/sign-out')
        self._create_default_setting('USER_MANAGE_EMAILS_URL',          app, self.base_url+'/manage-emails')
        self._create_default_setting('USER_REGISTER_URL',               app, self.base_url+'/register')
        self._create_default_setting('USER_RESEND_USER_CHANGE_CONFIRM_EMAIL_URL',   app, self.base_url+'/resend-confirm-email')
        self._create_default_setting('USER_RESET_PASSWORD_URL',         app, self.base_url+'/reset-password/<token>')
        self._create_default_setting('USER_USER_PROFILE_URL',           app, self.base_url+'/profile')
        self._create_default_setting('USER_INVITE_URL',                 app, self.base_url+'/invite')

        # Create default ENDPOINTs
        self._create_default_setting('home_endpoint',                  app, '')
        self._create_default_setting('login_endpoint',                 app, 'user.login')
        self._create_default_setting('USER_AFTER_CHANGE_PASSWORD_ENDPOINT', app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_CHANGE_USERNAME_ENDPOINT', app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_CONFIRM_ENDPOINT',         app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_FORGOT_PASSWORD_ENDPOINT', app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_LOGIN_ENDPOINT',           app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_LOGOUT_ENDPOINT',          app, self.login_endpoint)
        self._create_default_setting('USER_AFTER_REGISTER_ENDPOINT',        app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT', app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_RESET_PASSWORD_ENDPOINT',  app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_INVITE_ENDPOINT',          app, self.home_endpoint)
        self._create_default_setting('USER_AFTER_UNCONFIRMED_EMAIL_ENDPOINT',     app, self.home_endpoint)
        self._create_default_setting('USER_UNAUTHENTICATED_ENDPOINT',       app, self.login_endpoint)
        self._create_default_setting('USER_UNAUTHORIZED_ENDPOINT',          app, self.home_endpoint)

        # Create default template files
        template_base = 'flask_user'
        self._create_default_setting('USER_CHANGE_PASSWORD_TEMPLATE',       app, template_base+'/change_password.html')
        self._create_default_setting('USER_CHANGE_USERNAME_TEMPLATE',       app, template_base+'/change_username.html')
        self._create_default_setting('USER_FORGOT_PASSWORD_TEMPLATE',       app, template_base+'/forgot_password.html')
        self._create_default_setting('USER_LOGIN_TEMPLATE',                 app, template_base+'/login.html')
        self._create_default_setting('USER_MANAGE_EMAILS_TEMPLATE',         app, template_base+'/manage_emails.html')
        self._create_default_setting('USER_REGISTER_TEMPLATE',              app, template_base+'/register.html')
        self._create_default_setting('USER_RESENT_CONFIRM_EMAIL_TEMPLATE',  app, template_base+'/resend_confirm_email.html')
        self._create_default_setting('USER_RESET_PASSWORD_TEMPLATE',        app, template_base+'/reset_password.html')
        self._create_default_setting('USER_PROFILE_TEMPLATE',          app, template_base+'/user_profile.html')
        self._create_default_setting('USER_INVITE_TEMPLATE',                app, template_base+'/invite.html')
        self._create_default_setting('USER_INVITE_ACCEPT_TEMPLATE',         app, template_base+'/register.html')

        # Create default email template files
        self._create_default_setting('USER_CONFIRM_EMAIL_EMAIL_TEMPLATE',   app, template_base+'/emails/confirm_email')
        self._create_default_setting('USER_FORGOT_PASSWORD_EMAIL_TEMPLATE', app, template_base+'/emails/forgot_password')
        self._create_default_setting('USER_PASSWORD_CHANGED_EMAIL_TEMPLATE',app, template_base+'/emails/password_changed')
        self._create_default_setting('USER_REGISTERED_EMAIL_TEMPLATE',      app, template_base+'/emails/registered')
        self._create_default_setting('USER_USERNAME_CHANGED_EMAIL_TEMPLATE',app, template_base+'/emails/username_changed')
        self._create_default_setting('USER_INVITE_EMAIL_TEMPLATE',          app, template_base+'/emails/invite')


    # ***** Internal methods *****

    def _create_default_setting(self, attribute_name, app, default_value):
        """ self.attribute = self.ATTRIBUTE or app.config.USER_ATTRIBUTE or default_value """

        # If self.ATTRIBUTE is set in CustomUserManager.customize():
        UPPERCASE_NAME = attribute_name.upper()
        if hasattr(self, UPPERCASE_NAME):
            # value = self.ATTRIBUTE
            value = getattr(self, UPPERCASE_NAME)

        else:
            # value = app.config['USER_ATTRIBUTE'] or default_value
            value = app.config.get('USER_'+UPPERCASE_NAME, default_value)

        # self.attribute = value
        setattr(self, attribute_name, value)


    def _create_default_attr(self, attribute_name, default_value):
        if not hasattr(self, attribute_name):
            setattr(self, attribute_name, default_value)


    def _check_settings(self):
        """ Verify config combinations. Produce a helpful error messages for inconsistent combinations."""

        if self.db_adapter is None:
            raise ConfigurationError('You must specify a DbAdapter interface or install Flask-SQLAlchemy or FlaskMongAlchemy.')

        # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True.
        if self.USER_ENABLE_REGISTER and not (self.USER_ENABLE_USERNAME or self.USER_ENABLE_EMAIL):
            raise ConfigurationError('USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True.')
        # USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True
        if self.USER_ENABLE_CONFIRM_EMAIL and not self.USER_ENABLE_EMAIL:
            raise ConfigurationError('USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True.')
        # USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True
        if self.USER_ENABLE_MULTIPLE_EMAILS and not self.USER_ENABLE_EMAIL:
            raise ConfigurationError('USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True.')
        # USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True
        if self.USER_SEND_REGISTERED_EMAIL and not self.USER_ENABLE_EMAIL:
            raise ConfigurationError('USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True.')
        # USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.
        if self.USER_ENABLE_CHANGE_USERNAME and not self.USER_ENABLE_USERNAME:
            raise ConfigurationError('USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.')
        if self.USER_REQUIRE_INVITATION and not self.USER_ENABLE_INVITATION:
            raise ConfigurationError('USER_REQUIRE_INVITATION=True must have USER_ENABLE_INVITATION=True.')
        if self.USER_ENABLE_INVITATION and not self.UserInvitationClass:
            raise ConfigurationError(
                'USER_ENABLE_INVITATION=True must pass UserInvitationClass to SQLAlchemyAdapter().')


    def _add_url_routes(self, app):
        """ Add URL Routes"""
        app.add_url_rule(self.USER_LOGIN_URL,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGOUT_URL, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        if self.USER_ENABLE_CONFIRM_EMAIL:
            app.add_url_rule(self.USER_CHANGE_CONFIRM_EMAIL_URL, 'user.confirm_email', self.confirm_email_view_function)
            app.add_url_rule(self.USER_RESEND_USER_CHANGE_CONFIRM_EMAIL_URL, 'user.resend_confirm_email', self.resend_confirm_email_view_function, methods=['GET', 'POST'])
        if self.USER_ENABLE_CHANGE_PASSWORD:
            app.add_url_rule(self.USER_CHANGE_PASSWORD_URL, 'user.change_password', self.change_password_view_function, methods=['GET', 'POST'])
        if self.USER_ENABLE_CHANGE_USERNAME:
            app.add_url_rule(self.USER_CHANGE_USERNAME_URL, 'user.change_username', self.change_username_view_function, methods=['GET', 'POST'])
        if self.USER_ENABLE_FORGOT_PASSWORD:
            app.add_url_rule(self.USER_FORGOT_PASSWORD_URL, 'user.forgot_password', self.forgot_password_view_function, methods=['GET', 'POST'])
            app.add_url_rule(self.USER_RESET_PASSWORD_URL, 'user.reset_password', self.reset_password_view_function, methods=['GET', 'POST'])
        if self.USER_ENABLE_REGISTER:
            app.add_url_rule(self.USER_REGISTER_URL, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        if self.UserEmailClass:
            app.add_url_rule(self.USER_EMAIL_ACTION_URL,  'user.email_action',  self.email_action_view_function)
            app.add_url_rule(self.USER_MANAGE_EMAILS_URL, 'user.manage_emails', self.manage_emails_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.USER_USER_PROFILE_URL,  'user.profile',  self.user_profile_view_function,  methods=['GET', 'POST'])
        if self.USER_ENABLE_INVITATION:
            app.add_url_rule(self.USER_INVITE_URL, 'user.invite', self.invite_view_function, methods=['GET', 'POST'])

    def get_user_by_id(self, user_id):
        """Retrieve a User by ID."""
        return self.db_adapter.get_object(self.UserClass, user_id)

    def get_user_email_by_id(self, user_email_id):
        """Retrieve a UserEmail by ID."""
        return self.db_adapter.get_object(self.UserEmailClass, user_email_id)

    def find_user_by_username(self, username):
        """Retrieve a User by username."""
        return self.db_adapter.ifind_first_object(self.UserClass, username=username)

    def find_user_by_email(self, email):
        """Retrieve a User by email."""
        if self.UserEmailClass:
            user_email = self.db_adapter.ifind_first_object(self.UserEmailClass, email=email)
            user = user_email.user if user_email else None
        else:
            user_email = None
            user = self.db_adapter.ifind_first_object(self.UserClass, email=email)

        return (user, user_email)

    def email_is_available(self, new_email):
        """Check if ``new_email`` is available.

        | Returns True if ``new_email`` does not exist or belongs to the current user.
        | Return False otherwise.
        """

        user, user_email = self.find_user_by_email(new_email)
        return (user==None)

    def username_is_available(self, new_username):
        """Check if ``new_username`` is available.

        | Returns True if ``new_username`` does not exist or belongs to the current user.
        | Return False otherwise.
        """

        # Allow user to change username to the current username
        if _call_or_get(current_user.is_authenticated):
            current_username = current_user.username
            if new_username == current_username:
                return True
        # See if new_username is available
        return self.find_user_by_username(new_username)==None

    def get_primary_user_email(self, user):
        """Retrieve the primary User email for the 'multiple emails per user' feature."""
        db_adapter = self.db_adapter
        if self.UserEmailClass:
            user_email = db_adapter.find_first_object(self.UserEmailClass,
                                                      user_id=user.id,
                                                      is_primary=True)
            return user_email
        else:
            return user

