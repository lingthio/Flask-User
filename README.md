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
- Forgot password (Reset password)
- Customizable (by adding code)
- Configurable (by changing settings)
- Session management through Flask-Login
- Password encryption through passlib and py-bcript
- Internationalization through Flask-Babel
- Model agnostic (specify your own User model)
- Database abstraction (SQLAlchemyAdapter provided)

Planned Features
----------------

- Confirm email
- Change password
- Change username
- Multiple emails per user
- Registration by invitation only
- Extensible: Flask-User-Roles for role based authorization

Customizable (by adding code)
-----------------------------

- Forms
- View functions
- Validators
- Password encryption

Configurable (by changing settings)
-----------------------------------

- Templates
- Validation errors
- Flash messages
- URLs

Install
-------

    mkvirtualenv flask_user
    workon flask_user
    mkdir -p ~/dev
    cd ~/dev
    git clone git@github.com:solidbuilds/flask-user.git flask_user
    cd flask_user
    pip install -r requirements.txt
    fab runserver
    # point your browser to http://localhost:5001

Configure
---------

Change the USER\_\* settings in example_app/settings.py  
Available settings can be seen in flask\_user/\_\_init\_\_.py for now.

Documentation
-------------

TBD
    
