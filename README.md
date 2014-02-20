Flask-User
==========

Customizable user registration for Flask

Status
------
This package is in active development (Feb 2014) but not yet ready for production.
We believe in early feedback, so we are publishing a few features early
while developing the remaining feature set.

Current Features
----------------

- Well tested (97% test coverage)
- Register (sign up)
- Login (Sign in) with email or username
- Logout (Sign out)
- Configurable (by changing settings)
- Customizable (by adding code)
- Session management through Flask-Login
- Password encryption through passlib and py-bcript
- Internationalization through Flask-Babel
- Model agnostic (specify your own User model)
- Database abstraction (SQLAlchemyAdapter provided)

Planned Features
----------------

- Confirm email
- Forgot password (Reset password)
- Change password
- Change username
- Multiple emails per user
- Registration by invitation only
- Extensible: Flask-User-Roles for role based authorization

Configurable (by changing settings)
-----------------------------------

- URLs
- Templates
- Flash messages
- Validation errors

Customizable (by adding code)
-----------------------------

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
- Flask-WTF
- Jinja2
- WTForms
- passlib
- py-bcript (if bcyrpt encryption is used)

Install
-------

```
    mkvirtualenv flask_user
    workon flask_user
    mkdir -p ~/dev
    cd ~/dev
    git clone git@github.com:solidbuilds/flask-user.git flask_user
    cd flask_user
    pip install -r requirements.txt
    touch example_app/env_settings.py
    fab test
    fab runserver
    # point your browser to http://localhost:5001
```

Configure
---------

Configure by changing settings in example_app/settings.py.
Below are the available settings with their defaults

```
    # Features
    USER_FEATURE_REGISTER = True
   
    # Config
    USER_REGISTER_WITH_RETYPE_PASSWORD = False
    USER_LOGIN_WITH_USERNAME = False
    USER_LOGIN_WITH_EMAIL = True

    # URLs
    USER_REGISTER_URL = '/user/register'
    USER_LOGIN_URL = '/user/login'
    USER_LOGOUT_URL = '/user/logout'
    
    # Templates
    USER_REGISTER_TEMPLATE = 'flask_user/register.html'
    USER_LOGIN_TEMPLATE = 'flask_user/login.html
    
    # Flash messages
    USER_FLASH_SIGNED_IN = 'You have signed in successfully.'
    USER_FLASH_SIGNED_OUT = 'You have signed out successfully.'
```

Documentation
-------------

TBD
    
Contact
-------
Ling Thio - ling.thio@gmail.com
