""" Flask-User is a customizable user account management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from passlib.context import CryptContext
from flask import Blueprint, current_app, url_for, render_template
from flask_login import LoginManager, UserMixin as LoginUserMixin
from flask_user.db_adapters import DBAdapter
from .db_adapters import SQLAlchemyAdapter
from . import emails
from . import forms
from . import passwords
from . import tokens
from . import translations
from . import views
from . import signals
from .translations import get_translations

# Enable the following: from flask_user import current_user
from flask_login import current_user

# Enable the following: from flask_user import login_required, roles_required
from .decorators import *
# Enable the following: from flask_user import user_logged_in
from .signals import *


__version__ = '0.9'


def _call_or_get(function_or_property):
    return function_or_property() if callable(function_or_property) else function_or_property


def _flask_user_context_processor():
    """ Make 'user_manager' available to Jinja2 templates"""
    return dict(
        user_manager=current_app.user_manager,
        call_or_get=_call_or_get)

class UserManager(object):
    """ This is the Flask-User object that manages the User management process."""

    def __init__(self, app=None, **kwargs):
        """ Initialize UserManager, with or without an app """
        if app:
            self.init_app(app, **kwargs)

    def _init_settings(self, app):
        """ Set default app.config settings, but only if they have not been set before """
        # define short names

        # General settings
        self.app_name =                 app.config.get('USER_APP_NAME', 'AppName')

        # Set default features
        self.enable_change_password =   app.config.get('USER_ENABLE_CHANGE_PASSWORD', True)
        self.enable_change_username =   app.config.get('USER_ENABLE_CHANGE_USERNAME', True)
        self.enable_email =             app.config.get('USER_ENABLE_EMAIL', False)
        self.enable_confirm_email =     app.config.get('USER_ENABLE_CONFIRM_EMAIL', self.enable_email)
        self.enable_forgot_password =   app.config.get('USER_ENABLE_FORGOT_PASSWORD', self.enable_email)
        self.enable_login_without_confirm_email = app.config.get('USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL', False)
        self.enable_multiple_emails =   app.config.get('USER_ENABLE_MULTIPLE_EMAILS', False)
        self.enable_register =          app.config.get('USER_ENABLE_REGISTER', True)
        self.enable_remember_me =       app.config.get('USER_ENABLE_REMEMBER_ME', True)
        self.enable_retype_password =   app.config.get('USER_ENABLE_RETYPE_PASSWORD', True)
        self.enable_username =          app.config.get('USER_ENABLE_USERNAME', True)

        # Set default settings
        self.auto_login =               app.config.get('USER_AUTO_LOGIN', True)
        self.auto_login_after_confirm = app.config.get('USER_AUTO_LOGIN_AFTER_CONFIRM', self.auto_login)
        self.auto_login_after_register = app.config.get('USER_AUTO_LOGIN_AFTER_REGISTER', self.auto_login)
        self.auto_login_after_reset_password = app.config.get('USER_AUTO_LOGIN_AFTER_RESET_PASSWORD', self.auto_login)
        self.auto_login_at_login =      app.config.get('USER_AUTO_LOGIN_AT_LOGIN', self.auto_login)
        self.confirm_email_expiration = app.config.get('USER_CONFIRM_EMAIL_EXPIRATION', 2 * 24 * 3600)  # 2 days
        self.invite_expiration =        app.config.get('USER_INVITE_EXPIRATION', 90 * 24 * 3600)  # 90 days
        self.password_hash_mode =       app.config.get('USER_PASSWORD_HASH_MODE', 'passlib')
        self.password_hash =            app.config.get('USER_PASSWORD_HASH', 'bcrypt')
        self.password_salt =            app.config.get('USER_PASSWORD_SALT', app.config['SECRET_KEY'])
        self.reset_password_expiration = app.config.get('USER_RESET_PASSWORD_EXPIRATION', 2 * 24 * 3600)  # 2 days
        self.enable_invitation =        app.config.get('USER_ENABLE_INVITATION', False)
        self.require_invitation =       app.config.get('USER_REQUIRE_INVITATION', False)
        self.send_password_changed_email = app.config.get('USER_SEND_PASSWORD_CHANGED_EMAIL', self.enable_email)
        self.send_registered_email =    app.config.get('USER_SEND_REGISTERED_EMAIL', self.enable_email)
        self.send_username_changed_email = app.config.get('USER_SEND_USERNAME_CHANGED_EMAIL', self.enable_email)
        self.show_username_email_does_not_exist = app.config.get('USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST', self.enable_register)

        # Set default URLs
        self.change_password_url =      app.config.get('USER_CHANGE_PASSWORD_URL', '/user/change-password')
        self.change_username_url =      app.config.get('USER_CHANGE_USERNAME_URL', '/user/change-username')
        self.confirm_email_url =        app.config.get('USER_CONFIRM_EMAIL_URL', '/user/confirm-email/<token>')
        self.email_action_url =         app.config.get('USER_EMAIL_ACTION_URL', '/user/email/<id>/<action>')
        self.forgot_password_url =      app.config.get('USER_FORGOT_PASSWORD_URL', '/user/forgot-password')
        self.login_url =                app.config.get('USER_LOGIN_URL', '/user/sign-in')
        self.logout_url =               app.config.get('USER_LOGOUT_URL', '/user/sign-out')
        self.manage_emails_url =        app.config.get('USER_MANAGE_EMAILS_URL', '/user/manage-emails')
        self.register_url =             app.config.get('USER_REGISTER_URL', '/user/register')
        self.resend_confirm_email_url = app.config.get('USER_RESEND_CONFIRM_EMAIL_URL', '/user/resend-confirm-email')
        self.reset_password_url =       app.config.get('USER_RESET_PASSWORD_URL', '/user/reset-password/<token>')
        self.user_profile_url =         app.config.get('USER_PROFILE_URL', '/user/profile')
        self.invite_url =               app.config.get('USER_INVITE_URL', '/user/invite')

        # Set default ENDPOINTs
        home_endpoint = ''
        login_endpoint = self.login_endpoint = 'user.login'
        self.after_change_password_endpoint = app.config.get('USER_AFTER_CHANGE_PASSWORD_ENDPOINT', home_endpoint)
        self.after_change_username_endpoint = app.config.get('USER_AFTER_CHANGE_USERNAME_ENDPOINT', home_endpoint)
        self.after_confirm_endpoint = app.config.get('USER_AFTER_CONFIRM_ENDPOINT', home_endpoint)
        self.after_forgot_password_endpoint = app.config.get('USER_AFTER_FORGOT_PASSWORD_ENDPOINT', home_endpoint)
        self.after_login_endpoint = app.config.get('USER_AFTER_LOGIN_ENDPOINT', home_endpoint)
        self.after_logout_endpoint = app.config.get('USER_AFTER_LOGOUT_ENDPOINT', login_endpoint)
        self.after_register_endpoint = app.config.get('USER_AFTER_REGISTER_ENDPOINT', home_endpoint)
        self.after_resend_confirm_email_endpoint = app.config.get('USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT', home_endpoint)
        self.after_reset_password_endpoint = app.config.get('USER_AFTER_RESET_PASSWORD_ENDPOINT', home_endpoint)
        self.after_invite_endpoint = app.config.get('USER_INVITE_ENDPOINT', home_endpoint)
        self.unconfirmed_email_endpoint = app.config.get('USER_UNCONFIRMED_EMAIL_ENDPOINT', home_endpoint)
        self.unauthenticated_endpoint = app.config.get('USER_UNAUTHENTICATED_ENDPOINT', login_endpoint)
        self.unauthorized_endpoint = app.config.get('USER_UNAUTHORIZED_ENDPOINT', home_endpoint)

        # Set default template files
        self.change_password_template = app.config.get('USER_CHANGE_PASSWORD_TEMPLATE', 'flask_user/change_password.html')
        self.change_username_template = app.config.get('USER_CHANGE_USERNAME_TEMPLATE', 'flask_user/change_username.html')
        self.forgot_password_template = app.config.get('USER_FORGOT_PASSWORD_TEMPLATE', 'flask_user/forgot_password.html')
        self.login_template = app.config.get('USER_LOGIN_TEMPLATE', 'flask_user/login.html')
        self.manage_emails_template = app.config.get('USER_MANAGE_EMAILS_TEMPLATE', 'flask_user/manage_emails.html')
        self.register_template = app.config.get('USER_REGISTER_TEMPLATE', 'flask_user/register.html')
        self.resend_confirm_email_template = app.config.get('USER_RESEND_CONFIRM_EMAIL_TEMPLATE',
                                              'flask_user/resend_confirm_email.html')
        self.reset_password_template = app.config.get('USER_RESET_PASSWORD_TEMPLATE', 'flask_user/reset_password.html')
        self.user_profile_template = app.config.get('USER_PROFILE_TEMPLATE', 'flask_user/user_profile.html')
        self.invite_template = app.config.get('USER_INVITE_TEMPLATE', 'flask_user/invite.html')
        self.invite_accept_template = app.config.get('USER_INVITE_ACCEPT_TEMPLATE', 'flask_user/register.html')

        # Set default email template files
        self.confirm_email_email_template = app.config.get('USER_CONFIRM_EMAIL_EMAIL_TEMPLATE', 'flask_user/emails/confirm_email')
        self.forgot_password_email_template = app.config.get('USER_FORGOT_PASSWORD_EMAIL_TEMPLATE',
                                               'flask_user/emails/forgot_password')
        self.password_changed_email_template = app.config.get('USER_PASSWORD_CHANGED_EMAIL_TEMPLATE',
                                                'flask_user/emails/password_changed')
        self.registered_email_template = app.config.get('USER_REGISTERED_EMAIL_TEMPLATE', 'flask_user/emails/registered')
        self.username_changed_email_template = app.config.get('USER_USERNAME_CHANGED_EMAIL_TEMPLATE',
                                                'flask_user/emails/username_changed')
        self.invite_email_template = app.config.get('USER_INVITE_EMAIL_TEMPLATE', 'flask_user/emails/invite')


    def _check_settings(self):
        """ Verify config combinations. Produce a helpful error messages for inconsistent combinations."""

        # Define custom Exception
        class ConfigurationError(Exception):
            pass

        # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.
        if self.enable_register and not (self.enable_username or self.enable_email):
            raise ConfigurationError('USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.')
        # USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True
        if self.enable_confirm_email and not self.enable_email:
            raise ConfigurationError('USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True.')
        # USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True
        if self.enable_multiple_emails and not self.enable_email:
            raise ConfigurationError('USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True.')
        # USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True
        if self.send_registered_email and not self.enable_email:
            raise ConfigurationError('USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True.')
        # USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.
        if self.enable_change_username and not self.enable_username:
            raise ConfigurationError('USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.')
        if self.require_invitation and not self.enable_invitation:
            raise ConfigurationError('USER_REQUIRE_INVITATION=True must have USER_ENABLE_INVITATION=True.')
        if self.enable_invitation and not self.db_adapter.UserInvitationClass:
            raise ConfigurationError(
                'USER_ENABLE_INVITATION=True must pass UserInvitationClass to SQLAlchemyAdapter().')

    def customize(self, app):
        pass

    def init_app(self, app,
                # Forms
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
                login_manager=LoginManager(),
                password_crypt_context=None,
                send_email_function = emails.send_email,
                token_manager=tokens.TokenManager(),
                legacy_check_password_hash=None):

        """ Initialize the UserManager object """
        self.db_adapter = None
        self.app = app

        # Forms
        self.add_email_form = add_email_form
        self.change_password_form = change_password_form
        self.change_username_form = change_username_form
        self.forgot_password_form = forgot_password_form
        self.login_form = login_form
        self.register_form = register_form
        self.resend_confirm_email_form = resend_confirm_email_form
        self.reset_password_form = reset_password_form
        self.invite_form = invite_form
        # Validators
        self.username_validator = username_validator
        self.password_validator = password_validator
        # View functions
        self.render_function = render_function
        self.change_password_view_function = change_password_view_function
        self.change_username_view_function = change_username_view_function
        self.confirm_email_view_function = confirm_email_view_function
        self.email_action_view_function = email_action_view_function
        self.forgot_password_view_function = forgot_password_view_function
        self.login_view_function = login_view_function
        self.logout_view_function = logout_view_function
        self.manage_emails_view_function = manage_emails_view_function
        self.register_view_function = register_view_function
        self.resend_confirm_email_view_function = resend_confirm_email_view_function
        self.reset_password_view_function = reset_password_view_function
        self.unconfirmed_email_view_function = unconfirmed_email_view_function
        self.unauthenticated_view_function = unauthenticated_view_function
        self.unauthorized_view_function = unauthorized_view_function
        self.user_profile_view_function = user_profile_view_function
        self.invite_view_function = invite_view_function
        # Misc
        self.login_manager = login_manager
        self.token_manager = token_manager
        self.password_crypt_context = password_crypt_context
        self.send_email_function = send_email_function
        self.legacy_check_password_hash = legacy_check_password_hash

        """ Initialize app.user_manager."""
        # Bind Flask-USER to app
        app.user_manager = self
        # Flask seems to also support the current_app.extensions[] list
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['user'] = self

        # Initialize settings
        self._init_settings(app)

        self.customize(app)

        # Make sure the settings are valid -- raise ConfigurationError if not
        self._check_settings()

        # Initialize Translations -- Only if Flask-Babel has been installed
        if hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.install_gettext_callables(
                    lambda x: get_translations().ugettext(x),
                    lambda s, p, n: get_translations().ungettext(s, p, n),
                    newstyle=True)
        else:
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations()


        # Create password_crypt_context if needed
        if not self.password_crypt_context:
            self.password_crypt_context = CryptContext(
                    schemes=[self.password_hash])

        # Setup Flask-Login
        self.setup_login_manager(app)

        # Setup TokenManager
        self.token_manager.setup(self.password_salt)

        # Add flask_user/templates directory using a Blueprint
        blueprint = Blueprint('flask_user', 'flask_user', template_folder='templates')
        app.register_blueprint(blueprint)

        # Add URL routes
        self.add_url_routes(app)

        # Add context processor
        app.context_processor(_flask_user_context_processor)

        # Prepare for translations
        _ = translations.gettext


    def setup_login_manager(self, app):

        # Flask-Login calls this function to retrieve a User record by user ID.
        # Note: user_id is a UNICODE string returned by UserMixin.get_id().
        # See https://flask-login.readthedocs.org/en/latest/#how-it-works
        @self.login_manager.user_loader
        def load_user_by_id(user_unicode_id):
            user_id = int(user_unicode_id)
            #print('load_user_by_id: user_id=', user_id)
            return self.get_user_by_id(user_id)

        self.login_manager.login_view = 'user.login'
        self.login_manager.init_app(app)


    def add_url_routes(self, app):
        """ Add URL Routes"""
        app.add_url_rule(self.login_url,  'user.login',  self.login_view_function,  methods=['GET', 'POST'])
        app.add_url_rule(self.logout_url, 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        if self.enable_confirm_email:
            app.add_url_rule(self.confirm_email_url, 'user.confirm_email', self.confirm_email_view_function)
            app.add_url_rule(self.resend_confirm_email_url, 'user.resend_confirm_email', self.resend_confirm_email_view_function, methods=['GET', 'POST'])
        if self.enable_change_password:
            app.add_url_rule(self.change_password_url, 'user.change_password', self.change_password_view_function, methods=['GET', 'POST'])
        if self.enable_change_username:
            app.add_url_rule(self.change_username_url, 'user.change_username', self.change_username_view_function, methods=['GET', 'POST'])
        if self.enable_forgot_password:
            app.add_url_rule(self.forgot_password_url, 'user.forgot_password', self.forgot_password_view_function, methods=['GET', 'POST'])
            app.add_url_rule(self.reset_password_url, 'user.reset_password', self.reset_password_view_function, methods=['GET', 'POST'])
        if self.enable_register:
            app.add_url_rule(self.register_url, 'user.register', self.register_view_function, methods=['GET', 'POST'])
        if self.db_adapter.UserEmailClass:
            app.add_url_rule(self.email_action_url,  'user.email_action',  self.email_action_view_function)
            app.add_url_rule(self.manage_emails_url, 'user.manage_emails', self.manage_emails_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.user_profile_url,  'user.profile',  self.user_profile_view_function,  methods=['GET', 'POST'])
        if self.enable_invitation:
            app.add_url_rule(self.invite_url, 'user.invite', self.invite_view_function, methods=['GET', 'POST'])
    # Obsoleted function. Replace with hash_password()
    def generate_password_hash(self, password):
        return passwords.hash_password(self, password)

    def hash_password(self, password):
        return passwords.hash_password(self, password)

    def get_password(self, user):
        use_auth_class = True if self.db_adapter.UserAuthClass and hasattr(user, 'user_auth') else False
        # Handle v0.5 backward compatibility
        if self.db_adapter.UserProfileClass:
            hashed_password = user.password
        else:
            hashed_password = user.user_auth.password if use_auth_class else user.password
        return hashed_password

    def update_password(self, user, hashed_password):
        use_auth_class = True if self.db_adapter.UserAuthClass and hasattr(user, 'user_auth') else False

        if use_auth_class:
            user.user_auth.password = hashed_password
        else:
            user.password = hashed_password
        self.db_adapter.commit()

    def verify_password(self, password, user):
        """
        Make it backward compatible to legacy password hash.
        In addition, if such password were found, update the user's password field.
        """
        verified = False
        hashed_password = self.get_password(user)

        try:
            verified = passwords.verify_password(self, password, hashed_password)
        except ValueError:
            legacy_check = self.legacy_check_password_hash
            if legacy_check:
                verified = legacy_check(hashed_password, password)
                if verified:
                    # update the hash
                    new_hash = self.hash_password(password)
                    self.update_password(user, new_hash)
        return verified

    def generate_token(self, user_id):
        return self.token_manager.generate_token(user_id)

    def verify_token(self, token, expiration_in_seconds):
        return self.token_manager.verify_token(token, expiration_in_seconds)

    def get_user_by_id(self, user_id):
        # Handle v0.5 backward compatibility
        ObjectClass = self.db_adapter.UserAuthClass if self.db_adapter.UserAuthClass and self.db_adapter.UserProfileClass else self.db_adapter.UserClass
        return self.db_adapter.get_object(ObjectClass, user_id)

    # NB: This backward compatibility function may be obsoleted in the future
    # Use 'get_user_by_id() instead.
    def find_user_by_id(self, user_id):
        print('Warning: find_user_by_id() will be deprecated in the future. User get_user_by_id() instead.')
        return self.get_user_by_id(user_id)

    def get_user_email_by_id(self, user_email_id):
        return self.db_adapter.get_object(self.db_adapter.UserEmailClass, user_email_id)

    # NB: This backward compatibility function may be obsoleted in the future
    # Use 'get_user_email_by_id() instead.
    def find_user_email_by_id(self, user_email_id):
        print('Warning: find_user_email_by_id() will be deprecated in the future. User get_user_email_by_id() instead.')
        return self.get_user_email_by_id(user_email_id)

    def find_user_by_username(self, username):
        user_auth = None

        # The username field can either be in the UserAuth class or in the User class
        if self.db_adapter.UserAuthClass and hasattr(self.db_adapter.UserAuthClass, 'username'):
            user_auth = self.db_adapter.ifind_first_object(self.db_adapter.UserAuthClass, username=username)

            # Handle v0.5 backward compatibility
            if self.db_adapter.UserProfileClass: return user_auth

            user = user_auth.user if user_auth else None
        else:
            user = self.db_adapter.ifind_first_object(self.db_adapter.UserClass, username=username)

        return user


    def find_user_by_email(self, email):
        user_email = None
        user_auth = None
        if self.db_adapter.UserEmailClass:
            user_email = self.db_adapter.ifind_first_object(self.db_adapter.UserEmailClass, email=email)
            user = user_email.user if user_email else None
        else:
            # The email field can either be in the UserAuth class or in the User class
            if self.db_adapter.UserAuthClass and hasattr(self.db_adapter.UserAuthClass, 'email'):
                user_auth = self.db_adapter.ifind_first_object(self.db_adapter.UserAuthClass, email=email)

                # Handle v0.5 backward compatibility
                if self.db_adapter.UserProfileClass: return (user_auth, user_email)

                user = user_auth.user if user_auth else None
            else:
                user = self.db_adapter.ifind_first_object(self.db_adapter.UserClass, email=email)

        return (user, user_email)

    def email_is_available(self, new_email):
        """ Return True if new_email does not exist.
            Return False otherwise."""
        user, user_email = self.find_user_by_email(new_email)
        return (user==None)

    def username_is_available(self, new_username):
        """ Return True if new_username does not exist or if new_username equals old_username.
            Return False otherwise."""
        # Allow user to change username to the current username
        if _call_or_get(current_user.is_authenticated):
            current_username = current_user.user_auth.username if self.db_adapter.UserAuthClass and hasattr(current_user, 'user_auth') else current_user.username
            if new_username == current_username:
                return True
        # See if new_username is available
        return self.find_user_by_username(new_username)==None

    def send_reset_password_email(self, email):
        # Find user by email
        user, user_email = self.find_user_by_email(email)
        if user:
            # Generate reset password link
            token = self.generate_token(int(user.get_id()))
            reset_password_link = url_for('user.reset_password', token=token, _external=True)

            # Send forgot password email
            emails.send_forgot_password_email(user, user_email, reset_password_link)

            # Store token
            if hasattr(user, 'reset_password_token'):
                self.db_adapter.update_object(user, reset_password_token=token)
                self.db_adapter.commit()

            # Send forgot_password signal
            signals.user_forgot_password.send(current_app._get_current_object(), user=user)


class UserMixin(LoginUserMixin):
    """ This class adds methods to the User model class required by Flask-Login and Flask-User."""

    def is_active(self):
        if hasattr(self, 'active'):
            return self.active
        else:
            return self.is_enabled


    def set_active(self, active):
        if hasattr(self, 'active'):
            self.active = active
        else:
            self.is_enabled = active


    def has_role(self, *specified_role_names):
        """ Return True if the user has one of the specified roles. Return False otherwise.

            has_roles() accepts a 1 or more role name parameters
                has_role(role_name1, role_name2, role_name3).

            For example:
                has_roles('a', 'b')
            Translates to:
                User has role 'a' OR role 'b'
        """

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles: return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # Return True if one of the role_names matches
        for role_name in specified_role_names:
            if role_name in user_role_names:
                return True

        # Return False if none of the role_names matches
        return False


    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.

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
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles: return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in user_role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in user_role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True


    # Flask-Login is capable of remembering the current user ID in the browser's session.
    # This function enables the user ID to be encrypted as a token.
    # See https://flask-login.readthedocs.org/en/latest/#remember-me
    def get_auth_token(self):
        token_manager = current_app.user_manager.token_manager
        user_id = int(self.get_id())
        token = token_manager.encrypt_id(user_id)
        #print('get_auth_token: user_id=', user_id, 'token=', token)
        return token


    def has_confirmed_email(self):
        db_adapter = current_app.user_manager.db_adapter

        # Handle multiple emails per user: Find at least one confirmed email
        if db_adapter.UserEmailClass:
            has_confirmed_email = False
            user_emails = db_adapter.find_all_objects(db_adapter.UserEmailClass, user_id=self.id)
            for user_email in user_emails:
                if user_email.confirmed_at:
                    has_confirmed_email = True
                    break

        # Handle single email per user
        else:
            has_confirmed_email = True if self.confirmed_at else False

        return has_confirmed_email
