""" Flask-User is a customizable user account management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from flask import Blueprint, current_app, Flask, url_for, render_template
from flask_login import LoginManager, UserMixin as LoginUserMixin
from flask_user.db_adapters import DBAdapter
from .db_adapters import SQLAlchemyAdapter
from .password_mixin import PasswordMixin
from .send_email_mixin import SendEmailMixin
from .token_mixin import TokenMixin
from . import send_email_mixin
from . import forms
from . import signals
from . import translations
from .translations import get_translations
from . import views

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

class UserManager(PasswordMixin, SendEmailMixin, TokenMixin):
    """ This is the Flask-User object that manages the User management process."""

    # ***** Initialization methods *****

    def __init__(self, app=None, db_adapter=None, **kwargs):
        """ Initialize UserManager, with or without an app """
        self.app = app              # Make sure to set self.app here
                                    # See http://flask.pocoo.org/docs/0.11/extensiondev/
        if app:
            self.init_app(app, db_adapter, **kwargs)

    def init_app(self, app, db_adapter=None,
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
                 login_manager = None,
                 password_crypt_context = None,
                 send_email_function = None):
        """ Initialize the UserManager object """

        # Make sure to NOT set self.app here
        # See http://flask.pocoo.org/docs/0.11/extensiondev/

        # Perform some Python magic to allow for:
        # - v0.6  init_app(db_adapter, app), and
        # - v0.9+ init_app(app, db_adapter) parameter order
        if isinstance(app, DBAdapter) or isinstance(db_adapter, Flask):
            # Switch v0.6 parameter order
            temp = app
            app = db_adapter
            db_adapter = temp

        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)
        if not isinstance(db_adapter, DBAdapter):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'db_adapter' is instance of class '%s' "
                            "instead of a subclass of 'flask_user.DBAdapter'."
                            % app.__class__.__name__)

        self.db_adapter = db_adapter

        # Bind Flask-USER to app
        app.user_manager = self
        # Flask seems to also support the current_app.extensions[] list
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['user'] = self

        # Initialize Translations -- Only if Flask-Babel has been installed
        if hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.install_gettext_callables(
                    lambda x: get_translations().ugettext(x),
                    lambda s, p, n: get_translations().ungettext(s, p, n),
                    newstyle=True)
        else:
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations()

        # Allow CustomUserManager to customize certain settings
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
        self._create_default_attr('send_email_function', send_email_function)

        # Initialize PasswordMixin
        self.init_password_mixin()

        # Initialize SendEmailMixin
        if not self.send_email_function:
            self.send_email_function = self.send_email
            self.init_email_mixin()

        # Setup default TokenManager
        self.init_token_mixin(self.password_salt)

        # Setup default LoginManager using Flask-Login
        if not self.login_manager:
            self.login_manager = LoginManager(app)
            self.login_manager.login_view = 'user.login'

            # Flask-Login calls this function to retrieve a User record by user ID.
            # Note: user_id is a UNICODE string returned by UserMixin.get_id().
            # See https://flask-login.readthedocs.org/en/latest/#how-it-works
            @self.login_manager.user_loader
            def load_user_by_user_token(user_token):
                # decode token
                is_valid, has_expired, user_id = self.verify_token(
                    user_token,
                    3600)  # timeout in seconds
                # print("load_user_by_user_token(): is_valid:", is_valid, "has_expired:", has_expired, "user_id:", user_id)

                # verify token
                if not is_valid or has_expired:
                    return None

                # load user by user ID
                user = self.get_user_by_id(user_id)
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
        """ This method can be overridden to set Flask-User settings """
        pass
    
    
    def _create_default_settings(self, app):
        """ Set default app.config settings, but only if they have not been set before """
        # sets self.attribute = self.ATTRIBUTE or app.config.USER_ATTRIBUTE or default_value

        # Create default features
        self._create_default_setting('enable_change_password',     app, True)
        self._create_default_setting('enable_change_username',     app, True)
        self._create_default_setting('enable_email',               app, True)
        self._create_default_setting('enable_confirm_email',       app, self.enable_email)
        self._create_default_setting('enable_forgot_password',     app, self.enable_email)
        self._create_default_setting('enable_login_without_confirm_email', app, False)
        self._create_default_setting('enable_multiple_emails',     app, False)
        self._create_default_setting('enable_register',            app, True)
        self._create_default_setting('enable_remember_me',         app, True)
        self._create_default_setting('enable_retype_password',     app, True)
        self._create_default_setting('enable_username',            app, True)

        # Create default settings
        self._create_default_setting('app_name',                   app, 'MyApp')
        self._create_default_setting('auto_login',                 app, True)
        self._create_default_setting('auto_login_after_confirm',   app, self.auto_login)
        self._create_default_setting('auto_login_after_register',  app, self.auto_login)
        self._create_default_setting('auto_login_after_reset_password', app, self.auto_login)
        self._create_default_setting('auto_login_at_login',        app, self.auto_login)
        self._create_default_setting('confirm_email_expiration',   app, 2 * 24 * 3600)  # 2 days
        self._create_default_setting('invite_expiration',          app, 90 * 24 * 3600)  # 90 days
        self._create_default_setting('password_hash_mode',         app, 'passlib')
        self._create_default_setting('password_hash',              app, 'bcrypt')
        self._create_default_setting('password_salt',              app, app.config['SECRET_KEY'])
        self._create_default_setting('reset_password_expiration',  app, 2 * 24 * 3600)  # 2 days
        self._create_default_setting('enable_invitation',          app, False)
        self._create_default_setting('require_invitation',         app, False)
        self._create_default_setting('send_password_changed_email',app, self.enable_email)
        self._create_default_setting('send_registered_email',      app, self.enable_email)
        self._create_default_setting('send_username_changed_email',app, self.enable_email)
        self._create_default_setting('show_username_email_does_not_exist', app, self.enable_register)

        # Create default URLs
        self._create_default_setting('base_url',                   app, '/user')
        self._create_default_setting('change_password_url',        app, self.base_url+'/change-password')
        self._create_default_setting('change_username_url',        app, self.base_url+'/change-username')
        self._create_default_setting('confirm_email_url',          app, self.base_url+'/confirm-email/<token>')
        self._create_default_setting('email_action_url',           app, self.base_url+'/email/<id>/<action>')
        self._create_default_setting('forgot_password_url',        app, self.base_url+'/forgot-password')
        self._create_default_setting('login_url',                  app, self.base_url+'/sign-in')
        self._create_default_setting('logout_url',                 app, self.base_url+'/sign-out')
        self._create_default_setting('manage_emails_url',          app, self.base_url+'/manage-emails')
        self._create_default_setting('register_url',               app, self.base_url+'/register')
        self._create_default_setting('resend_confirm_email_url',   app, self.base_url+'/resend-confirm-email')
        self._create_default_setting('reset_password_url',         app, self.base_url+'/reset-password/<token>')
        self._create_default_setting('user_profile_url',           app, self.base_url+'/profile')
        self._create_default_setting('invite_url',                 app, self.base_url+'/invite')

        # Create default ENDPOINTs
        home_endpoint = ''
        login_endpoint = 'user.login'
        self._create_default_setting('after_change_password_endpoint', app, home_endpoint)
        self._create_default_setting('after_change_username_endpoint', app, home_endpoint)
        self._create_default_setting('after_confirm_endpoint',         app, home_endpoint)
        self._create_default_setting('after_forgot_password_endpoint', app, home_endpoint)
        self._create_default_setting('after_login_endpoint',           app, home_endpoint)
        self._create_default_setting('after_logout_endpoint',          app, login_endpoint)
        self._create_default_setting('after_register_endpoint',        app, home_endpoint)
        self._create_default_setting('after_resend_confirm_email_endpoint', app, home_endpoint)
        self._create_default_setting('after_reset_password_endpoint',  app, home_endpoint)
        self._create_default_setting('after_invite_endpoint',          app, home_endpoint)
        self._create_default_setting('unconfirmed_email_endpoint',     app, home_endpoint)
        self._create_default_setting('unauthenticated_endpoint',       app, login_endpoint)
        self._create_default_setting('unauthorized_endpoint',          app, home_endpoint)

        # Create default template files
        template_base = 'flask_user'
        self._create_default_setting('change_password_template',       app, template_base+'/change_password.html')
        self._create_default_setting('change_username_template',       app, template_base+'/change_username.html')
        self._create_default_setting('forgot_password_template',       app, template_base+'/forgot_password.html')
        self._create_default_setting('login_template',                 app, template_base+'/login.html')
        self._create_default_setting('manage_emails_template',         app, template_base+'/manage_emails.html')
        self._create_default_setting('register_template',              app, template_base+'/register.html')
        self._create_default_setting('resend_confirm_email_template',  app, template_base+'/resend_confirm_email.html')
        self._create_default_setting('reset_password_template',        app, template_base+'/reset_password.html')
        self._create_default_setting('user_profile_template',          app, template_base+'/user_profile.html')
        self._create_default_setting('invite_template',                app, template_base+'/invite.html')
        self._create_default_setting('invite_accept_template',         app, template_base+'/register.html')

        # Create default email template files
        self._create_default_setting('confirm_email_email_template',   app, template_base+'/emails/confirm_email')
        self._create_default_setting('forgot_password_email_template', app, template_base+'/emails/forgot_password')
        self._create_default_setting('password_changed_email_template',app, template_base+'/emails/password_changed')
        self._create_default_setting('registered_email_template',      app, template_base+'/emails/registered')
        self._create_default_setting('username_changed_email_template',app, template_base+'/emails/username_changed')
        self._create_default_setting('invite_email_template',          app, template_base+'/emails/invite')


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


    def _add_url_routes(self, app):
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

    def get_user_by_id(self, user_id):
        # Handle v0.5 backward compatibility
        ObjectClass = self.db_adapter.UserAuthClass if self.db_adapter.UserAuthClass and self.db_adapter.UserProfileClass else self.db_adapter.UserClass
        return self.db_adapter.get_object(ObjectClass, user_id)

    # NB: This backward compatibility function may be obsoleted in the future
    # Use 'get_user_by_id() instead.
    def find_user_by_id(self, user_id):
        print('Warning: find_user_by_id() will be deprecated in the future. Use get_user_by_id() instead.')
        return self.get_user_by_id(user_id)

    def get_user_email_by_id(self, user_email_id):
        return self.db_adapter.get_object(self.db_adapter.UserEmailClass, user_email_id)

    # NB: This backward compatibility function may be obsoleted in the future
    # Use 'get_user_email_by_id() instead.
    def find_user_email_by_id(self, user_email_id):
        print('Warning: find_user_email_by_id() will be deprecated in the future. Use get_user_email_by_id() instead.')
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
            token = self.generate_token(user.id)
            reset_password_link = url_for('user.reset_password', token=token, _external=True)

            # Send forgot password email
            self.send_email_forgot_password(user, user_email, reset_password_link)

            # Store token
            if hasattr(user, 'reset_password_token'):
                self.db_adapter.update_object(user, reset_password_token=token)
                self.db_adapter.commit()

            # Send forgot_password signal
            signals.user_forgot_password.send(current_app._get_current_object(), user=user)


class UserMixin(LoginUserMixin):
    """ This class adds methods to the User model class required by Flask-Login and Flask-User."""

    def get_id(self):
        """ Return a token string representing the user's ID """
        # Works in tandem with user_loader()
        user_manager = current_app.user_manager
        user_token = user_manager.generate_token(self.id)
        # print("UserMixin.get_id: ID:", self.id, "token:", user_token)
        return user_token


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
