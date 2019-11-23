"""This module implements the main UserManager class for Flask-User.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio'

import datetime

from flask import abort, Blueprint, current_app, Flask, session
from flask_login import LoginManager
from wtforms import ValidationError

from . import ConfigError
from . import forms
from .db_manager import DBManager
from .email_manager import EmailManager
from .password_manager import PasswordManager
from .token_manager import TokenManager
from .translation_utils import lazy_gettext as _  # map _() to lazy_gettext()
from .user_manager__settings import UserManager__Settings
from .user_manager__utils import UserManager__Utils
from .user_manager__views import UserManager__Views


# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class for ease of customization.
class UserManager(UserManager__Settings, UserManager__Utils, UserManager__Views):
    """ Customizable User Authentication and Management.
    """

    def __init__(self, app, db, UserClass, **kwargs):
        """
        Args:
            app(Flask): The Flask application instance.
            db: An Object-Database Mapper instance such as SQLAlchemy or MongoEngine.
            UserClass: The User class (*not* an instance!).

        Keyword Args:
            UserEmailClass: The optional UserEmail class (*not* an instance!).
                Required for the 'multiple emails per user' feature.
            UserInvitationClass: The optional UserInvitation class (*not* an instance!).
                Required for the 'register by invitation' feature.

        Example:
            ``user_manager = UserManager(app, db, User, UserEmailClass=UserEmail)``

        .. This hack shows a header above the _next_ section
        .. code-block:: none

            Customizable UserManager methods
        """

        #see http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code """
        self.app = app
        if app:
            self.init_app(app, db, UserClass, **kwargs)

    def init_app(
        self, app, db, UserClass,
        UserInvitationClass=None,
        UserEmailClass=None,
        RoleClass=None,    # Only used for testing
        ):

        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

        # Bind Flask-User to app
        app.user_manager = self

        # Remember all data-models
        # ------------------------
        self.db = db
        # self.db_manager.UserClass = UserClass
        # self.db_manager.UserEmailClass = UserEmailClass
        # self.UserInvitationClass = UserInvitationClass
        # self.RoleClass=RoleClass

        # Load app config settings
        # ------------------------
        # For each 'UserManager.USER_...' property: load settings from the app config.
        for attrib_name in dir(self):
            if attrib_name[0:5] == 'USER_':
                default_value = getattr(UserManager, attrib_name)
                setattr(self, attrib_name, app.config.get(attrib_name, default_value))

        # If USER_EMAIL_SENDER_EMAIL is not set, try to construct it from
        # MAIL_DEFAULT_SENDER or DEFAULT_MAIL_SENDER
        if not self.USER_EMAIL_SENDER_EMAIL:
            default_sender = app.config.get('DEFAULT_MAIL_SENDER', None)
            default_sender = app.config.get('MAIL_DEFAULT_SENDER', default_sender)
            if default_sender:
                # Accept two formats: '{name}<{email}>' or plain '{email}'
                if default_sender[-1:] == '>':
                    start = default_sender.rfind('<')
                    if start >= 1:
                        self.USER_EMAIL_SENDER_EMAIL = default_sender[start + 1:-1]
                        if not self.USER_EMAIL_SENDER_NAME:
                            self.USER_EMAIL_SENDER_NAME = default_sender[0:start].strip(' "')
                else:
                    self.USER_EMAIL_SENDER_EMAIL = default_sender

        # If USER_EMAIL_SENDER_NAME is not set, default it to USER_APP_NAME
        if not self.USER_EMAIL_SENDER_NAME:
            self.USER_EMAIL_SENDER_NAME = self.USER_APP_NAME

        # Configure Flask session behavior
        # --------------------------------
        if self.USER_USER_SESSION_EXPIRATION:
            app.permanent_session_lifetime = datetime.timedelta(seconds=self.USER_USER_SESSION_EXPIRATION)

            @app.before_request
            def advance_session_timeout():
                session.permanent = True    # Timeout after app.permanent_session_lifetime period
                session.modified = True     # Advance session timeout each time a user visits a page

        # Configure Flask-Login
        # --------------------
        # Setup default LoginManager using Flask-Login
        self.login_manager = LoginManager(app)
        self.login_manager.login_view = 'user.login'

        # Flask-Login calls this function to retrieve a User record by token.
        @self.login_manager.user_loader
        def load_user_by_user_token(user_token):
            user = self.db_manager.UserClass.get_user_by_token(user_token)
            return user

        # Configure Flask-BabelEx
        # -----------------------
        self.babel = app.extensions.get('babel', None)
        from .translation_utils import init_translations
        init_translations(self.babel)

        # Configure Jinja2
        # ----------------
        # If the application has not initialized BabelEx,
        # we must provide a NULL translation to Jinja2
        if not hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations()

        # Define a context processor to provide custom variable and functions available to Jinja2 templates
        def flask_user_context_processor():
            # In Flask-Login 0.2 ``is_authenticated`` and ``is_active`` were implemented as functions,
            # while in 0.3+ they are implemented as properties.
            def call_or_get(function_or_property):
                return function_or_property() if callable(function_or_property) else function_or_property

            return dict(
                user_manager=current_app.user_manager,
                call_or_get=call_or_get,
            )

        # Register context processor with Jinja2
        app.context_processor(flask_user_context_processor)

        # Create a dummy Blueprint to add the app/templates/flask_user dir to the template search path
        blueprint = Blueprint('flask_user', __name__, template_folder='templates')
        app.register_blueprint(blueprint)

        # Set default form classes
        # ------------------------
        self.AddEmailFormClass = forms.AddEmailForm
        self.ChangePasswordFormClass = forms.ChangePasswordForm
        self.ChangeUsernameFormClass = forms.ChangeUsernameForm
        self.EditUserProfileFormClass = forms.EditUserProfileForm
        self.ForgotPasswordFormClass = forms.ForgotPasswordForm
        self.InviteUserFormClass = forms.InviteUserForm
        self.LoginFormClass = forms.LoginForm
        self.RegisterFormClass = forms.RegisterForm
        self.ResendEmailConfirmationFormClass = forms.ResendEmailConfirmationForm
        self.ResetPasswordFormClass = forms.ResetPasswordForm

        # Set default managers
        # --------------------
        # Setup DBManager
        self.db_manager = DBManager(app, db, UserClass, UserEmailClass, UserInvitationClass, RoleClass)

        # Setup PasswordManager
        self.password_manager = PasswordManager(app)

        # Set default EmailAdapter
        if self.USER_ENABLE_EMAIL:
            from .email_adapters.smtp_email_adapter import SMTPEmailAdapter
            self.email_adapter = SMTPEmailAdapter(app)

        # Setup EmailManager
        if self.USER_ENABLE_EMAIL:
            self.email_manager = EmailManager(app)

        # Setup TokenManager
        self.token_manager = TokenManager(app)

        # Allow developers to customize UserManager
        self.customize(app)

        # Make sure the settings are valid -- raise ConfigError if not
        self._check_settings(app)

        # Configure a list of URLs to route to their corresponding view method.
        self._add_url_routes(app)


    def customize(self, app):
        """ Override this method to customize properties.

        Example::

            # Customize Flask-User
            class CustomUserManager(UserManager):

                def customize(self, app):

                    # Add custom managers and email mailers here
                    self.email_manager = CustomEmailManager(app)
                    self.password_manager = CustomPasswordManager(app)
                    self.token_manager = CustomTokenManager(app)
                    self.email_adapter = CustomEmailAdapter(app)

            # Setup Flask-User
            user_manager = CustomUserManager(app, db, User)
        """

    def password_validator(self, form, field):
        """Ensure that passwords have at least 6 characters with one lowercase letter, one uppercase letter and one number.

        Override this method to customize the password validator.
        """

        # Convert string to list of characters
        password = list(field.data)
        password_length = len(password)

        # Count lowercase, uppercase and numbers
        lowers = uppers = digits = 0
        for ch in password:
            if ch.islower(): lowers += 1
            if ch.isupper(): uppers += 1
            if ch.isdigit(): digits += 1

        # Password must have one lowercase letter, one uppercase letter and one digit
        is_valid = password_length >= 6 and lowers and uppers and digits
        if not is_valid:
            raise ValidationError(
                _('Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))

    # If you prefer using Regex:
    # from re import compile
    # PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z')
    # def password_is_valid(password):
    #     return PASSWORD_REGEX.match(password) is not None

    def username_validator(self, form, field):
        """Ensure that Usernames contains at least 3 alphanumeric characters.

        Override this method to customize the username validator.
        """
        username = field.data
        if len(username) < 3:
            raise ValidationError(
                _('Username must be at least 3 characters long'))
        valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._'
        chars = list(username)
        for char in chars:
            if char not in valid_chars:
                raise ValidationError(
                    _("Username may only contain letters, numbers, '-', '.' and '_'"))

    # If you prefer using Regex:
    # from re import compile
    # USERNAME_REGEX = compile(r'\A[\w\-\.]{3,}\Z')
    # def username_is_valid(username):
    #     return USERNAME_REGEX.match(username) is not None

    # ***** Private methods *****

    def _check_settings(self, app):
        """Verify required settings. Produce a helpful error messages for incorrect settings."""

        # Check for invalid settings
        # --------------------------

        # Check UserInvitationClass and USER_ENABLE_INVITE_USER
        if self.USER_ENABLE_INVITE_USER and not self.db_manager.UserInvitationClass:
            raise ConfigError(
                'UserInvitationClass is missing while USER_ENABLE_INVITE_USER is True.' \
                ' Specify UserInvitationClass with UserManager(app, db, User, UserInvitationClass=...' \
                ' or set USER_ENABLE_INVITE_USER=False.')

        # Check for deprecated settings
        # -----------------------------

        # Check for deprecated USER_ENABLE_CONFIRM_EMAIL
        setting = app.config.get('USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL', None)
        if setting is not None:
            print(
                'Deprecation warning: USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL'\
                ' will be deprecated.' \
                ' It has been replaced by USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL.'\
                ' Please change this as soon as possible.')
            self.USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = setting

        # Check for deprecated USER_ENABLE_RETYPE_PASSWORD
        setting = app.config.get('USER_ENABLE_RETYPE_PASSWORD', None)
        if setting is not None:
            print(
                'Deprecation warning: USER_ENABLE_RETYPE_PASSWORD'\
                ' will be deprecated.' \
                ' It has been replaced with USER_REQUIRE_RETYPE_PASSWORD.'\
                ' Please change this as soon as possible.')
            self.USER_REQUIRE_RETYPE_PASSWORD = setting

        # Check for deprecated USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST
        setting = app.config.get('USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST', None)
        if setting is not None:
            print(
                'Deprecation warning: USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST' \
                ' will be deprecated.' \
                ' It has been replaced with USER_SHOW_USERNAME_DOES_NOT_EXIST'
                ' and USER_SHOW_EMAIL_DOES_NOT_EXIST.'
                ' Please change this as soon as possible.')
            self.USER_SHOW_USERNAME_DOES_NOT_EXIST = setting
            self.USER_SHOW_EMAIL_DOES_NOT_EXIST = setting

        # Check for deprecated USER_PASSWORD_HASH
        setting = app.config.get('USER_PASSWORD_HASH', None)
        if setting is not None:
            print(
                "Deprecation warning: USER_PASSWORD_HASH=<string>"\
                " will be deprecated."\
                " It has been replaced with USER_PASSLIB_CRYPTCONTEXT_SCHEMES=<list>."
                " Please change USER_PASSWORD_HASH='something' to"\
                " USER_PASSLIB_CRYPTCONTEXT_SCHEMES=['something'] as soon as possible.")
            self.USER_PASSLIB_CRYPTCONTEXT_SCHEMES = [setting]

        # Check that USER_EMAIL_SENDER_EMAIL is set when USER_ENABLE_EMAIL is True
        if not self.USER_EMAIL_SENDER_EMAIL and self.USER_ENABLE_EMAIL:
            raise ConfigError(
                'USER_EMAIL_SENDER_EMAIL is missing while USER_ENABLE_EMAIL is True.'\
                ' specify USER_EMAIL_SENDER_EMAIL (and USER_EMAIL_SENDER_NAME) or set USER_ENABLE_EMAIL to False.')

        # Disable settings that rely on a feature setting that's not enabled
        # ------------------------------------------------------------------

        # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True.
        if not self.USER_ENABLE_USERNAME and not self.USER_ENABLE_EMAIL:
            self.USER_ENABLE_REGISTER = False

        # Settings that depend on USER_ENABLE_EMAIL
        if not self.USER_ENABLE_EMAIL:
            self.USER_ENABLE_CONFIRM_EMAIL = False
            self.USER_ENABLE_MULTIPLE_EMAILS = False
            self.USER_ENABLE_FORGOT_PASSWORD = False
            self.USER_SEND_PASSWORD_CHANGED_EMAIL = False
            self.USER_SEND_REGISTERED_EMAIL = False
            self.USER_SEND_USERNAME_CHANGED_EMAIL = False
            self.USER_REQUIRE_INVITATION = False

        # Settings that depend on USER_ENABLE_USERNAME
        if not self.USER_ENABLE_USERNAME:
            self.USER_ENABLE_CHANGE_USERNAME = False

    def _add_url_routes(self, app):
        """Configure a list of URLs to route to their corresponding view method.."""

        # Because methods contain an extra ``self`` parameter, URL routes are mapped
        # to stub functions, which simply call the corresponding method.

        # For testing purposes, we map all available URLs to stubs, but the stubs
        # contain config checks to return 404 when a feature is disabled.

        # Define the stubs
        # ----------------

        # def auth0_callback_stub():
        #     if not self.USER_ENABLE_AUTH0: abort(404)
        #     return self.auth0_callback_view()

        def change_password_stub():
            if not self.USER_ENABLE_CHANGE_PASSWORD: abort(404)
            return self.change_password_view()

        def change_username_stub():
            if not self.USER_ENABLE_CHANGE_USERNAME: abort(404)
            return self.change_username_view()

        def confirm_email_stub(token):
            if not self.USER_ENABLE_CONFIRM_EMAIL: abort(404)
            return self.confirm_email_view(token)

        def edit_user_profile_stub():
            return self.edit_user_profile_view()

        def email_action_stub(id, action):
            if not self.USER_ENABLE_MULTIPLE_EMAILS or not self.db_manager.UserEmailClass: abort(404)
            return self.email_action_view(id, action)

        def forgot_password_stub():
            if not self.USER_ENABLE_FORGOT_PASSWORD: abort(404)
            return self.forgot_password_view()

        def manage_emails_stub():
            if not self.USER_ENABLE_MULTIPLE_EMAILS or not self.db_manager.UserEmailClass: abort(404)
            return self.manage_emails_view()

        def invite_user_stub():
            if not self.USER_ENABLE_INVITE_USER: abort(404)
            return self.invite_user_view()

        def login_stub():
            return self.login_view()

        def logout_stub():
            return self.logout_view()

        def register_stub():
            if not self.USER_ENABLE_REGISTER: abort(404)
            return self.register_view()

        def resend_email_confirmation_stub():
            if not self.USER_ENABLE_CONFIRM_EMAIL: abort(404)
            return self.resend_email_confirmation_view()

        def reset_password_stub(token):
            if not self.USER_ENABLE_FORGOT_PASSWORD: abort(404)
            return self.reset_password_view(token)

        # def unconfirmed_email_stub():
        #     return self.unconfirmed_email_view()

        def unauthorized_stub():
            return self.unauthorized_view()


        # Add the URL routes
        # ------------------

        # app.add_url_rule('/callbacks/auth0', 'user.auth0_callback', auth0_callback_stub)
        app.add_url_rule(self.USER_CHANGE_PASSWORD_URL, 'user.change_password', change_password_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_CHANGE_USERNAME_URL, 'user.change_username', change_username_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_CONFIRM_EMAIL_URL, 'user.confirm_email', confirm_email_stub)
        app.add_url_rule(self.USER_EDIT_USER_PROFILE_URL, 'user.edit_user_profile', edit_user_profile_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_EMAIL_ACTION_URL, 'user.email_action', email_action_stub)
        app.add_url_rule(self.USER_FORGOT_PASSWORD_URL, 'user.forgot_password', forgot_password_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_INVITE_USER_URL, 'user.invite_user', invite_user_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGIN_URL, 'user.login', login_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_LOGOUT_URL, 'user.logout', logout_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_MANAGE_EMAILS_URL, 'user.manage_emails', manage_emails_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_REGISTER_URL, 'user.register', register_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_RESEND_EMAIL_CONFIRMATION_URL, 'user.resend_email_confirmation',
                         resend_email_confirmation_stub,
                         methods=['GET', 'POST'])
        app.add_url_rule(self.USER_RESET_PASSWORD_URL, 'user.reset_password', reset_password_stub,
                         methods=['GET', 'POST'])



