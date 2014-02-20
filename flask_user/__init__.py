# -*- coding: utf-8 -*-
"""
    Flask-Account is a Flask extension
    that provides customizable user flask_user management functionality.

    :copyright: (c) 2013 SolidBuilds.com and Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Apache 2.0, see LICENSE for more details.
"""

from flask import Blueprint, current_app
from flask.ext.babel import gettext as _
from flask.ext.login import LoginManager, current_user
from passlib.context import CryptContext

from werkzeug.datastructures import ImmutableList

__version__ = '0.0.1'

class UserManager():
    """
    This is the Flask-User object that manages the User process.
    """
    def __init__(self, db_adapter, app=None):
        """
        Initialize the UserManager with default customizable settings
        """
        import views
        import forms

        self.db_adapter = db_adapter

        # Customizable view functions
        self.register_view_function = views.register
        self.login_view_function  = views.login
        self.logout_view_function = views.logout
        self.change_password_view_function = views.change_password
        self.change_username_view_function = views.change_username

        # Customizable forms
        self.register_form = forms.RegisterForm
        self.login_form = forms.LoginForm
        self.change_password_form = forms.ChangePasswordForm
        self.change_username_form = forms.ChangeUsernameForm

        # Customizable validators
        self.password_validator = forms.password_validator
        self.username_validator = forms.username_validator

        # Customizable endpoints
        self.logout_next = None

        # Customizable passlib crypt context
        self.crypt_context = CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')
                # See https://pythonhosted.org/passlib/new_app_quickstart.html#choosing-a-hash

        if (app):
            self.init_app(app)

    def init_app(self, app):
        """
        Binds the UserManager to the specified app.
        """

        # Set default features
        self.feature_register        = app.config.setdefault('USER_FEATURE_REGISTER',        True)
        self.feature_invite          = app.config.setdefault('USER_FEATURE_INVITE',          True)
        self.feature_change_password = app.config.setdefault('USER_FEATURE_CHANGE_PASSWORD', True)
        self.feature_change_username = app.config.setdefault('USER_FEATURE_CHANGE_USERNAME', True)
        self.feature_forget_password = app.config.setdefault('USER_FEATURE_FORGOT_PASSWORD', True)
        self.feature_confirm_email   = app.config.setdefault('USER_FEATURE_CONFIRM_EMAIL',   True)

        # Set default settings
        self.register_with_retype_password = app.config.setdefault('USER_REGISTER_WITH_RETYPE_PASSWORD', True)
        self.login_with_username           = app.config.setdefault('USER_LOGIN_WITH_USERNAME',        False)
        self.change_password_with_retype_password = app.config.setdefault('USER_CHANGE_PASSWORD_WITH_RETYPE_PASSWORD', True)

        # Set default URLs
        self.register_url        = app.config.setdefault('USER_REGISTER_URL',        '/user/register')
        self.login_url           = app.config.setdefault('USER_LOGIN_URL',           '/user/sign-in')
        self.logout_url          = app.config.setdefault('USER_LOGOUT_URL',          '/user/sign-out')
        self.change_password_url = app.config.setdefault('USER_CHANGE_PASSWORD_URL', '/user/change-password')
        self.change_username_url = app.config.setdefault('USER_CHANGE_USERNAME_URL', '/user/change-username')

        # Set default template files
        self.register_template        = app.config.setdefault('USER_REGISTER_TEMPLATE',         'flask_user/register.html')
        self.login_template           = app.config.setdefault('USER_LOGIN_TEMPLATE',            'flask_user/login.html')
        self.change_password_template = app.config.setdefault('USER_CHANGE_PASSWORD_TEMPLATE',  'flask_user/change_password.html')
        self.change_username_template = app.config.setdefault('USER_CHANGE_USERNAME_TEMPLATE',  'flask_user/change_username.html')

        # Set default flash messages
        self.flash_signed_in        = app.config.setdefault('USER_FLASH_SIGNED_IN',  'You have signed in successfully.')
        self.flash_signed_out       = app.config.setdefault('USER_FLASH_SIGNED_OUT', 'You have signed out successfully.')
        self.flash_username_changed = app.config.setdefault('USER_FLASH_USERNAME_CHANGED', 'Your Username has been changed successfully.')
        self.flash_password_changed = app.config.setdefault('USER_FLASH_PASSWORD_CHANGED', 'Your Password has been changed successfully.')

        # Setup Flask-Login
        self.lm = LoginManager()
        #self.lm.anonymous_user = AnonymousUser
        self.lm.login_view = 'user.login'
        self.lm.user_loader(_user_loader)
        self.lm.login_message = _('Please Sign in to access this page.')
        self.lm.login_message_category = 'error'
        #login_manager.token_loader(_token_loader)

        #if cv('FLASH_MESSAGES', app=app):
        #    lm.login_message, lm.login_message_category = cv('MSG_LOGIN', app=app)
        #    lm.needs_refresh_message, lm.needs_refresh_message_category = cv('MSG_REFRESH', app=app)
        #else:
        #    lm.login_message = None
        #    lm.needs_refresh_message = None

        self.lm.init_app(app)

        # Add URL Routes
        app.add_url_rule(self.register_url, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.login_url,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.logout_url, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.change_password_url, 'user.change_password', self.change_password_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.change_username_url, 'user.change_username', self.change_username_view_function, methods=['GET', 'POST'])

        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add context processor
        app.context_processor(_account_context_processor)

        app.user_manager = self


