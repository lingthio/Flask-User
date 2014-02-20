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
- Packaging so it can be installed using `pip install flask-user'

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

Example code
------------

```
def create_app():
    app = Flask(__name__)                                   # Initialize Flask App
    db = SQLAlchemy(app)                                    # Initialize Flask-SQLAlchemy
    db_adapter = flask_user.SQLAlchemyAdapter(db, User)     # Choose a database Adapter
    user_manager = flask_user.UserManager(db_adapter)       # Initialize Flask-User
    user_manager.init_app(app)                              # Bind Flask-User to App
    return app
```

Requirements
------------

- Python 2.7 (May work on other versions - please let us know)
- Flask 0.10 (May work on other versions - please let us know)
- Flask-Login
- Flask-Babel
- Flask-WTF
- Jinja2
- passlib
- py-bcript (only if 'bcyrpt' encryption is used)

Install Flask-User
------------------

TBD. Hopefully 'pip install flask-user'

Install Flask-User Example App
------------------------------

```
mkvirtualenv flask_user
workon flask_user
mkdir -p ~/dev
git clone git@github.com:solidbuilds/flask-user.git ~/dev/flask_user
cd ~/dev/flask_user
pip install -r requirements.txt
touch example_app/env_settings.py
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
