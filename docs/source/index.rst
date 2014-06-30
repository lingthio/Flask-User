Flask-User
==========
.. image:: https://travis-ci.org/lingthio/Flask-User.png?branch=master
    :target: https://travis-ci.org/lingthio/Flask-User

.. comment .. image:: https://pypip.in/v/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User

.. comment .. image:: https://coveralls.io/repos/lingthio/Flask-User/badge.png?branch=master
.. comment     :target: https://coveralls.io/r/lingthio/Flask-User?branch=master

.. comment .. image:: https://pypip.in/d/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User

.. comment .. image:: https://pypip.in/license/Flask-User/badge.png
.. comment     :target: https://pypi.python.org/pypi/Flask-User


Customizable User Account Management for Flask
----------------------------------------------

Many web applications require User Account Management features such as **Register**, **Confirm email**,
**Login**, **Change username**, **Change password** and **Forgot password**.

Some also require **Role-based Authorization** and **Internationalization**.

Wouldn't it be nice to have a package that would offer these features **out-of-the-box**
while retaining **full customization control** over the workflow and presentation of this process?

Flask-User aims to provide such a ready-to-use **AND** fully customizable solution:

* **Reliable**
* **Secure**
* **Ready to use**
* **Fully customizable**
* **Role-based Authorization**
* **Internationalization**
* **Well documented**
* Tested on Python 2.6, 2.7, 3.3 and 3.4

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
    base_templates
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
* v0.5.2 USER_AUTO_LOGIN=True setting to auto-login already logged in users in user.login page.
* v0.5.1 Support for multiple emails per user.
* v0.5.0 Added ``resend_confirm_email``.
* v0.4.9 Added ``login_or_register.html``. Cleaned up example_apps.
* v0.4.8 Removed the need for app.mail, app.babel, app.db and app.User
* v0.4.7 Added 'confirm_email', 'password_changed' and 'username_changed' emails.

::

    v0.4.7 API changes
    The 'registered' email was split into 'confirm_email' and 'registered' emails.
    If you've customized 'templates/flask_user/email/registered_*':
    rename the 'registered_*' files into 'confirm_email_*'.

* v0.4.6 Added 'next' query parameter to confirm_email link
* v0.4.5 Save custom Register fields to User or UserProfile

::

    v0.4.5 API changes
    db_adapter.add_object()/update_object()/delete_object() now require a separate
    call to db_adapter.commit()

* v0.4.4 Enhancements and Fixes: Github issues #6, #7 & #8
* v0.4.3 base.html, flask_user/public_base.html, flask_user/member_base.html.
  Cleanup. Reduced package size from 83KB to 30KB.

::

    v0.4.3 API changes
    Form templates now inherit from templates/flask_user/public_base.html,
    templates/flask_user/member_base.html and templates/base.html.

* v0.4.2 Cleanup of SQLAlchemyAdapter. Added tox for Python 3.4
* v0.4.1 Cleanup of customized email messages and signals.

::

    v0.4.1 API changes
    - User.email_confirmed_at                          --> confirmed_at
    - templates/flask_user/emails/confirmation_email_* --> registered_*
    - signals.confirmation_email_set                   --> user_registered
    - template variable {{ confirmation_link }}        --> {{ confirm_email_link }}
    - templates/flask_user/emails/reset_password_*     --> forgot_password_*
    - signals.reset_password_email_sent                --> user_forgot_password

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
* `SQLAlchemy <http://www.sqlalchemy.org/>`_ and `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
* `WTForms <http://wtforms.readthedocs.org/en/latest/>`_ and `Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_

Alternative Flask extensions
----------------------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

