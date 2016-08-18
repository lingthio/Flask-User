Flask-User |release|
==========

.. image:: https://img.shields.io/pypi/v/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://img.shields.io/travis/lingthio/Flask-User.svg
    :target: https://travis-ci.org/lingthio/Flask-User

.. image:: https://img.shields.io/pypi/dm/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://img.shields.io/pypi/l/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User


Customizable User Account Management for Flask
----------------------------------------------

| So you're writing a Flask web application and would like to authenticate your users.
| You start with a simple **Login** page, but soon enough you'll need to handle:

* **Registrations** and **Email Confirmations**
* **Change Usernames**, **Change Passwords**, and **Forgotten Passwords**

And wouldn't it be nice to also offer:

* **Role-based Authorization**
* **Remember-me cookies**
* **Multiple emails per user**
* **Internationalization**

| Flask-User offers these user features (and more) out-of-the-box
| while also honoring the following developer needs:

* **Tested on Python 2.6, 2.7, 3.3 and 3.4**
* **Reliable** (Code coverage of over 95%)
* **Secure** (Built on top of widely deployed Flask-Login)
* **Ready to use** (Through sensible defaults)
* **Largely configurable** (Through configuration settings)
* **Fully customizable** (Through customizable functions and email templates)
* **Well documented**
* **Translations** (Chinese,  Dutch, English, Finnish, French, Swedish)


.. topic:: Headsup

    Flask-Login v0.3.x broke backward compatibility by using *properties*
    instead of *methods* for current_user.is_authenticated(),
    is_anonymous() and is_active().
    Please upgrade to Flask-User v0.6.8+ if you plan to use Flask-Login v0.3+.


Status
------

| Flask-User |release| is quite stable and is used in production environments.
| It is marked as a Beta release because the API is subject to small changes.
| We appreciate it if you would enter issues and
  enhancement requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.


Demo
----
The `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_ showcases Flask-User.
To protect against spam mis-use, all email features have been disabled.
(If you're the first visitor in the last hour, it may take a few seconds for Heroku to start this service)


Contact Information
-------------------
Ling Thio - ling.thio [at] gmail.com

Feeling generous? `Tip me on Gittip <https://www.gittip.com/lingthio/>`_


Up Next
-------
:doc:`installation`


Documentation
-------------
.. toctree::
    :maxdepth: 2

    design_goals
    limitations
    installation
    data_models
    basic_app
    flask_user_starter_app
    authorization
    roles_required_app
    base_templates
    customization
    signals
    recipes
    internationalization
    faq
    api


Revision History
----------------
* v0.6.8 Added support for Flask-Login v0.3+
* v0.6.7 Uses Python package bcrypt instead of py-bcrypt.
* v0.6.6 Forgot password form now honors USER_SHOW_USERNAME_OR_EMAIL_DOES_NOT_EXIST setting.
* v0.6.5 Added USER_SHOW_USERNAME_OR_EMAIL_DOES_NOT_EXIST setting.
* v0.6.4 Moved custom params from __init__() to init_app(). Added send_reset_password_email().
* v0.6.3 Fix for Python 3.4 and signals. Added UserMixin.has_role() and @roles_accepted().
* v0.6.2 Added support for invitation-only registrations.
* v0.6.1 Added Chinese (Simplified) and French translations`.
* v0.6 Changed User/UserProfile DataModels into UserAuth/User DataModels.

::

  v0.6 Is backwards compatible with v0.5 but UserProfileClass will be deprecated
  in the future. See the 'Data Models' section in this documentation.

* v0.5.5 Added user_profile view. Cleaned up base template. Support for UserProfile.roles.
* v0.5.4 Decoupled Flask-User from Flask-Babel and speaklater
* v0.5.3

  * Added remember-me feature.
  * Added support for a primary key name other than 'id'.
  * Added USER_AUTO_LOGIN\_... settings.
  * Added USER_AFTER\_..._ENDPOINT settings.
  * Cleaned up email templates.

::

    v0.5.3 API changes
    The 'confirm_email' emails are now sent only after a resend confirm email request.
    The 'registered' email is now sent after registration, whether
    USER_ENABLE_CONFIRM_EMAIL is True or False.

    (Previously, the 'confirm_email' email was sent after registration
    and after a resend confirm email request, and the 'registered' email was sent only
    after registration and when USER_ENABLE_CONFIRM_EMAIL was False)


* v0.5.2 Added USER_AUTO_LOGIN setting.
* v0.5.1 Added Support for multiple emails per user.
* v0.5.0 Added ``resend_confirm_email``.
* v0.4.9 Added ``login_or_register.html``. Cleaned up example_apps.
* v0.4.8 Removed the need for app.mail, app.babel, app.db and app.User properties.
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

Contributors
------------
- https://github.com/neurosnap : Register by invitation only
- https://github.com/lilac : Chinese translation
- https://github.com/cranberyxl : Bugfix for login_endpoint & macros.label
- https://github.com/markosys : Early testing and feedback

Alternative Flask extensions
----------------------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

