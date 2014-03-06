"""
    flask_user
    ----------
    Flask-User is a customizable user management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from flask import Blueprint
from flask_login import LoginManager, UserMixin as LoginUserMixin
from flask_user.db_interfaces import DBInterface

from .db_interfaces import SQLAlchemyAdapter
from . import forms
from . import passwords
from . import settings
from . import tokens
from . import translations
from . import views

__version__ = '0.4.0'

# Enable the following: from flask.ext.user import current_user
from flask_login import current_user

# Enable the following: from flask.ext.user import login_required, roles_required
from .decorators import *

def _user_loader(user_id):
    """
    Flask-Login helper function to load user by user_id
    """
    user_manager = current_app.user_manager
    return user_manager.db_adapter.find_user_by_id(user_id=user_id)

def _flask_user_context_processor():
    """
    Make 'user_manager' available to Jinja2 templates
    """
    return dict(user_manager=current_app.user_manager)


class UserManager():
    """
    This is the Flask-User object that manages the User management process.
    """

    def __init__(self, db_adapter, app=None,
                # Forms
                change_password_form=forms.ChangePasswordForm,
                change_username_form=forms.ChangeUsernameForm,
                forgot_password_form=forms.ForgotPasswordForm,
                login_form=forms.LoginForm,
                register_form=forms.RegisterForm,
                reset_password_form=forms.ResetPasswordForm,
                # Validators
                username_validator=forms.username_validator,
                password_validator=forms.password_validator,
                # View functions
                change_password_view_function=views.change_password,
                change_username_view_function=views.change_username,
                confirm_email_view_function=views.confirm_email,
                forgot_password_view_function=views.forgot_password,
                login_view_function=views.login,
                logout_view_function=views.logout,
                register_view_function=views.register,
                resend_confirmation_email_view_function = views.resend_confirmation_email,
                reset_password_view_function = views.reset_password,
                unauthenticated_view_function = views.unauthenticated,
                unauthorized_view_function = views.unauthorized,
                # Misc
                login_manager=LoginManager(),
                token_manager=tokens.TokenManager(),
                password_crypt_context=passwords.crypt_context,
                ):
        """
        Initialize the UserManager with custom or built-in attributes
        """
        self.db_adapter = db_adapter
        self.lm = login_manager
        # Forms
        self.change_password_form = change_password_form
        self.change_username_form = change_username_form
        self.forgot_password_form = forgot_password_form
        self.login_form = login_form
        self.register_form = register_form
        self.reset_password_form = reset_password_form
        # Validators
        self.username_validator = username_validator
        self.password_validator = password_validator
        # View functions
        self.change_password_view_function = change_password_view_function
        self.change_username_view_function = change_username_view_function
        self.confirm_email_view_function = confirm_email_view_function
        self.forgot_password_view_function = forgot_password_view_function
        self.login_view_function = login_view_function
        self.logout_view_function = logout_view_function
        self.register_view_function = register_view_function
        self.resend_confirmation_email_view_function = resend_confirmation_email_view_function
        self.reset_password_view_function = reset_password_view_function
        self.unauthenticated_view_function = unauthenticated_view_function
        self.unauthorized_view_function = unauthorized_view_function
        # Misc
        self.password_crypt_context = password_crypt_context
        self.token_manager = token_manager

        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize app.user_manager.
        """
        app.user_manager = self

        # Initialize Translations
        app.jinja_env.install_gettext_callables(
                translations.gettext,
                translations.ngettext,
                newstyle=True
                )

        # Set default app.config settings, but only if they have not been set before
        settings.set_default_settings(self, app.config)

        # Verify config combinations. Produce a helpful error messages for invalid combinations.
        settings.check_settings(self)

        # Setup Flask-Login
        self.setup_login_manager(app)

        # Setup TokenManager
        self.token_manager.setup(app.config.get('SECRET_KEY'))

        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add URL routes
        self.add_url_routes(app)

        # Add context processor
        app.context_processor(_flask_user_context_processor)

    def setup_login_manager(self, app):
        _ = translations.gettext
        self.lm.login_message = _('Please Sign in to access this page.')
        self.lm.login_message_category = 'error'
        self.lm.login_view = 'user.login'
        self.lm.user_loader(_user_loader)
        #login_manager.token_loader(_token_loader)
        self.lm.init_app(app)

    def add_url_routes(self, app):
        # Add URL Routes
        if self.enable_confirm_email:
            app.add_url_rule(self.confirm_email_url, 'user.confirm_email', self.confirm_email_view_function)
            app.add_url_rule(self.resend_confirmation_email_url, 'user.resend_confirmation_email', self.resend_confirmation_email_view_function)
        if self.enable_change_password:
            app.add_url_rule(self.change_password_url, 'user.change_password', self.change_password_view_function, methods=['GET', 'POST'])
        if self.enable_change_username:
            app.add_url_rule(self.change_username_url, 'user.change_username', self.change_username_view_function, methods=['GET', 'POST'])
        if self.enable_forgot_password:
            app.add_url_rule(self.forgot_password_url, 'user.forgot_password', self.forgot_password_view_function, methods=['GET', 'POST'])
            app.add_url_rule(self.reset_password_url, 'user.reset_password', self.reset_password_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.login_url,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.logout_url, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        if self.enable_register:
            app.add_url_rule(self.register_url, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        # We can not define 'user.unauthenticated' here because it clashes with 'user.login'
        # We can not define 'user.unauthorized' here because it clashes with 'home_page'



class UserMixin(LoginUserMixin):
    """
    This class adds methods to the User model class required by Flask-Login and Flask-User.
    """
    
    def has_roles(self, *requirements):
        """
        Return True if the user has all of the specified roles. Return False otherwise.
        
        has_roles() accepts a list of requirements:
            has_role(requirement1, requirement2, requirement3).
            
        Each requirement is either a role_name, or a tuple_of_role_names.
            role_name example:   'manager'
            tuple_of_role_names: ('funny', 'witty', 'hilarious')
        A role_name-requirement is accepted when the user has this role.
        A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
        has_roles() returns true if ALL of the requirements have been accepted.
         
        For example:
            has_roles('a', ('b', 'c'), d)
        Translates to:
            User has role 'a' AND (role 'b' OR role 'c') AND role 'd'
        """

        # Translates a list of role objects to a list of role_names
        user_roles = [role.name for role in self.roles]

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in user_roles:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in user_roles:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True
