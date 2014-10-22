============
Installation
============

We recommend making use of virtualenv and virtualenvwrapper::

    mkvirtualenv my_env
    workon my_env

Installation Instructions
-------------------------

After setting up virtualenv, installation is as easy as::

    workon my_env
    pip install flask-user

Requirements
------------
- Python 2.6, 2.7, 3.3 or 3.4
- Flask 0.10+
- Flask-Login 0.2+
- Flask-Mail 0.9+ or Flask-Sendmail
- Flask-WTF 0.9+
- passlib 1.6+
- pycrypto 2.6+
- py-bcript 0.4+        # Recommended for speed, and only if bcrypt is used to hash passwords

When using the included SQLAlchemyAdapter, Flask-User requires:

- Flask-SQLAlchemy 1.0+ (with a driver such as MySQL-Python or PyMySQL)

Optional requirements for Event Notification:

- blinker 1.3+

Optional requirements for Internationalization:

- Flask-Babel 0.9+
- speaklater 1.3+

Up Next
-------
:doc:`basic_app`

