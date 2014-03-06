============
Installation
============

We recommend making use of virtualenv and virtualenvwrapper::

    mkvirtualenv my_env
    workon my_env

Installation Instructions
-------------------------

After setting up virtualenv, installation is as easy as::

    pip install flask-user

Requirements
------------
- Python 2.6, 2.7 or 3.3
- crypto, passlib and py-bcript
- Flask
- Flask-Babel
- Flask-Login
- Flask-Mail
- Flask-WTF

Optional requirements for SQLAlchemyAdapter:

- SQL-Python
- Flask-SQLAlchemy

Optional requirements for Event Notification:

- blinker

