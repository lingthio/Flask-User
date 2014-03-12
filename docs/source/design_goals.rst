============
Design Goals
============

* `Reliable`_
* `Secure`_
* `Easy to Install`_
* `Ready to use`_
* `Fully Customizable`_
* `Nice Feature Set`_
* Well documented
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

See :doc:`installation`

Ready to use
------------

The :doc:`minimal_app` requires only eleven lines of additional code.

Fully Customizable
------------------
* Emails
* Features
* Field labels
* Field validators
* Field validation messages
* Flash messages
* Forms
* Form templates
* Password and Username validators
* Password hashing algorithms
* Token generator
* URLs
* View functions

See :doc:`customization`

Nice Feature Set
----------------

* Register with username or email,
* Confirm email, Login, Logout
* Change username, Change password, Forgot password
* Secure password hashing and token generation
* Role-based Authorization -- See :doc:`authorization`
* Easy to setup and Ready to use -- See :doc:`minimal_app`
* Fully customizable -- See :doc:`customization`
* Form validation
* Event notification -- See :doc:`notification`.
* Internationalization ready

Planned Features
----------------
* Registration by invitation only
* Profile editing with pictures and thumbnails
* Role based authorization
