"""This module defines UserManager settings and their defaults.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

# This class mixes into the UserManager class.
# Mixins allow for maintaining code and docs across several files.
class UserManager__Settings(object):
    """Flask-User settings and their defaults.

    .. This hack shows a header above the _next_ section
    .. code-block:: none

        Feature settings
    """


    #: | Allow users to login and register with an email address
    USER_ENABLE_EMAIL = True

    #: | Allow users to associate multiple email addresses with one user account.
    #: | Depends on USER_ENABLE_EMAIL=True
    USER_ENABLE_MULTIPLE_EMAILS = False

    #: | Allow users to login and register with a username
    USER_ENABLE_USERNAME = True

    #: | Allow users to change their username.
    #: | Depends on USER_ENABLE_USERNAME=True.
    USER_ENABLE_CHANGE_USERNAME = True

    #: | Allow users to change their password.
    USER_ENABLE_CHANGE_PASSWORD = True

    #: | Enable email confirmation emails to be sent.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_CONFIRM_EMAIL = True

    #: | Allow users to reset their passwords.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_FORGOT_PASSWORD = True

    #: | Allow unregistered users to be invited.
    USER_ENABLE_INVITE_USER = False

    #: | Allow unregistered users to register.
    USER_ENABLE_REGISTER = True

    #: | Remember user sessions across browser restarts.
    #:
    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Generic settings and their defaults
    USER_ENABLE_REMEMBER_ME = True

    USER_ENABLE_AUTH0 = False


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

    #: | Sender's email address, used by the EmailAdapters.
    #: | Required for sending emails.
    #: | Derived from MAIL_DEFAULT_SENDER or DEFAULT_MAIL_SENDER when specified.
    USER_EMAIL_SENDER_EMAIL = ''

    #: | Sender's name, user by the EmailAdapters.
    #: | Optional. Defaults to USER_APP_NAME setting.
    USER_EMAIL_SENDER_NAME = ''

    #: | The way Flask-User handles case insensitive searches.
    #: | Valid options are:
    #: | - 'ifind' (default): Use the case insensitive ifind_first_object()
    #: | - 'nocase_collation': username and email fields must be configured
    #: |     with an case insensitve collation (collation='NOCASE' in SQLAlchemy)
    #: |     so that a regular find_first_object() can be performed.
    USER_IFIND_MODE = 'ifind'

    #: | Send notification email after a password change.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_PASSWORD_CHANGED_EMAIL = True

    #: | Send notification email after a registration.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_REGISTERED_EMAIL = True

    #: | Send notification email after a username change.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_USERNAME_CHANGED_EMAIL = True

    #: | Only invited users may register.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_REQUIRE_INVITATION = False

    #: | Ensure that users can login only with a confirmed email address.
    #: | Depends on USER_ENABLE_EMAIL=True.
    #:
    #: This setting works in tandem with the ``@allow_unconfirmed_emails``
    #: view decorator to allow users without confirmed email addresses
    #: to access certain views.
    #:
    #: .. caution::
    #:
    #:     | Use ``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL=True`` and
    #:         ``@allow_unconfirmed_email`` with caution,
    #:         as they relax security requirements.
    #:     | Make sure that decorated views **never call other views directly**.
    #:         Allways se ``redirect()`` to ensure proper view protection.

    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False

    #: | Require users to retype their password.
    #: | Affects registration, change password and reset password forms.
    USER_REQUIRE_RETYPE_PASSWORD = True

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

    #: | User session token expiration in seconds.
    #: | Default is 1 hour (1*3600 seconds).
    #:
    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Password hash settings
    USER_USER_SESSION_EXPIRATION = 1*3600

    #: | List of accepted password hashes.
    #: | See `Passlib CryptContext docs on Constructor Keyword ``'schemes'`` <http://passlib.readthedocs.io/en/stable/lib/passlib.context.html?highlight=cryptcontext#constructor-keywords>`_
    #: | Example: ``['bcrypt', 'argon2']``
    #: |   Creates new hashes with 'bcrypt' and verifies existing hashes with 'bcrypt' and 'argon2'.
    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['bcrypt']

    #: | Dictionary of CryptContext keywords and hash options.
    #: | See `Passlib CryptContext docs on Constructor Keywords <http://passlib.readthedocs.io/en/stable/lib/passlib.context.html?highlight=cryptcontext#constructor-keywords>`_
    #: | and `Passlib CryptContext docs on Algorithm Options <http://passlib.readthedocs.io/en/stable/lib/passlib.context.html?highlight=cryptcontext#algorithm-options>`_
    #: | Example: ``dict(bcrypt__rounds=12, argon2__time_cost=2, argon2__memory_cost=512)``
    #:
    #: .. This hack shows a header above the _next_ section
    #:     URL settings
    USER_PASSLIB_CRYPTCONTEXT_KEYWORDS = dict()

    USER_CHANGE_PASSWORD_URL = '/user/change-password' #:
    USER_CHANGE_USERNAME_URL = '/user/change-username' #:
    USER_CONFIRM_EMAIL_URL = '/user/confirm-email/<token>' #:
    USER_EDIT_USER_PROFILE_URL = '/user/edit_user_profile' #:
    USER_EMAIL_ACTION_URL = '/user/email/<id>/<action>' #:
    USER_FORGOT_PASSWORD_URL = '/user/forgot-password' #:
    USER_INVITE_USER_URL = '/user/invite' #:
    USER_LOGIN_URL = '/user/sign-in' #:
    USER_LOGOUT_URL = '/user/sign-out' #:
    USER_MANAGE_EMAILS_URL = '/user/manage-emails' #:
    USER_REGISTER_URL = '/user/register' #:
    USER_RESEND_EMAIL_CONFIRMATION_URL = '/user/resend-email-confirmation' #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Template file settings
    USER_RESET_PASSWORD_URL = '/user/reset-password/<token>'

    USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html' #:
    USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html' #:
    USER_EDIT_USER_PROFILE_TEMPLATE = 'flask_user/edit_user_profile.html' #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'flask_user/forgot_password.html' #:
    USER_INVITE_USER_TEMPLATE = 'flask_user/invite_user.html' #:
    USER_LOGIN_TEMPLATE = 'flask_user/login.html' #:
    USER_LOGIN_AUTH0_TEMPLATE = 'flask_user/login_auth0.html' #:
    USER_MANAGE_EMAILS_TEMPLATE = 'flask_user/manage_emails.html' #:
    USER_REGISTER_TEMPLATE = 'flask_user/register.html' #:
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'flask_user/resend_confirm_email.html' #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Email template file settings
    USER_RESET_PASSWORD_TEMPLATE = 'flask_user/reset_password.html'

    USER_CONFIRM_EMAIL_TEMPLATE = 'flask_user/emails/confirm_email' #:
    USER_INVITE_USER_EMAIL_TEMPLATE = 'flask_user/emails/invite_user' #:
    USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/password_changed' #:
    USER_REGISTERED_EMAIL_TEMPLATE = 'flask_user/emails/registered' #:
    USER_RESET_PASSWORD_EMAIL_TEMPLATE = 'flask_user/emails/reset_password' #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     FLask endpoint settings
    USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'flask_user/emails/username_changed'

    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_CHANGE_USERNAME_ENDPOINT = '' #:
    USER_AFTER_CONFIRM_ENDPOINT = '' #:
    USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = '' #:
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_LOGIN_ENDPOINT = '' #:
    USER_AFTER_LOGOUT_ENDPOINT = '' #:
    USER_AFTER_REGISTER_ENDPOINT = '' #:
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = '' #:
    USER_AFTER_RESET_PASSWORD_ENDPOINT = '' #:
    USER_AFTER_INVITE_ENDPOINT = '' #:
    USER_UNAUTHENTICATED_ENDPOINT = 'user.login' #:
    USER_UNAUTHORIZED_ENDPOINT = '' #:
    # USER_UNCONFIRMED_EMAIL_ENDPOINT = '' #:
