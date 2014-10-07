============
Design Goals
============

Reliable
--------

We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code through automated tests from the very beginning and we're proud
to consistently achieve code coverage of over 95% without fudging.

Secure
------

Passwords are hashed using **bcrypt** by default and can be customized to any
set of hashing algorithms that **passlib** supports.
Tokens are encrypted using **AES** and signed using the **itsdangerous** package.

Fully Customizable
------------------
We offer as much customization as possible through the use of configuration settings.
The remainder is customizable by writing and configuring your own custom functions.
See :doc:`customization`.

Ready to use
------------
Installing is as easy as: ``pip install flask-user``. See :doc:`installation`.

Through the use of **sensible defaults**, our fully customizable package
is also ready-to-use.
The :doc:`recipes_minimal_app` requires only eleven lines of additional code
and all the default web forms and email templates could be used in production as-is.

Great Feature Set
-----------------

* Login with username or email or both, Remember me, Logout
* Register, Confirm email, Resend confirmation email
* Forgot password, Change username, Change password
* Secure password hashing and token generation
* Role-based Authorization -- See :doc:`authorization`
* Internationalization -- See :doc:`internationalization`
* Event notification -- See :doc:`notification`.

Also
----
* Well documented
* Data model agnostic (provide your own User model)
* Database ORM abstraction (SQLAlchemyAdapter provided)
