============
Installation
============

We recommend making use of virtualenv and virtualenvwrapper::

    mkvirtualenv my_env
    workon my_env

Installation Instructions
-------------------------

After that, installation is as easy as::

    pip install flask-user


See also: :doc:`minimal-app`

Requirements
------------
- Python 3.3, 2.7 or 2.6
- Flask (includes itsdangerous)
- Flask-Babel
- Flask-Login
- Flask-Mail
- Flask-WTF
- crypto, passlib and py-bcript

Optional requirements needed for SQLAlchemyAdapter:

- SQL-Python
- Flask-SQLAlchemy

Optional requirements needed to register for signals

- blinker

