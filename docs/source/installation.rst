============
Installation
============

Requirements
------------
Flask-User requires the following Python packages:

- Python |supported_python_versions_or|
- Flask 0.10+
- Flask-Login 0.3+
- Flask-Mail 0.9+ or Flask-Sendmail
- Flask-WTF 0.9+
- passlib 1.6+
- pycrypto 2.6+

Optionally, for fast bcrypt encryption:

- py-bcript 0.4+

For SQLAlchemy applications:

- Flask-SQLAlchemy 1.0+
- A DBAPI driver (such as mysql-python for MySQL or psycopg2 for PostgreSQL)

Optionally, for Event Notification:

- blinker 1.3+

Optionally, for Internationalization:

- Flask-Babel 0.9+
- speaklater 1.3+


Installation Instructions
-------------------------

We recommend making use of virtualenv and virtualenvwrapper::

    mkvirtualenv my_env
    workon my_env

Install Flask-User using pip::

    workon my_env
    pip install flask-user