class DBInterface(object):
    """
    This object is used to shield Flask-User from ORM specific dependencies.
    It's used as the base class for ORM specific adapters like SQLAlchemyAdapter.
    """
    def __init__(self, db, UserClass, EmailClass=None):
        self.db = db
        self.UserClass = UserClass
        if not EmailClass:
            EmailClass = UserClass
        self.EmailClass = EmailClass

    def find_user_by_email(self, email): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_email() not implemented')

    def find_user_by_username(self, username): # pragma: no cover
        raise NotImplementedError('DBInterface.find_user_by_username() not implemented')


class SQLAlchemyAdapter(DBInterface):
    """
    This object is used to shield Flask-User from SQLAlchemy specific dependencies.
    """
    def __init__(self, db, UserClass, EmailClass=None):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass, EmailClass)

    def add_user(self, **kwargs):
        self.db.session.add(self.UserClass(**kwargs))
        self.db.session.commit()

    def set_username(self, user, username):
        user.username = username
        self.db.session.commit()

    def set_password(self, user, hashed_password):
        user.password = hashed_password
        self.db.session.commit()

    def find_user_by_id(self, id):
        return self.EmailClass.query.filter(self.EmailClass.id==id).first()

    def find_user_by_email(self, email):
        return self.EmailClass.query.filter(self.EmailClass.email==email).first()

    def find_user_by_username(self, username):
        return self.UserClass.query.filter(self.UserClass.username==username).first()

    def email_is_available(self, new_email):
        """
        Return True if new_email does not exist.
        Return False otherwise. 
        """
        # See if new_email is available
        return self.EmailClass.query.filter(self.EmailClass.email==new_email).count()==0

    def username_is_available(self, new_username, old_username=''):
        """
        Return True if new_username does not exist or if new_username equals old_username.
        Return False otherwise. 
        """
        # To avoid user confusion, we allow the old email if the user is currently logged in
        if current_user.is_authenticated():
            old_username = current_user.username
        else:
            old_username = ''
        # See if new_username is available
        return self.UserClass.query.filter(self.UserClass.username==new_username).count()==0 or new_username==old_username

def _account_context_processor():
    return dict(
        user_manager=current_app.user_manager
            )

def _user_loader(user_id):
    um = current_app.user_manager
    return um.db_adapter.find_user_by_id(id=user_id)
