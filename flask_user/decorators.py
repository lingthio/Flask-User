""" This file implements Flask-User decorators: @login_required, @confirm_email_required and @roles_required.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from functools import wraps
from flask import current_app
from flask_login import current_user
from .access import is_authenticated, is_confirmed_email


# Here to not break backward compatibility
def _call_or_get(function_or_property):
    return function_or_property() if callable(function_or_property) else function_or_property


def login_required(func):
    """ This decorator ensures that the current user is logged in before calling the actual view.
        Calls the unauthorized_view_function() when the user is not logged in."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if not is_authenticated():
            # Redirect to unauthenticated page
            return current_app.user_manager.unauthenticated_view_function()

        # Call the actual view
        return func(*args, **kwargs)
    return decorated_view


def roles_accepted(*role_names):
    """ This decorator ensures that the current user one of the specified roles.
        Calls the unauthorized_view_function() when requirements fail.
        See also: UserMixin.has_role()
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # User must be logged
            if not is_authenticated():
                # Redirect to the unauthenticated page
                return current_app.user_manager.unauthenticated_view_function()

            # User must have the required roles
            if not current_user.has_role(*role_names):
                # Redirect to the unauthorized page
                return current_app.user_manager.unauthorized_view_function()

            # Call the actual view
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def roles_required(*role_names):
    """ This decorator ensures that the current user has all of the specified roles.
        Calls the unauthorized_view_function() when requirements fail.
        See also: UserMixin.has_roles()
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # User must be logged
            if not is_authenticated():
                # Redirect to the unauthenticated page
                return current_app.user_manager.unauthenticated_view_function()

            # User must have the required roles
            if not current_user.has_roles(*role_names):
                # Redirect to the unauthorized page
                return current_app.user_manager.unauthorized_view_function()

            # Call the actual view
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def confirm_email_required(func):
    """ This decorator ensures that the current user is logged in and has confirmed their email.
        Calls the unauthorized_view_function() when the user is not logged in."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if is_authenticated():
            user_manager = current_app.user_manager
            # If confirm email has been enabled, user must have at least one confirmed email
            if is_confirmed_email():
                return func(*args, **kwargs)

        return current_app.user_manager.unconfirmed_email_view_function()

    return decorated_view
