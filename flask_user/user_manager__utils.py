"""This module implements UserManager utility methods.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

# Python version specific imports
from sys import version_info as py_version
is_py2 = (py_version[0] == 2)     #: Python 2.x?
if is_py2:
    from urlparse import urlsplit
else:
    from urllib.parse import urlsplit

from flask_login import current_user


# This class mixes into the UserManager class.
# Mixins allow for maintaining code and docs across several files.
class UserManager__Utils(object):
    """Flask-User utility methods."""

    # Flask-Login 0.2 uses functions while 0.3 uses properties
    def call_or_get(self, function_or_property):
        """| Calls ``function_or_property`` if it's a function.
        | Gets ``function_or_property`` otherwise.

        In Flask-Login 0.2 ``is_authenticated`` and ``is_active`` were
        implemented as functions, while in 0.3+ they are implemented as properties.

        Example::

            if self.call_or_get(current_user.is_authenticated):
                pass
        """
        return function_or_property() if callable(function_or_property) else function_or_property

    def email_is_available(self, new_email):
        """Check if ``new_email`` is available.

        | Returns True if ``new_email`` does not exist or belongs to the current user.
        | Return False otherwise.
        """

        user, user_email = self.find_user_by_email(new_email)
        return (user == None)

    def find_user_by_username(self, username):
        """Retrieve a User by username (case insensitively)."""
        return self.db_adapter.ifind_first_object(self.UserClass, username=username)

    def find_user_by_email(self, email):
        """Retrieve a User by email."""
        if self.UserEmailClass:
            user_email = self.db_adapter.ifind_first_object(self.UserEmailClass, email=email)
            user = user_email.user if user_email else None
        else:
            user_email = None
            user = self.db_adapter.ifind_first_object(self.UserClass, email=email)

        return (user, user_email)

    def generate_token(self, *args):
        """Convenience method that calls self.token_manager.generate_token(\*args)."""
        return self.token_manager.generate_token(*args)

    def get_language_codes(self):
        """Returns the language codes of available Flask-User translations.

        Example:
            ``['de', 'en', 'es', 'fa', 'fi', 'fr', 'it', 'nl', 'ru', 'sv', 'tr', 'zh']``

        """
        from .translation_utils import get_language_codes
        return get_language_codes()

    def get_primary_user_email(self, user):
        """Retrieve the email from User object or the primary UserEmail object (if multiple emails
        per user are enabled)."""
        db_adapter = self.db_adapter
        if self.UserEmailClass:
            user_email = db_adapter.find_first_object(self.UserEmailClass,
                                                      user_id=user.id,
                                                      is_primary=True)
            return user_email
        else:
            return user

    def get_user_by_id(self, user_id):
        """Retrieve a User object by ID."""
        return self.db_adapter.get_object(self.UserClass, user_id)

    def get_user_email_by_id(self, user_email_id):
        """Retrieve a UserEmail object by ID."""
        return self.db_adapter.get_object(self.UserEmailClass, user_email_id)

    def hash_password(self, password):
        """Convenience method that calls self.password_manager.hash_password(password)."""
        return self.password_manager.hash_password(password)

    def make_safe_url(self, url):
        """Makes a URL safe by removing optional hostname and port.

        Example:

            | ``make_safe_url('https://hostname:80/path1/path2?q1=v1&q2=v2#fragment')``
            | returns ``'/path1/path2?q1=v1&q2=v2#fragment'``

        Override this method if you need to allow a list of safe hostnames.
        """

        # Split the URL into scheme, hostname, port, path, query and fragment
        parts = urlsplit(url)
        # Rebuild a safe URL with only the path, query and fragment parts
        safe_url = parts.path + parts.query + parts.fragment
        return safe_url

    def prepare_domain_translations(self):
        """Set domain_translations for current request context."""
        from .translation_utils import domain_translations
        if domain_translations:
            domain_translations.as_default()

    def send_email_message(self, recipient, subject, html_message, text_message):
        """Convenience method that calls self.email_mailer.send_email_message(password, password_hash).
        """
        return self.email_mailer.send_email_message(
            recipient=recipient, subject=subject,
            html_message=html_message, text_message=text_message)

    # Return True if ENABLE_EMAIL and ENABLE_CONFIRM_EMAIL and email has been confirmed.
    # Return False otherwise
    def user_has_confirmed_email(self, user):
        """| Return True if user has a confirmed email.
        | Return False otherwise."""
        if not self.USER_ENABLE_EMAIL: return True
        if not self.USER_ENABLE_CONFIRM_EMAIL: return True

        db_adapter = self.db_adapter

        # Handle multiple email_templates per user: Find at least one confirmed email
        if self.UserEmailClass:
            has_confirmed_email = False
            user_emails = db_adapter.find_objects(self.UserEmailClass, user_id=user.id)
            for user_email in user_emails:
                if user_email.email_confirmed_at:
                    has_confirmed_email = True
                    break

        # Handle single email per user
        else:
            has_confirmed_email = True if user.email_confirmed_at else False

        return has_confirmed_email

    def username_is_available(self, new_username):
        """Check if ``new_username`` is still available.

        | Returns True if ``new_username`` does not exist or belongs to the current user.
        | Return False otherwise.
        """

        # Return True if new_username equals current user's username
        if self.call_or_get(current_user.is_authenticated):
            if new_username == current_user.username:
                return True

        # Return True if new_username does not exist,
        # Return False otherwise.
        return self.find_user_by_username(new_username) == None

    def verify_password(self, password, password_hash):
        """Convenience method that calls self.password_manager.verify_password(password, password_hash).
        """
        # Handle deprecated v0.6 (password, user) params
        if isinstance(password_hash, self.UserClass):
            print(
                'Deprecation warning: verify_password(password, user) has been changed'\
                ' to: verify_password(password, password_hash). The user param will be deprecated.'\
                ' Please change your call with verify_password(password, user) into'\
                ' a call with verify_password(password, user.password)'
                ' as soon as possible.')
            password_hash = password_hash.password   # effectively user.password

        return self.password_manager.verify_password(password, password_hash)

    def verify_token(self, token, expiration_in_seconds):
        """Convenience method that calls self.token_manager.verify_token(token, expiration_in_seconds)."""
        return self.token_manager.verify_token(token, expiration_in_seconds)
