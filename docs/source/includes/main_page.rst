Flask-User v0.9
===============
**Customizable User Authentication, User Management, and more.**

.. topic:: Attention

    Flask-User v0.9 (pre-alpha) is under active development and not recommended for production use at this time.
    Please use `Flask-User v0.6 <http://flask-user.readthedocs.io/en/v0.6/>`_ (stable) for now.

| So, you're writing a Flask web application and would like to authenticate your users.
| You start with a simple **Login** page, but soon enough you'll need to handle:

* **Registrations** and **Email Confirmations**
* **Change Usernames**, **Change Passwords**, and **Forgotten Passwords**

And wouldn't it be nice to also offer:

* **Added security**
* **Increased reliability**
* **Role-based Authorization**
* **Internationalization**
* **Support for multiple emails per user**

| Flask-User offers these features and more.

Secure and Reliable
-------------------
* **Secure** -- Built on top of widely deployed Passlib and Cryptography.
* **Reliable** -- Code coverage of over 95%
* **Available** -- Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5 and 3.6

Well documented
---------------
- `Flask-User v0.6 documentation <http://flask-user.readthedocs.io/en/v0.6/>`_
- `Flask-User v0.5 documentation <http://flask-user.readthedocs.io/en/v0.5/>`_

Fully customizable, yet Ready to use
------------------------------------
* **Ready to use** -- Through sensible defaults.
* **Largely configurable** -- By overriding configuration settings.
* **Almost fully customizable** -- By overriding default methods and properties.
* Supports **SQL Databases** and **MongoDB Databases**.
* **Event hooking** -- Through efficient signals.

Comes with translations
-----------------------
Chinese, Dutch, English, Farsi, Finnish, French, German, Italian, Russian, Spanish, Swedish, and Turkish

Requirements
------------
Flask-User requires the following Python packages:

- cryptography 2.0+
- Flask 0.9+
- Flask-Login 0.3+
- Flask-WTF 0.9+
- passlib 1.6+

Optionally:

- blinker 1.3+ -- for Event Notification
- Flask-Babel 0.9+ -- for translations
- Flask-Mail 0.9+ -- for sending mail with SMTP
- Flask-MongoEngine 0.9+ -- for MongoDB applications
- Flask-Sendmail -- for sending mail with sendmail
- Flask-SQLAlchemy 1.0+ -- for SQL database applications
- py-bcript 0.4+ -- for fast bcrypt encryption
- speaklater 1.3+ -- for translations

Alternatives
------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

Authors
-------
* Ling Thio - ling AT gmail DOT com
* `Many contributors from coders/translators <https://github.com/lingthio/Flask-User/graphs/contributors>`_