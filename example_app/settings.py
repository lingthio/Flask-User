# Flask settings
DEBUG = True
SECRET_KEY = 'super-secret'

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///example_app.db'

# ** Flask-User settings **

# # Features
# USER_ENABLE_CHANGE_PASSWORD     = True
# USER_ENABLE_CHANGE_USERNAME     = True
# USER_ENABLE_FORGOT_PASSWORD     = True
# USER_ENABLE_REGISTRATION        = True
# USER_REQUIRE_EMAIL_CONFIRMATION = True
# USER_REQUIRE_INVITATION         = False
#
# # Settings
# USER_CONFIRM_EMAIL_EXPIRATION   = 2*24*3600  # 2 days
# USER_LOGIN_WITH_USERNAME        = False
# USER_REGISTER_WITH_EMAIL        = True
# USER_RESET_PASSWORD_EXPIRATION  = 2*24*3600  # 2 days
# USER_RETYPE_PASSWORD            = True
#
# # URLs
# USER_CHANGE_PASSWORD_URL        = '/user/change-password'
# USER_CHANGE_USERNAME_URL        = '/user/change-username'
# USER_CONFIRM_EMAIL_URL          = '/user/confirm-email'
# USER_FORGOT_PASSWORD_URL        = '/user/forgot-password'
# USER_LOGIN_URL                  = '/user/login'
# USER_LOGOUT_URL                 = '/user/logout'
# USER_REGISTER_URL               = '/user/register'
#
# # Templates
# USER_CHANGE_USERNAME_TEMPLATE   = 'flask_user/change_username.html'
# USER_CHANGE_PASSWORD_TEMPLATE   = 'flask_user/change_password.html'
# USER_FORGOT_PASSWORD_TEMPLATE   = 'flask_user/forgot_password.html'
# USER_LOGIN_TEMPLATE             = 'flask_user/login.html'
# USER_REGISTER_TEMPLATE          = 'flask_user/register.html'
# USER_RESEND_CONFIRMATION_EMAIL_TEMPLATE = 'flask_user/resend_confirmation_email.html'
# USER_RESET_PASSWORD_TEMPLATE    = 'flask_user/reset_password.html'

