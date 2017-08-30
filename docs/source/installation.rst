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

Because Flask-User defaults to sending emails with Flask-Mail and managing databases with Flask-SQLAlchemy,
Flask-User will install these packages by default.

If you configure Flask-User to use a different mailer or a different
object-database mapper, you may uninstall unused packages::

    # Optionally uninstall unused packages
    pip uninstall Flask-Mail
    pip uninstall Flask-SQLAlchemy

