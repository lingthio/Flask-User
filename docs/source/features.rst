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
| * Database ORM abstraction        |                                    |
|   (SQLAlchemyAdapter provided)    |                                    |
| * Internationalization Ready      |                                    |
+-----------------------------------+------------------------------------+

Reliable
--------
We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code through automated tests from the very beginning and we're proud
to consistently achieve code coverage of over 95% without fudging.

Here is our Feb 2014 code coverage report::

    > coverage report
    Name                                                            Stmts   Miss  Cover
    -----------------------------------------------------------------------------------
    flask_user/__init__                                                93      0   100%
    flask_user/db_interfaces                                           51      0   100%
    flask_user/emails                                                  28      0   100%
    flask_user/forms                                                  149      3    98%
    flask_user/passwords                                                4      0   100%
    flask_user/tokens                                                  37      0   100%
    flask_user/views                                                  128     13    90%
    -----------------------------------------------------------------------------------
    TOTAL                                                             490     16    97%

Secure
------

Passwords are hashed using bcrypt by default and can be customized to any hashing
algorithm that ``passlib`` supports.

The user ID in Confirm email and Reset password tokens are encrypted using AES
and signed using the ``itsdangerous`` package.


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

See :doc:`minimal-app`

Planned Features
----------------
* Event signaling through blinker
* Registration by invitation only
* Profile editing with pictures and thumbnails
* Role based authorization
