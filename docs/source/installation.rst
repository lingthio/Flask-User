============
Installation
============

We recommend making use of virtualenv, virtualenvwrapper and pip::

    # Create virtual enviroment
    mkvirtualenv my_app

    # Switch to virtual environment
    workon my_app

    # Install Flask-User
    pip install Flask-User

Optional uninstalls
-------------------
- FLask-User installs bcrypt for its default passlib hash of 'bcrypt'.
- Flask-User installs Flask-Mail for its default SMTPEmailAdapter.
- Flask-User installs Flask-SQLAlchemy for its default SQLDbAdapter.

If you configure/customize Flask-User away from their defaults, certain packages may be uninstalled::

    # Optionally uninstall unused packages
    pip uninstall bcrypt
    pip uninstall Flask-Mail
    pip uninstall Flask-SQLAlchemy

