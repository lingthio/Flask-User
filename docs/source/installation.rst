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
- Python 2.6, 2.7, 3.3 or 3.4
- crypto, passlib and py-bcript
- Flask 0.10+
- Flask-Login 0.2+
- Flask-Mail or Flask-Sendmail
- Flask-WTF

Optional requirements for Internationalization:

- Flask-Babel

Optional requirements for SQLAlchemyAdapter:

- SQL-Python
- Flask-SQLAlchemy

Optional requirements for Event Notification:

- blinker

