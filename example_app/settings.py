# Flask settings
DEBUG = True
SECRET_KEY = 'super-secret'

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///example_app.db'

# ** Flask-User settings **

# # Features
# USER_FEATURE_REGISTER = True
# USER_FEATURE_CHANGE_USERNAME = True
# USER_FEATURE_CHANGE_PASSWORD = True

# # Config
# USER_REGISTER_WITH_RETYPE_PASSWORD = True
# USER_LOGIN_WITH_USERNAME = False
# USER_LOGIN_WITH_EMAIL = True
# USER_CHANGE_PASSWORD_WITH_RETYPE_PASSWORD = True

# # URLs
# USER_REGISTER_URL = '/user/register'
# USER_LOGIN_URL = '/user/login'
# USER_LOGOUT_URL = '/user/logout'
# USER_CHANGE_USERNAME_URL = '/user/change-username'
# USER_CHANGE_PASSWORD_URL = '/user/change-password'

# # Templates
# USER_REGISTER_TEMPLATE = 'flask_user/register.html'
# USER_LOGIN_TEMPLATE = 'flask_user/login.html'
# USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change_username.html'
# USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change_password.html'

# # Flash messages
# USER_FLASH_SIGNED_IN = 'You have signed in successfully.'
# USER_FLASH_SIGNED_OUT = 'You have signed out successfully.'
# USER_USERNAME_CHANGED = 'Your username has been changed successfully.'
# USER_PASSWORD_CHANGED = 'Your password has been changed successfully.'
