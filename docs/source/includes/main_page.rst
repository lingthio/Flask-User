Flask-User v1.0
===============
**Customizable User Authentication, User Management, and more.**

.. topic:: Attention

    | This is `Flask-User v1.0 <http://flask-user.readthedocs.io/en/latest/>`_ which is **incompatible** with `Flask-User v0.6 <http://flask-user.readthedocs.io/en/v0.6/>`_.
    | Flask-User v1.0 is basically Flask-User v0.6 with a more Pythonic API for customization.
    | This package is production grade, but it is marked as an alpha release because its API may be subject to change.

| So, you're writing a Flask web application and would like to authenticate your users.
| You start with a simple **Login** page, but soon enough you'll need to handle:

* **Registrations** and **Email Confirmations**
* **Change Usernames**, **Change Passwords**, and **Forgotten Passwords**

.. _SupportedLanguages:

And wouldn't it be nice to also offer:

* **Added Security**
* **Increased Reliability**
* **Role-based Authorization**
* **Internationalization** (Chinese, Dutch, English, Farsi, Finnish, French, German, Italian, Russian, Spanish, Swedish, and Turkish)

Customizable, yet Ready to use
------------------------------
* **Largely Configurable** -- By overriding configuration settings.
* **Fully Customizable** -- By overriding methods and properties.
* **Ready to use** -- Through sensible defaults.
* Supports **SQL** and **MongoDB** databases.

Well documented
---------------
- `Flask-User v1.0 documentation <https://flask-user.readthedocs.io/en/latest/>`_
- `Flask-User v0.6 documentation <https://flask-user.readthedocs.io/en/v0.6/>`_
- `Flask-User v0.5 documentation <https://flask-user.readthedocs.io/en/v0.5/>`_

Additional features
-------------------
* **MIT License**
* **Tested** on Python 2.6, 2.7, 3.3, 3.4, 3.5 and 3.6. Coverage: Over 90%.
* **Event hooking** -- Through efficient signals.
* **Support for multiple emails per user**

Minimal Requirements
--------------------
- brypt 2.0+
- cryptography 1.6+
- Flask 0.9+
- Flask-Login 0.2+
- Flask-WTF 0.9+
- passlib 1.6+

Alternatives
------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_
