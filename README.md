Flask-User
==========

Customizable user management for Flask (Register, Confirm, Forgot password, Login, etc.)

Status
------
This package is in active development (Feb 2014) but not yet ready for production.
We believe in early feedback, so we are publishing a few features early
while developing the remaining feature set.

__Completed Features__

- Register (sign up)
- Login (Sign in) with email or username
- Logout (Sign out)
- Change password
- Change username
- Session management through Flask-Login
- Password encryption through passlib and py-bcript
- Internationalization through Flask-Babel

__Planned Features__

- Confirm email
- Forgot password (Reset password)
- Multiple emails per user
- Registration by invitation only

__Philosophy__

- Reliable (Automated tests currently cover 99% of the code)
- Simple to use
- Easy to configure (by changing files)
- Easy to customize (by adding code)
- Model agnostic (specify your own User model)
- Database abstraction (SQLAlchemyAdapter provided)
- Extensible (See Flask-User-Roles for role based authorization)


Reliable
--------
```
> coverage report -m
Name                                              Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------
flask_user/__init__                                  97      0   100%   
flask_user/forms                                    123      0   100%   
flask_user/views                                     57      4    93%   53, 69, 91, 114
-------------------------------------------------------------------------------
TOTAL                                               277      4    99%   
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
USER_FEATURE_REGISTER = True
   
# Config
USER_REGISTER_WITH_RETYPE_PASSWORD = True
USER_CHANGE_PASSWORD_WITH_RETYPE_PASSWORD = True
USER_LOGIN_WITH_USERNAME = False

# URLs
USER_REGISTER_URL = '/user/register'
USER_LOGIN_URL = '/user/login'
USER_LOGOUT_URL = '/user/logout'
USER_CHANGE_USERNAME_URL = '/user/change-username'
USER_CHANGE_PASSWORD_URL = '/user/change-password'
    
# Templates
USER_REGISTER_TEMPLATE = 'flask_user/register.html'
USER_LOGIN_TEMPLATE = 'flask_user/login.html
USER_CHANGE_USERNAME_TEMPLATE = 'flask_user/change-username.html
USER_CHANGE_PASSWORD_TEMPLATE = 'flask_user/change-password.html
    
# Flash messages
USER_FLASH_SIGNED_IN = 'You have signed in successfully.'
USER_FLASH_SIGNED_OUT = 'You have signed out successfully.'
USER_FLASH_USERNAME_CHANGED = 'Username has been changed successfully.'
USER_FLASH_PASSWORD_CHANGED = 'Password has been changed successfully.'
```

These settings must be set before calling `user_manager.init_app(app)`.

In the Flask-User Example App, you can place them in example_app/settings.py.


Customize
---------

The available customizations with their defaults are listed below:

```
    # View functions
    user_manager.login_view_function = flask_user.views.login
    user_manager.logout_view_function = flask_user.views.logout
    user_manager.register_view_function = flask_user.views.register

    # Forms
    user_manager.login_form = = flask_user.forms.LoginForm
    user_manager.register_form = flask_user.forms.RegisterForm
    
    # Validators
    user_manager.password_validator.flask_user.forms.forms.password_validator

    # Encryptions
    user_manager.crypt_context = CryptContext(schemes=['bcrypt', 'sha512_crypt', 'pbkdf2_sha512'], default='bcrypt')
```

They can be set in between `user_manager=UserManager()` and `user_manager.init_app(app)` like so:

```
    ...

    # Choose Database adapter
    db_adapter = flask_user.SQLAlchemyAdapter(db, User)
    
    # Initialize Flask-User
    user_manager = flask_user.UserManager(db_adapter)

    # Configure Flask-User
    app.config['USER_LOGIN_TEMPLATE'] = 'my_app/my_login_form.html'

    # Customize Flask-User
    user_manager.login_form = forms.MyLoginForm

    # Bind Flask-User to app
    user_manager.init_app(app)
    
    ...
```

Documentation
-------------

TBD
    
Contact
-------
Ling Thio - ling.thio@gmail.com
