Flask-User
==========
.. image:: https://pypip.in/v/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://travis-ci.org/lingthio/Flask-User.png?branch=master
    :target: https://travis-ci.org/lingthio/Flask-User

.. comment .. image:: https://coveralls.io/repos/lingthio/Flask-User/badge.png?branch=master
.. comment     :target: https://coveralls.io/r/lingthio/Flask-User?branch=master

.. image:: https://pypip.in/d/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://pypip.in/license/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

::

    !! News Flash: v0.4.1 API changes !!
    - User.email_confirmed_at                          --> confirmed_at
    - templates/flask_user/emails/confirmation_email_* --> registered_*
    - signals.confirmation_email_set                   --> user_registered
    - template variable {{ confirmation_link }}        --> {{ confirm_email_link }}
    - templates/flask_user/emails/reset_password_*     --> forgot_password_*
    - signals.reset_password_email_sent                --> user_forgot_password

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
* **Ready to use**
* **Fully customizable**
* **Role-based Authorization**
* **Internationalization**
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Demo
----
| `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_
| (If you're the first visitor in the last hour, this may take a few seconds to load)

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
    faq
    api


Contact Information
-------------------
Ling Thio - ling.thio [at] gmail.com

Feeling generous? `Tip me on Gittip <https://www.gittip.com/lingthio/>`_

Revision History
----------------
* v0.4.2 Cleanup of SQLAlchemyAdapter. Added tox for Python 3.4
* v0.4.1 Cleanup of customized email messages and signals.
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
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Acknowledgements
----------------
This project would not be possible without the use of the following amazing offerings:

* `Flask <http://flask.pocoo.org/>`_
* `Flask-Babel <http://babel.pocoo.org/>`_
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Mail <http://pythonhosted.org/flask-mail/>`_
* `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
* `Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_
* `SQLAlchemy <http://www.sqlalchemy.org/>`_
* `WTForms <http://wtforms.readthedocs.org/en/latest/>`_

Alternative Flask Extensions
----------------------------
`Flask-Security <https://pythonhosted.org/Flask-Security/>`_

