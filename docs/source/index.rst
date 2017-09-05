Flask-User v0.6
===============
**Customizable User Authentication & Management**

.. topic:: Attention

    IMPORTANT: Flask-User v0.9 is under development and breaks
    backward compatibility with Flask-User v0.6.

    To avoid disruption, please take the time to pin your Flask-User version
    in your ``requirements.txt``. For example: ``Flask-User==0.6.17``

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
* **Available** -- Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5 and 3.6

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


Table of Contents
-----------------
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


.. include:: ../../CHANGES.rst

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

