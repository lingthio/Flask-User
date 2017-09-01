""" This file implements utility functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from flask import current_app
from flask_login import current_user


# Return True for logged in users.
# Return False otherwise
def user_is_authenticated(user):
    # Flask-Login prior to v0.3 uses a method.
    # Flask-Login v0.3+ uses an attribute.
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


# Return True if ENABLE_EMAIL and ENABLE_CONFIRM_EMAIL and email has been confirmed.
# Return False otherwise
def user_has_confirmed_email(user):
    user_manager = current_app.user_manager
    if not user_manager.USER_ENABLE_EMAIL: return True
    if not user_manager.USER_ENABLE_CONFIRM_EMAIL: return True

    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Handle multiple email_templates per user: Find at least one confirmed email
    if user_manager.UserEmailClass:
        has_confirmed_email = False
        user_emails = db_adapter.find_objects(user_manager.UserEmailClass, user_id=user.id)
        for user_email in user_emails:
            if user_email.email_confirmed_at:
                has_confirmed_email = True
                break

    # Handle single email per user
    else:
        has_confirmed_email = True if user.email_confirmed_at else False

    return has_confirmed_email
