============
Design Goals
============

* `Reliable`_
* `Secure`_
* `Ready to use`_
* `Fully Customizable`_
* `Nice Feature Set`_
* Well documented
* Data model agnostic (provide your own User model)
* Database ORM abstraction (SQLAlchemyAdapter provided)
* Internationalization Ready

Reliable
--------

We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code through automated tests from the very beginning and we're proud
to consistently achieve code coverage of over 95% without fudging.

Secure
------

Passwords are hashed using ``bcrypt`` by default and can be customized to any
set of hashing algorithms that ``passlib`` supports.

Tokens are encrypted using ``AES`` and signed using the ``itsdangerous`` package.


Ready to use
------------
Installing is as easy as: ``pip install flask-user``. See :doc:`installation`.

The :doc:`recipes_minimal_app` requires only eleven lines of additional code.

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

* Register with username or email or both
* Confirm email, Login, Remember me, Logout
* Change username, Change password, Forgot password
* Secure password hashing and token generation
* Role-based Authorization -- See :doc:`authorization`
* Internationalization -- See :doc:`internationalization`
* Fully customizable -- See :doc:`customization`
* Event notification -- See :doc:`notification`.

