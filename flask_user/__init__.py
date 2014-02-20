# -*- coding: utf-8 -*-
"""
    Flask-Account is a Flask extension
    that provides customizable user flask_user management functionality.

    :copyright: (c) 2013 SolidBuilds.com and Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Apache 2.0, see LICENSE for more details.
"""

from flask import Blueprint, current_app
from flask_login import AnonymousUserMixin, LoginManager, current_user
from passlib.context import CryptContext
#from flask.ext.principal import Identity, Principal

from werkzeug.datastructures import ImmutableList


__version__ = '0.0.1'

class UserManager():
    """
    This object is used to initialize the AccountManager in one of two ways:
    user_manager = AccountManager(app), or
    user_manager = AccountManager(); user_manager.init_app(app)
    """
    def __init__(self, db_adapter):
        import views
        import forms

        self.db_adapter = db_adapter

        # Customizable view functions **
        self.register_view_function = views.register
        self.login_view_function  = views.login
        self.logout_view_function = views.logout

        # Customizable forms **
        self.register_form = forms.RegisterForm
        self.login_form = forms.LoginForm

        # Customizable validators **
        self.password_validator = forms.password_validator

        # Customizable endpoints
        self.logout_next = None

        # Customizable passlib crypt context
        self.crypt_context = CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')
                # See https://pythonhosted.org/passlib/new_app_quickstart.html#choosing-a-hash

    def init_app(self, app):
        """
        Initialize AccountManager with a specific application.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        """

        # Set default features
        self.feature_register        = app.config.setdefault('USER_FEATURE_REGISTER',        True)
        self.feature_invite          = app.config.setdefault('USER_FEATURE_INVITE', True)
        self.feature_change_password = app.config.setdefault('USER_FEATURE_CHANGE_PASSWORD', True)
        self.feature_forget_password = app.config.setdefault('USER_FEATURE_FORGOT_PASSWORD', True)
        self.feature_confirm_email   = app.config.setdefault('USER_FEATURE_CONFIRM_EMAIL',   True)

        # Set default settings
        self.login_with_username           = app.config.setdefault('USER_LOGIN_WITH_USERNAME',        False)
        self.login_with_email              = app.config.setdefault('USER_LOGIN_WITH_EMAIL',           True)
        self.register_with_retype_password = app.config.setdefault('USER_REGISTER_WITH_RETYPE_PASSWORD', False)

        # Set default URLs
        self.register_url       = app.config.setdefault('USER_REGISTER_URL', '/user/register')
        self.login_url          = app.config.setdefault('USER_LOGIN_URL',  '/user/sign-in')
        self.logout_url         = app.config.setdefault('USER_LOGOUT_URL', '/user/sign-out')

        # Set default template files
        self.register_template  = app.config.setdefault('USER_REGISTER_TEMPLATE', 'flask_user/register.html')
        self.login_template     = app.config.setdefault('USER_LOGIN_TEMPLATE',  'flask_user/login.html')

        # Set default flash messages
        self.flash_signed_in    = app.config.setdefault('USER_FLASH_SIGNED_IN',  'You have signed in successfully.')
        self.flash_signed_out   = app.config.setdefault('USER_FLASH_SIGNED_OUT', 'You have signed out successfully.')

        # Setup Flask-Login
        self.lm = LoginManager()
        #self.lm.anonymous_user = AnonymousUser
        self.lm.login_view = 'user.login'
        self.lm.user_loader(_user_loader)
        #login_manager.token_loader(_token_loader)

        #if cv('FLASH_MESSAGES', app=app):
        #    lm.login_message, lm.login_message_category = cv('MSG_LOGIN', app=app)
        #    lm.needs_refresh_message, lm.needs_refresh_message_category = cv('MSG_REFRESH', app=app)
        #else:
        #    lm.login_message = None
        #    lm.needs_refresh_message = None

        self.lm.init_app(app)

        # # Initialize Flask-Principal
        # principal = Principal(app, use_sessions=False)
        # principal.identity_loader(_identity_loader)
        # self.principal = principal

        # Add URL Routes
        app.add_url_rule(self.register_url, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.login_url,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.logout_url, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])

        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add context processor
        app.context_processor(_account_context_processor)

        app.user_manager = self

# class AnonymousUser(AnonymousUserMixin):
#     """AnonymousUser definition"""
#
#     def __init__(self):
#         self.roles = ImmutableList()
#
#     def has_role(self, *args):
#         """Returns `False`"""
#         return False

class DBInterface(object):
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
    def __init__(self, db, UserClass, EmailClass=None):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass, EmailClass)

    def add_user(self, **kwargs):
        self.db.session.add(self.UserClass(**kwargs))
        self.db.session.commit()

    def find_user_by_id(self, id):
        return self.EmailClass.query.get(id)

    def find_user_by_email(self, email):
        return self.EmailClass.query.filter(self.EmailClass.email==email).first()

    def find_user_by_username(self, username):
        return self.UserClass.query.filter(self.UserClass.username==username).first()

def _account_context_processor():
    return dict(
        user_manager=current_app.user_manager
    )

def _user_loader(user_id):
    um = current_app.user_manager
    return um.db_adapter.find_user_by_id(id=user_id)
