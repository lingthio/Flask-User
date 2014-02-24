=======
Install
=======

Requirements
------------
- Python 3.3, 2.7 or 2.6
- Flask (includes itsdangerous)
- Flask-Babel
- Flask-Login
- Flask-Mail (includes blinker)
- Flask-WTF
- crypto, passlib and py-bcript

Additional requirements when selecting the SQLAlchemyAdapter():

- SQL-Python
- Flask-SQLAlchemy

Install
-------

We recommend making use of virtualenv and virtualenvwrapper
::

    mkvirtualenv my_env
    workon my_env
    pip install flask-user

See also
--------

See also: :doc:`minimal-app`