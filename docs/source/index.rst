Flask-User
==========
.. image:: https://pypip.in/v/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://travis-ci.org/lingthio/flask-user.png?branch=master
    :target: https://travis-ci.org/lingthio/flask-user

.. image:: https://coveralls.io/repos/lingthio/flask-user/badge.png?branch=master
    :target: https://coveralls.io/r/lingthio/flask-user?branch=master

.. image:: https://pypip.in/d/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://pypip.in/license/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

::

    !! Newsflash !!
    In v0.3.1 and v0.3.2 confirmation emails were not working
    Please upgrade to v0.3.3 or later. Thank you.

    !! Headsup !!
    The upcoming v0.4 will break v0.3 compatibility. See the Status section below.

Customizable User Login for Flask: Register, Confirm email, Login, Forgot password and more
-------------------------------------------------------------------------------------------

| Many Flask websites require that their users can Register, Confirm email, Login, Logout, Change password and Reset forgotten passwords.
| Each website often requires different and precise customization of this process.

Flask-User aims to provide a ready to use **and** fully customizable package that is:

* **Reliable** (Automated tests cover over 95% of the code base)
* **Secure** (``bcrypt`` password hashing, ``AES`` ID encryption, ``itsdangerous`` token signing)
* **Ready to use**
* **Fully customizable** (Field labels, Flash messages, Form templates, Emails, URLs, and more)
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Status
------

v0.3 is an Alpha release. We would appreciate it if you enter issues, suggestions and
feature requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.

The v0.4 Beta release is in active development. The main purpose of this release is:

* Allowing full Flask-Login customization
* Breaking view function content into re-usable helper functions
  to ease view function customization

Documentation
-------------
.. toctree::
    :maxdepth: 2

    features
    install
    minimal-app
    basic-app
    customize
    signals

Revision History
----------------
* v0.3.6 Added: Provide @login_required. Handle multiple apps.
* v0.3.5 Added: Signals. Refactored automated tests.
* v0.3.4 Added: Support for Python 3.3 (while retaining support for 2.7 and 2.6)
* v0.3.3 Added: Minimal-app and basic-app examples to docs
* v0.3.2 Bug fix: Confirm email did not send confirmation emails
* v0.3.1 Alpha release
* v0.3 Added: Confirm email, Forgot password, Reset password
* v0.2 Added: Change username, Change password
* v0.1 Initial version: Register, Login, Logout

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Roles: Role based authentication
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Alternative Packages
--------------------
I've successfully used `Flask-Security <https://pythonhosted.org/Flask-Security/>`_ in the past.
Flask-Security offers additional role based authentication.

Contact
-------
Ling Thio - ling.thio [at] gmail.com