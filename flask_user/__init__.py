""" Flask-User is a customizable user account management extension for Flask.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from .user_mixin import UserMixin
from .user_manager import UserManager

# Export Flask-Login's current user
from flask_login import current_user            # pass through Flask-Login's current_user

# Export login_required, roles_required, roles_accepted, confirm_email_required
from .decorators import *

# Export Flask-User signals
from .signals import *
