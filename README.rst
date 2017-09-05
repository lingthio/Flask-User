Flask-User v0.6
===============
**Customizable User Authentication & Management**

| **Attention:**
| The documentation has moved to http://flask-user.readthedocs.io/en/v0.6
|
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
* **Secure** -- Built on top of widely deployed Passlib, PyCrypto, ItsDangerous.
* **Reliable** -- Code coverage of over 95%
* **Available** -- Tested on Python 2.6, 2.7 and 3.3-3.6

Well documented
---------------
- `Flask-User v0.6 documentation <http://flask-user.readthedocs.io/en/v0.6/>`_
- `Flask-User v0.5 documentation <http://flask-user.readthedocs.io/en/v0.5/>`_

Fully customizable, yet Ready to use
------------------------------------
* **Largely configurable** -- Through configuration settings
* **Fully customizable** -- Through customizable functions and email templates
* **Ready to use** -- Through sensible defaults
* Supports **SQL Databases** -- Through SQLAlchemy
* **Event hooking** -- Through signals

Comes with translations
-----------------------
Chinese, Dutch, English, Farsi, Finnish, French, German, Italian, Russian, Spanish, Swedish, and Turkish

Requirements
------------
Flask-User requires the following Python packages:

- Flask 0.9+
- Flask-Babel 0.9+
- Flask-Login 0.3+
- Flask-Mail 0.9+
- Flask-SQLAlchemy 1.0+
- Flask-WTF 0.9+
- passlib 1.6+
- pycryptodome
- speaklater 1.3+

Optionally:

- blinker 1.3+ -- for Event Notification
- Flask-Sendmail -- for sending emails via ``sendmail``
- py-bcript 0.4+ -- for fast bcrypt encryption

Alternatives
------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_
