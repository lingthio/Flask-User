""" This file implements Flask-User decorators: @login_required, @confirmed_email_required and @roles_required.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from functools import wraps
from flask import current_app
from flask_login import current_user
from .utils import user_is_authenticated, user_has_confirmed_email


def login_required(func):
    """ This decorator ensures that the current user is logged in before calling the actual view.
        Calls the unauthorized_view() when the user is not logged in."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if not user_is_authenticated(current_user):
            # Redirect to unauthenticated page
            return current_app.user_manager.unauthenticated_view()

        # Call the actual view
        return func(*args, **kwargs)
    return decorated_view


def roles_accepted(*role_names):
    """ This decorator ensures that the current user one of the specified roles.
        Calls the unauthorized_view() when requirements fail.
        See also: UserMixin.has_role()
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # User must be logged
            if not user_is_authenticated(current_user):
                # Redirect to the unauthenticated page
                return current_app.user_manager.unauthenticated_view()

            # User must have the required roles
            if not current_user.has_role(*role_names):
                # Redirect to the unauthorized page
                return current_app.user_manager.unauthorized_view()

            # Call the actual view
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def roles_required(*role_names):
    """ This decorator ensures that the current user has all of the specified roles.
        Calls the unauthorized_view() when requirements fail.
        See also: UserMixin.has_roles()
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # User must be logged
            if not user_is_authenticated(current_user):
                # Redirect to the unauthenticated page
                return current_app.user_manager.unauthenticated_view()

            # User must have the required roles
            if not current_user.has_roles(*role_names):
                # Redirect to the unauthorized page
                return current_app.user_manager.unauthorized_view()

            # Call the actual view
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


def confirmed_email_required(func):
    """ This decorator ensures that the current user is logged in and has confirmed their email.
        Calls the unauthorized_view() when the user is not logged in."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if user_is_authenticated(current_user):
            user_manager = current_app.user_manager
            # If confirm email has been enabled, user must have at least one confirmed email
            if user_has_confirmed_email(current_user):
                return func(*args, **kwargs)

        return current_app.user_manager.unconfirmed_email_view()

    return decorated_view
