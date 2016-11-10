""" This file implements Flask-User access' checkers: is_authenticated and is_confirmed_email.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from flask import current_app
from flask_login import current_user


def _call_or_get(function_or_property):
    return function_or_property() if callable(function_or_property) else function_or_property


def is_authenticated():
    # User must be authenticated
    return _call_or_get(current_user.is_authenticated)


def is_confirmed_email():
    user_manager = current_app.user_manager
    # If confirm email has been enabled, user must have at least one confirmed email
    return not user_manager.enable_email\
                    or not user_manager.enable_confirm_email\
                    or current_user.has_confirmed_email()
