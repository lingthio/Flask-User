"""
UserManager__Settings is a Mixin for UserManager that holds all Flask-User settings.
"""

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.

# This Settings Mixin documents all Flask-User settings through docstrings.
# Sphinx Autodoc builds the documentation from these docstrings.

class UserManager__Settings(object):
    """Flask-User settings and their defaults.

    .. note:: Feature settings and their defaults
    """

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

    #: | Allow unregistered users to be invited.
    USER_ENABLE_INVITE_USER = False

    #: | Allow unregistered users to register.
    USER_ENABLE_REGISTER = True

    #: | Remember user sessions across browser restarts.
    #:
    #: .. note:: Generic settings and their defaults
    USER_ENABLE_REMEMBER_ME = True


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
    #:
    #: .. note:: URL settings and their defaults
    USER_RESET_PASSWORD_EXPIRATION = 2*24*3600


    USER_CHANGE_PASSWORD_URL = '/user/change-password' #:
    USER_CHANGE_USERNAME_URL = '/user/change-username' #:
    USER_CONFIRM_EMAIL_URL = '/user/confirm-email/<token>' #:
    USER_EDIT_USER_PROFILE_URL = '/user/edit_user_profile' #:
    USER_EMAIL_ACTION_URL = '/user/email/<id>/<action>' #:
    USER_FORGOT_PASSWORD_URL = '/user/forgot-password' #:
    USER_INVITE_USER_URL = '/user/invite' #:
    USER_LOGIN_URL = '/user/sign-in' #:
    USER_LOGOUT_URL = '/user/sign-out' #:
    USER_MANAGE_EMAILS_URL = '/user/manage-email_templates' #:
    USER_REGISTER_URL = '/user/register' #:
    USER_RESEND_EMAIL_CONFIRMATION_URL = '/user/resend-email-confirmation' #:
    USER_RESET_PASSWORD_URL = '/user/reset-password/<token>' #: .. note:: template file settings and their defaults

    USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html' #:
    USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html' #:
    USER_EDIT_USER_PROFILE_TEMPLATE = 'flask_user/edit_user_profile.html' #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'flask_user/forgot_password.html' #:
    USER_INVITE_TEMPLATE = 'flask_user/invite_user.html' #:
    USER_INVITE_ACCEPT_TEMPLATE = 'flask_user/register.html' #:
    USER_LOGIN_TEMPLATE = 'flask_user/login.html' #:
    USER_MANAGE_EMAILS_TEMPLATE = 'flask_user/manage_emails.html' #:
    USER_REGISTER_TEMPLATE = 'flask_user/register.html' #:
    USER_RESEND_EMAIL_CONFIRMATION_TEMPLATE = 'flask_user/request_email_confirmation.html' #:
    USER_RESET_PASSWORD_TEMPLATE = 'flask_user/reset_password.html' #: .. note:: email template file settings and their defaults

    USER_CONFIRM_EMAIL_TEMPLATE = 'flask_user/email_templates/confirm_email' #:
    USER_INVITE_USER_EMAIL_TEMPLATE = 'flask_user/email_templates/invite_user' #:
    USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'flask_user/email_templates/password_changed' #:
    USER_REGISTERED_EMAIL_TEMPLATE = 'flask_user/email_templates/registered' #:
    USER_RESET_PASSWORD_EMAIL_TEMPLATE = 'flask_user/email_templates/reset_password' #:
    USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'flask_user/email_templates/username_changed' #: .. note:: Flask endpoint settings and their defaults

    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_CHANGE_USERNAME_ENDPOINT = '' #:
    USER_AFTER_CONFIRM_ENDPOINT = '' #:
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_LOGIN_ENDPOINT = '' #:
    USER_AFTER_LOGOUT_ENDPOINT = 'user.login' #:
    USER_AFTER_REGISTER_ENDPOINT = '' #:
    USER_AFTER_resend_email_confirmation_ENDPOINT = '' #:
    USER_AFTER_RESET_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_INVITE_ENDPOINT = '' #:
    USER_UNCONFIRMED_EMAIL_ENDPOINT = '' #:
    USER_UNAUTHENTICATED_ENDPOINT = 'user.login' #:
    USER_UNAUTHORIZED_ENDPOINT = '' #:
