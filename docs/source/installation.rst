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
- passlib 1.6+
- pycrypto 2.6+
- py-bcript 0.4+
- Flask 0.10+
- Flask-Login 0.2+
- Flask-Mail 0.9+ or Flask-Sendmail
- Flask-WTF 0.9+

Optional requirements for Internationalization:

- Flask-Babel 0.9+
- speaklater 1.3+

Optional requirements for SQLAlchemyAdapter:

- Flask-SQLAlchemy 1.0+ with MySQL-Python or PyMySQL

Optional requirements for Event Notification:

- blinker

