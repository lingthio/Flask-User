========
Features
========
+-----------------------------------+------------------------------------+
| * Reliable                        | * Register with email address      |
| * Secure                          | * Register with username           |
| * Easy to Install and Setup       | * Confirm email address            |
| * Ready to use                    | * Login and Logout                 |
| * Fully Customizable              | * Change username                  |
| * Data model agnostic             | * Change password                  |
|   (provide your own User model)   | * Reset forgotten password         |
| * Database ORM abstraction        | * Notification signals             |
|   (SQLAlchemyAdapter provided)    |                                    |
| * Internationalization Ready      |                                    |
+-----------------------------------+------------------------------------+

Reliable
--------
We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code through automated tests from the very beginning and we're proud
to consistently achieve code coverage of over 95% without fudging.

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

Secure
------

Passwords are hashed using ``bcrypt`` by default and can be customized to any
set of hashing algorithms that ``passlib`` supports.

Tokens are encrypted using ``AES`` and signed using the ``itsdangerous`` package.


Fully Customizable
------------------
The following aspects work out-of the box **and** can be full customized:

* **Email message templates**
* **Field labels**
* **Flash messages**
* **Form classes**
* **Form templates**
* **Password hashing methods**
* **Password validator**
* **URLs**
* **Username validator**
* **Validation messages**
* **View functions**

See :doc:`customize`

Easy to Install
---------------
::

    pip install flask-user

See :doc:`install`

Easy to Setup
-------------

See :doc:`minimal-app` or :doc:`basic-app`

Planned Features
----------------
* Registration by invitation only
* Profile editing with pictures and thumbnails
* Role based authorization
