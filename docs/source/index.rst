Introduction
============

Customizable User Authentication
--------------------------------

| So, you're writing a Flask web application and would like to authenticate your users.
| You start with a simple **Login** page, but soon enough you'll need to handle:

* **Registrations** and **Email Confirmations**
* **Change Usernames**, **Change Passwords**, and **Forgotten Passwords**

And wouldn't it be nice to also offer:

* **Role-based Authorization**
* **Internationalization**
* **Support for multiple emails per user**
* **Event hooking**

| Flask-User offers these features and more.

Secure and Reliable
-------------------
* **Secure** -- Built on top of widely deployed Passlib, PyCrypto, ItsDangerous.
* **Reliable** -- Code coverage of over 95%
* **Available** -- Tested on Python |supported_python_versions_and|
* **Well documented**

Fully customizable, yet Ready to use
------------------------------------
* **Largely configurable** -- Through configuration settings
* **Fully customizable** -- Through customizable functions and email templates
* **Ready to use** -- Through sensible defaults

Comes with translations
-----------------------
Chinese, Dutch, English, Farsi, Finnish, French, German, Italian, Russian, Spanish, Swedish, and Turkish

Requirements
------------
Flask-User requires the following Python packages:

- Python |supported_python_versions_or|
- Flask 0.10+
- Flask-Login 0.3+
- Flask-Mail 0.9+ or Flask-Sendmail
- Flask-WTF 0.9+
- passlib 1.6+
- pycrypto 2.6+

Optionally, for fast bcrypt encryption:

- py-bcript 0.4+

For SQLAlchemy applications:

- Flask-SQLAlchemy 1.0+
- A DBAPI driver (such as mysql-python for MySQL or psycopg2 for PostgreSQL)

Optionally, for Event Notification:

- blinker 1.3+

Optionally, for Internationalization:

- Flask-Babel 0.9+
- speaklater 1.3+

Alternatives
------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_

Table of Contents
-----------------
.. toctree::
    :maxdepth: 2

    index
    installation
    quickstart
    flask_user_starter_app
    limitations
    data_models
    porting
    authorization
    roles_required_app
    base_templates
    customization
    signals
    recipes
    internationalization
    faq
    api


