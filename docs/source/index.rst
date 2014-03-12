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

    !! News Flash: v0.4.1 API changes !!
    - templates/flask_user/emails/confirmation_email_* --> registered_*
    - signals.confirmation_email_set                   --> user_registered
    - template variable {{ confirmation_link }}        --> {{ confirm_email_link }}
    - templates/flask_user/emails/reset_password_*     --> forgot_password_*
    - signals.reset_password_email_sent                --> forgot_password_email_sent

Customizable User Account Management for Flask
----------------------------------------------

Many web applications require User Account Management features such as **Register**, **Confirm email**,
**Login**, **Change username**, **Change password** and **Forgot password**.

Some also require **Role-based Authorization** and **Internationalization**.

Wouldn't it be nice to have a package that would offer these features **out-of-the-box**
while retaining **full control over the workflow and presentation** of this process?

Flask-User aims to provide such a ready-to-use **AND** fully customizable solution:

* **Reliable**
* **Secure**
* **Fully customizable**
* **Ready to use**
* **Role-based Authorization**
* **Internationalization**
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Status
------

Though v0.4 is quite stable, it is a Beta release and the API is subject to small changes.
We appreciate it if you would enter issues and
enhancement requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.


Documentation
-------------
.. toctree::
    :maxdepth: 2

    design_goals
    installation
    recipes
    authorization
    customization
    internationalization
    notification
    api

Revision History
----------------
* v0.4.1 Customized email messages.
* v0.4.0 Beta release. Translations via Babel.
* v0.3.8 Role-based authorization via @roles_required.
* v0.3.5 Support for Python 2.6, 2.7 and 3.3, Event notifications.
* v0.3.1 Alpha release. Email sending, Confirm email, Forgot password, Reset password.
* v0.2 Change username, Change password.
* v0.1 Register, Login, Logout.

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Roles: Role based authentication
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Alternative Packages
--------------------
`Flask-Security <https://pythonhosted.org/Flask-Security/>`_

Contact
-------
Ling Thio - ling.thio [at] gmail.com