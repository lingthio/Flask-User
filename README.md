Flask-User
==========

Customizable user management for Flask (Register, Confirm, Forgot password, Login, etc.)

Status
------
This package is in active development (Feb 2014) but not yet ready for production.
We believe in early feedback, so we are publishing a few features early
while developing the remaining feature set.

[![Build Status](https://travis-ci.org/solidbuilds/flask-user.png?branch=master)](https://travis-ci.org/solidbuilds/flask-user)

__Completed Features__

- Register (sign up)
- Confirm email
- Login (Sign in) with email or username
- Logout (Sign out)
- Change username
- Change password
- Forgot password (Reset password)
- Session management through Flask-Login
- Password encryption through passlib and py-bcript
- Internationalization through Flask-Babel

__Planned Features__

- Multiple emails per user
- Registration by invitation only

Philosophy
----------

- Reliable (Automated test coverage of over 95%)
- Simple to use
- Easy to configure (by changing files)
- Easy to customize (by adding code)
- Model agnostic (specify your own User model)
- Database abstraction (SQLAlchemyAdapter provided)
- Extensible (See Flask-User-Roles for role based authorization)


Reliable
--------

Our goal is to have our automated tests cover over 95% of our code base.  
We're currently at 97%.

```
> coverage report
Name                                                            Stmts   Miss  Cover
-----------------------------------------------------------------------------------
flask_user/__init__                                                93      0   100%
flask_user/db_interfaces                                           51      0   100%
flask_user/emails                                                  28      0   100%
flask_user/forms                                                  149      3    98%
flask_user/passwords                                                4      0   100%
flask_user/tokens                                                  37      0   100%
flask_user/views                                                  128     13    90%
-----------------------------------------------------------------------------------
TOTAL                                                             490     16    97%
```

Simple to use
-------------

```
def create_app():
    app = Flask(__name__)                                   # Initialize Flask App
    
    db  = SQLAlchemy(app)                                   # Initialize and bind Flask-SQLAlchemy
    from my_app.models import User                          # Import your User model
    
    db_adapter   = flask_user.SQLAlchemyAdapter(db, User)   # Choose a database Adapter
    user_manager = flask_user.UserManager(db_adapter, app)  # Initialize and bind Flask-User
    
    return app
```


Easy to Configure (by changing files)
-------------------------------------

- URLs
- Templates
- Flash messages
- Validation errors
- Email messages (subject, HTML message and Text message)

Easy to Customize (by adding code)
----------------------------------

- Forms
- View functions
- Validators
- Password encryption

Requirements
------------

- Python 2.7 (May work on other versions - please let us know)
- Flask 0.10 (May work on other versions - please let us know)
- Flask-Login
- Flask-Babel
- Flask-WTF and Jinja2
- passlib and py-bcript

Install Flask-User
------------------

The goal is to create a python package that can be installed 'pip install flask-user'.  

This is still work in progress.

Install Flask-User Example App
------------------------------

```
mkvirtualenv flask_user
workon flask_user
mkdir -p ~/dev
git clone git@github.com:solidbuilds/flask-user.git ~/dev/flask_user
cd ~/dev/flask_user
pip install -r requirements.txt
fab runserver
# point your browser to http://localhost:5001
```

Configure
---------

The available settings with their defaults are listed below:

```
# Features
USER_ENABLE_CHANGE_PASSWORD     = True
USER_ENABLE_CHANGE_USERNAME     = True
USER_ENABLE_FORGOT_PASSWORD     = True
USER_ENABLE_REGISTRATION        = True
USER_REQUIRE_EMAIL_CONFIRMATION = True
USER_REQUIRE_INVITATION         = False

# Settings
USER_CONFIRM_EMAIL_EXPIRATION   = 2*24*3600  # 2 days
USER_LOGIN_WITH_USERNAME        = False
USER_REGISTER_WITH_EMAIL        = True
USER_RESET_PASSWORD_EXPIRATION  = 2*24*3600  # 2 days
USER_RETYPE_PASSWORD            = True

# URLs
USER_CHANGE_PASSWORD_URL        = '/user/change-password'
USER_CHANGE_USERNAME_URL        = '/user/change-username'
USER_CONFIRM_EMAIL_URL          = '/user/confirm-email'
USER_FORGOT_PASSWORD_URL        = '/user/forgot-password'
USER_LOGIN_URL                  = '/user/login'
USER_LOGOUT_URL                 = '/user/logout'
USER_REGISTER_URL               = '/user/register'

# Templates
USER_CHANGE_USERNAME_TEMPLATE   = 'flask_user/change_username.html'
USER_CHANGE_PASSWORD_TEMPLATE   = 'flask_user/change_password.html'
USER_FORGOT_PASSWORD_TEMPLATE   = 'flask_user/forgot_password.html'
USER_LOGIN_TEMPLATE             = 'flask_user/login.html'
USER_REGISTER_TEMPLATE          = 'flask_user/register.html'
USER_RESEND_CONFIRMATION_EMAIL_TEMPLATE = 'flask_user/resend_confirmation_email.html'
USER_RESET_PASSWORD_TEMPLATE    = 'flask_user/reset_password.html'
```

These settings must be set before calling `user_manager.init_app(app)`.

In the Flask-User Example App, you can place them in example_app/settings.py.


Customize
---------

The available customizations are listed below:

```
# View functions
user_manager.change_password_view_function
user_manager.change_username_view_function
user_manager.confirm_email_view_function
user_manager.forgot_password_view_function
user_manager.login_view_function
user_manager.logout_view_function
user_manager.register_view_function
user_manager.resend_confirmation_email_view_function
user_manager.reset_password_view_function

# Forms
user_manager.change_password_form
user_manager.change_username_form
user_manager.forgot_password_form
user_manager.login_form
user_manager.register_form
user_manager.reset_password_form

# Validators
user_manager.password_validator  # at least 6 chars, 1 upper case letter, 1 lower case letter, 1 digit
user_manager.username_validator  # at least 3 alphanumeric characters

# Encryptions
user_manager.crypt_context = CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')
```

They can be set in between `user_manager=UserManager()` and `user_manager.init_app(app)` like so:

```
...

db_adapter = flask_user.SQLAlchemyAdapter(db, User)  # Choose Database adapter
user_manager = flask_user.UserManager(db_adapter)    # Initialize Flask-User
user_manager.login_form = forms.MyLoginForm          # Customize Flask-User
user_manager.init_app(app)                           # Bind Flask-User to app

...
```

Documentation
-------------

TBD
    
Contact
-------
Ling Thio - ling.thio@gmail.com
