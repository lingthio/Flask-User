""" Flask-User is a customizable user account management extension for Flask.
"""

# Copyright: (c) 2013 by Ling Thio
# Author:    Ling Thio (ling.thio@gmail.com)
# License:   Simplified BSD License, see LICENSE.txt for more details."""

from .user_mixin import UserMixin
from .user_manager import UserManager
from .email_manager import EmailManager
from .password_manager import PasswordManager
from .token_manager import TokenManager

__version__ = '0.9.0'

# Export Flask-Login's current user
from flask_login import current_user            # pass through Flask-Login's current_user

# Export login_required, roles_required, roles_accepted, confirmed_email_required
from .decorators import *

# Export Flask-User signals
from .signals import *
