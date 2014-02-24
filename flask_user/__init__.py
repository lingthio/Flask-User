"""
    flask_user
    ----------
    Flask-User is a customizable user management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from flask import Blueprint, current_app
from flask_babel import gettext as _
from flask_login import LoginManager, UserMixin as LoginUserMixin
from flask_user.db_interfaces import DBInterface

from .db_interfaces import SQLAlchemyAdapter
from .passwords import init_password_crypt_context
from .tokens import TokenManager

__version__ = '0.2.0'

class UserMixin(LoginUserMixin):
    pass

class UserManager():
    """
    This is the Flask-User object that manages the User process.
    """
    def __init__(self, db_adapter, app=None):
        """
        Initialize the UserManager with default customizable settings
        """
        from . import views
        from . import forms

        self.db_adapter = db_adapter

        # Customizable view functions
        self.change_password_view_function = views.change_password
        self.change_username_view_function = views.change_username
        self.confirm_email_view_function   = views.confirm_email
        self.forgot_password_view_function = views.forgot_password
        self.login_view_function           = views.login
        self.logout_view_function          = views.logout
        self.register_view_function        = views.register
        self.resend_confirmation_email_view_function = views.resend_confirmation_email
        self.reset_password_view_function   = views.reset_password

        # Customizable forms
        self.change_password_form = forms.ChangePasswordForm
        self.change_username_form = forms.ChangeUsernameForm
        self.forgot_password_form = forms.ForgotPasswordForm
        self.login_form           = forms.LoginForm
        self.register_form        = forms.RegisterForm
        self.reset_password_form  = forms.ResetPasswordForm

        # Customizable validators
        self.password_validator = forms.password_validator
        self.username_validator = forms.username_validator

        # Customizable endpoints
        self.logout_next = None

        # Customizable passlib crypt context
        self.password_crypt_context = init_password_crypt_context()

        if (app):
            self.init_app(app)

    def init_app(self, app):
        """
        Binds the UserManager to the specified app.
        """
        app.user_manager = self

        # Set default features
        self.enable_registration        = app.config.setdefault('USER_ENABLE_REGISTRATION',         True)
        self.enable_forgot_password     = app.config.setdefault('USER_ENABLE_FORGOT_PASSWORD',      False)
        self.enable_change_password     = app.config.setdefault('USER_ENABLE_CHANGE_PASSWORD',      True)
        self.enable_change_username     = app.config.setdefault('USER_ENABLE_CHANGE_USERNAME',      False)
        self.enable_confirm_email       = app.config.setdefault('USER_ENABLE_CONFIRM_EMAIL',        False)
        self.enable_require_invitation  = app.config.setdefault('USER_ENABLE_REQUIRE_INVITATION',   False)

        # Set default settings
        self.confirm_email_expiration   = app.config.setdefault('USER_CONFIRM_EMAIL_EXPIRATION',    2*24*3600) # 2 days
        self.login_with_username        = app.config.setdefault('USER_LOGIN_WITH_USERNAME',         False)
        self.register_with_email        = app.config.setdefault('USER_REGISTER_WITH_EMAIL',         True)
        self.reset_password_expiration  = app.config.setdefault('USER_RESET_PASSWORD_EXPIRATION',   2*24*3600) # 2 days
        self.retype_password            = app.config.setdefault('USER_RETYPE_PASSWORD',             True)

        # Set default URLs
        self.change_password_url = app.config.setdefault('USER_CHANGE_PASSWORD_URL', '/user/change-password')
        self.change_username_url = app.config.setdefault('USER_CHANGE_USERNAME_URL', '/user/change-username')
        self.confirm_email_url   = app.config.setdefault('USER_CONFIRM_EMAIL_URL',   '/user/confirm-email/<token>')
        self.forgot_password_url = app.config.setdefault('USER_FORGOT_PASSWORD_URL', '/user/forgot-password')
        self.login_url           = app.config.setdefault('USER_LOGIN_URL',           '/user/sign-in')
        self.logout_url          = app.config.setdefault('USER_LOGOUT_URL',          '/user/sign-out')
        self.register_url        = app.config.setdefault('USER_REGISTER_URL',        '/user/register')
        self.resend_confirmation_email_url = app.config.setdefault('USER_RESEND_CONFIRMATION_EMAIL_URL', '/user/resend-confirmation-email')
        self.reset_password_url   = app.config.setdefault('USER_RESET_PASSWORD_URL',  '/user/reset-password/<token>')

        # Set default template files
        self.change_password_template = app.config.setdefault('USER_CHANGE_PASSWORD_TEMPLATE',  'flask_user/change_password.html')
        self.change_username_template = app.config.setdefault('USER_CHANGE_USERNAME_TEMPLATE',  'flask_user/change_username.html')
        self.forgot_password_template = app.config.setdefault('USER_FORGOT_PASSWORD_TEMPLATE',  'flask_user/forgot_password.html')
        self.login_template           = app.config.setdefault('USER_LOGIN_TEMPLATE',            'flask_user/login.html')
        self.register_template        = app.config.setdefault('USER_REGISTER_TEMPLATE',         'flask_user/register.html')
        self.resend_confirmation_email_template = app.config.setdefault('USER_RESEND_CONFIRMATION_EMAIL_TEMPLATE', 'flask_user/resend_confirmation_email.html')
        self.reset_password_template = app.config.setdefault('USER_RESET_PASSWORD_TEMPLATE', 'flask_user/reset_password.html')

        # Setup Flask-Login
        self.lm = LoginManager()
        self.lm.login_message = _('Please Sign in to access this page.')
        self.lm.login_message_category = 'error'
        self.lm.login_view = 'user.login'
        self.lm.user_loader(_user_loader)
        #login_manager.token_loader(_token_loader)
        self.lm.init_app(app)

        # Initialize TokenManager
        self.token_manager = TokenManager(app.config.get('SECRET_KEY'))

        # Add URL Routes
        if self.enable_confirm_email:
            app.add_url_rule(self.confirm_email_url, 'user.confirm_email', self.confirm_email_view_function)
            app.add_url_rule(self.resend_confirmation_email_url, 'user.resend_confirmation_email', self.resend_confirmation_email_view_function)
        if self.enable_change_password:
            app.add_url_rule(self.change_password_url, 'user.change_password', self.change_password_view_function, methods=['GET', 'POST'])
        if self.enable_change_username:
            app.add_url_rule(self.change_username_url, 'user.change_username', self.change_username_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.login_url,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.logout_url, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        if self.enable_registration:
            app.add_url_rule(self.register_url, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        if self.enable_forgot_password:
            app.add_url_rule(self.forgot_password_url, 'user.forgot_password', self.forgot_password_view_function, methods=['GET', 'POST'])
            app.add_url_rule(self.reset_password_url, 'user.reset_password', self.reset_password_view_function, methods=['GET', 'POST'])

        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add context processor
        app.context_processor(_flask_user_context_processor)


def _flask_user_context_processor():
    """
    Make 'user_manager' available to Jinja2 templates
    """
    return dict(user_manager=current_app.user_manager)


def _user_loader(user_id):
    """
    Flask-Login helper function to load user by user_id
    """
    user_manager = current_app.user_manager
    return user_manager.db_adapter.find_user_by_id(user_id=user_id)
