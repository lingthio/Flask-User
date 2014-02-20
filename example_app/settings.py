# Flask settings
DEBUG = True
SECRET_KEY = 'super-secret'

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///example_app.db'

# ** Flask-User settings **

# Features
# USER_FEATURE_REGISTER = True

# Config
# USER_REGISTER_WITH_RETYPE_PASSWORD = False
# USER_LOGIN_WITH_USERNAME = False
# USER_LOGIN_WITH_EMAIL = True

# URLs
# USER_REGISTER_URL = '/user/register'
# USER_LOGIN_URL = '/user/login'
# USER_LOGOUT_URL = '/user/logout'

# Templates
# USER_REGISTER_TEMPLATE = 'flask_user/register.html'
# USER_LOGIN_TEMPLATE = 'flask_user/login.html

# Flash messages
# USER_FLASH_SIGNED_IN = 'You have signed in successfully.'
# USER_FLASH_SIGNED_OUT = 'You have signed out successfully.'