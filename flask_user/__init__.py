__title__       = 'Flask-User'
__description__ = 'Customizable User Authentication,User Management, and more.'
__version__     = '0.9.0'
__url__         = 'https://github.com/lingthio/Flask-User'
__author__      = 'Ling Thio'
__author_email__= 'ling.thio@gmail.com'
__maintainer__  = 'Ling Thio'
__license__     = 'MIT'
__copyright__   = '(c) 2013 Ling Thio'

# Define Flask-User Exceptions early on
class ConfigError(Exception):
    pass

class EmailError(Exception):
    pass


from .user_mixin import UserMixin
from .user_manager import UserManager
from .email_manager import EmailManager
from .password_manager import PasswordManager
from .token_manager import TokenManager


# Export Flask-Login's current user
from flask_login import current_user    # pass through Flask-Login's current_user

# Export login_required, roles_required, confirmed_email_required
from .decorators import *

# Export Flask-User signals
from .signals import *
