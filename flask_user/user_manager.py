""" Flask-User is a customizable user account management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""


from flask import Blueprint, current_app, Flask, url_for, render_template
from flask_login import LoginManager, current_user

from flask_user.managers.email_manager import EmailManager
from flask_user.managers.password_manager import PasswordManager
from flask_user.managers.token_manager import TokenManager
from . import forms
from . import signals
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

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class UserManager():
    """ Customizable User Authentication and Management."""

    # ***** Initialization methods *****

    def __init__(self, app=None, db=None, UserClass=None, **kwargs):
        """
        Args:
            app(Flask): The Flask application instance.
            db: An Object-Database Mapper instance such as SQLAlchemy or MongoAlchemy.
            UserClass: The User data-model Class (*not* an instance!)
        Keyword Args:
            UserEmailClass: The optional UserEmail data-model Class (*not* an instance!).
                Needed for the multiple emails per user feature.

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
                 send_email_function = None,
                 make_safe_url_function = views.make_safe_url):
        """ Initialize UserManager,."""

        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code

        from flask_sqlalchemy import SQLAlchemy
        if isinstance(db, SQLAlchemy):
            from .db_adapters import SQLAlchemyDbAdapter
            self.db_adapter = SQLAlchemyDbAdapter(db)

        from flask_mongoalchemy import MongoAlchemy
        if isinstance(db, MongoAlchemy):
            from .db_adapters import MongoAlchemyDbAdapter
            self.db_adapter = MongoAlchemyDbAdapter(db)

        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_user.UserManager.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

        # Start moving the Model attributes from db_adapter to user_manager
        self.db = db
        self.UserClass = UserClass
        self.UserEmailClass = UserEmailClass
        self.UserInvitationClass = UserInvitationClass

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
        self._create_default_attr('make_safe_url_function', make_safe_url_function)

        # Setup PasswordManager
        self.password_manager = PasswordManager(self.password_crypt_context, self.password_hash_scheme, self.password_hash_mode, self.password_salt)

        # Setup EmailManager
        self.email_manager = EmailManager(self, self.send_email_function)

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
        """ This method can be overridden to set Flask-User settings """
        pass
    
    
    def _create_default_settings(self, app):
        """ Set default app.config settings, but only if they have not been set before """
        # sets self.attribute = self.ATTRIBUTE or app.config.USER_ATTRIBUTE or default_value

        # Create default features
        self._create_default_setting('enable_change_password',     app, True)
        self._create_default_setting('enable_email',               app, True)
        self._create_default_setting('enable_confirm_email',       app, self.enable_email)
        self._create_default_setting('enable_forgot_password',     app, self.enable_email)
        self._create_default_setting('enable_login_without_confirm_email', app, False)
        self._create_default_setting('enable_multiple_emails',     app, False)
        self._create_default_setting('enable_register',            app, True)
        self._create_default_setting('enable_remember_me',         app, True)
        self._create_default_setting('enable_retype_password',     app, True)
        self._create_default_setting('enable_username',            app, True)
        self._create_default_setting('enable_change_username',     app, self.enable_username)

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
        self._create_default_setting('password_hash_scheme',       app, 'bcrypt')
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
        self._create_default_setting('home_endpoint',                  app, '')
        self._create_default_setting('login_endpoint',                 app, 'user.login')
        self._create_default_setting('after_change_password_endpoint', app, self.home_endpoint)
        self._create_default_setting('after_change_username_endpoint', app, self.home_endpoint)
        self._create_default_setting('after_confirm_endpoint',         app, self.home_endpoint)
        self._create_default_setting('after_forgot_password_endpoint', app, self.home_endpoint)
        self._create_default_setting('after_login_endpoint',           app, self.home_endpoint)
        self._create_default_setting('after_logout_endpoint',          app, self.login_endpoint)
        self._create_default_setting('after_register_endpoint',        app, self.home_endpoint)
        self._create_default_setting('after_resend_confirm_email_endpoint', app, self.home_endpoint)
        self._create_default_setting('after_reset_password_endpoint',  app, self.home_endpoint)
        self._create_default_setting('after_invite_endpoint',          app, self.home_endpoint)
        self._create_default_setting('unconfirmed_email_endpoint',     app, self.home_endpoint)
        self._create_default_setting('unauthenticated_endpoint',       app, self.login_endpoint)
        self._create_default_setting('unauthorized_endpoint',          app, self.home_endpoint)

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
        if self.enable_invitation and not self.UserInvitationClass:
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
        if self.UserEmailClass:
            app.add_url_rule(self.email_action_url,  'user.email_action',  self.email_action_view_function)
            app.add_url_rule(self.manage_emails_url, 'user.manage_emails', self.manage_emails_view_function, methods=['GET', 'POST'])
        app.add_url_rule(self.user_profile_url,  'user.profile',  self.user_profile_view_function,  methods=['GET', 'POST'])
        if self.enable_invitation:
            app.add_url_rule(self.invite_url, 'user.invite', self.invite_view_function, methods=['GET', 'POST'])

    def get_user_by_id(self, user_id):
        return self.db_adapter.get_object(self.UserClass, user_id)

    def get_user_email_by_id(self, user_email_id):
        return self.db_adapter.get_object(self.UserEmailClass, user_email_id)

    def find_user_by_username(self, username):
        return self.db_adapter.ifind_first_object(self.UserClass, username=username)

    def find_user_by_email(self, email):
        if self.UserEmailClass:
            user_email = self.db_adapter.ifind_first_object(self.UserEmailClass, email=email)
            user = user_email.user if user_email else None
        else:
            user_email = None
            user = self.db_adapter.ifind_first_object(self.UserClass, email=email)

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
            current_username = current_user.username
            if new_username == current_username:
                return True
        # See if new_username is available
        return self.find_user_by_username(new_username)==None

    def send_reset_password_email(self, email):
        # Find user by email
        user, user_email = self.find_user_by_email(email)
        if user:
            # Generate reset password link
            token = self.token_manager.generate_token(user.id)
            reset_password_link = url_for('user.reset_password', token=token, _external=True)

            # Send forgot password email
            self.email_manager.send_email_forgot_password(user, user_email, reset_password_link)

            # Send forgot_password signal
            signals.user_forgot_password.send(current_app._get_current_object(), user=user)

    def get_primary_user_email(self, user):
        db_adapter = self.db_adapter
        if self.UserEmailClass:
            user_email = db_adapter.find_first_object(self.UserEmailClass,
                                                      user_id=user.id,
                                                      is_primary=True)
            return user_email
        else:
            return user

