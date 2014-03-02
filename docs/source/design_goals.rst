============
Design Goals
============

* `Reliable`_
* `Secure`_
* `Easy to Install`_
* `Ready to use`_
* `Fully Customizable`_
* `Good Feature Set`_
* Data model agnostic (provide your own User model)
* Database ORM abstraction (SQLAlchemyAdapter provided)
* Internationalization Ready

Reliable
--------
.. image:: https://pypip.in/v/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://travis-ci.org/lingthio/flask-user.png?branch=master
    :target: https://travis-ci.org/lingthio/flask-user

.. image:: https://coveralls.io/repos/lingthio/flask-user/badge.png?branch=master
    :target: https://coveralls.io/r/lingthio/flask-user?branch=master

We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code through automated tests from the very beginning and we're proud
to consistently achieve code coverage of over 95% without fudging.

Secure
------

Passwords are hashed using ``bcrypt`` by default and can be customized to any
set of hashing algorithms that ``passlib`` supports.

Tokens are encrypted using ``AES`` and signed using the ``itsdangerous`` package.

Easy to Install
---------------
Installing is as easy as: ``pip install flask-user``

See :doc:`install`

Ready to use
------------
::

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

See :doc:`minimal_app`

Fully Customizable
------------------
* Email Subject lines, HTML messages and Text messages
* Features
* Field labels
* Field validators
* Field validation messages
* Flash messages
* Forms
* Form templates,
* Password hashing algorithms,
* Password validator
* Token generator,
* Username validator
* URLs
* View functions,

See :mod:`customize`

Good Feature Set
----------------

* Change password Form (with or without retype password)
* Change username Form
* Forgot password Form
* Login Form
* Logout Form
* Register Form (with email, username or both)
* Reset password Form (with or without retype password)
* Secure password hashing and token generation
* Form validation
* Event notification -- See :doc:`signals`.
* Fully customizable
* Internationalization ready

Planned Features
----------------
* Registration by invitation only
* Profile editing with pictures and thumbnails
* Role based authorization
