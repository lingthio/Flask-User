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

    !! News Flash !!
    Some config settings have been renamed for intuitive and consistency reasons:
    - USER_LOGIN_WITH_USERNAME --> USER_ENABLE_USERNAMES (plural)
    - USER_REGISTER_WITH_EMAIL --> USER_ENABLE_EMAILS (plural)
    - USER_RETYPE_PASSWORD     --> USER_ENABLE_RETYPE_PASSWORDS (plural)
    We apologize for any inconvenience but feel confident this will help going forward.

Customizable User Account Management for Flask
----------------------------------------------

Flask-User offers customizable user account management features
with sensible defaults to start using it right out of the box.

* **Reliable**
* **Secure**
* **Customizable**
* **Ready to use functionality**. With sensible defaults for **Register**, **Confirm email**,
  **Login**, **Change password** and **Forgot passwords**.
* **Role-based Authorization** through a simple function decorator.
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Status
------

Though v0.3  is quite stable, it is an Alpha release.
We appreciate it if you would enter issues, suggestions and
enhancement requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.

The v0.4 is in active development.

Documentation
-------------
.. toctree::
    :maxdepth: 2

    design_goals
    install
    authorization
    recipes
    customize
    signals
    api

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