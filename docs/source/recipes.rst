=======
Recipes
=======

Here we explain the use of Flask-User through code recipes.

Login Form and Register Form on one page
----------------------------------------
Some websites may prefer to show the login form and the register form on one page.

Flask-User (v0.4.9 and up) ships with a ``login_or_register.html`` form template which requires the following
application config settings:

* ``USER_LOGIN_TEMPLATE='flask_user/login_or_register.html'``
* ``USER_REGISTER_TEMPLATE='flask_user/login_or_register.html'``

This would accomplish the following:

* The ``/user/login`` and ``user/register`` URLs will now render ``login_or_register.html``.
* ``login_or_register.html`` now displays a Login form and a Register form.
* The Login button will post to ``/user/login``
* The Register button will post to ``/user/register``


After registration hook
-----------------------
Some applications require code to execute just after a new user registered for a new account.
This can be achieved by subscribing to the ``user_registered`` signal as follows:

::

    from flask_user.signals import user_registered

    @user_registered.connect_via(app)
    def _after_registration_hook(sender, user, **extra):
        sender.logger.info('user registered')

See also: :doc:`signals`


Hashing Passwords
-----------------
If you want to populate your database with User records with hashed passwords use ``user_manager.hash_password()``:

::

    user = User(
            email='user1@example.com',
            password=user_manager.hash_password('Password1'),
            )
    db.session.add(user)
    db.session.commit()

You can verify a password with ``user_manager.verify_password()``:

::

    does_match = user_manager.verify_password(password, user.password)

Account Tracking
----------------
Flask-User deliberately stayed away from implementing account tracking features because:

* What to track is often customer specific
* Where to store it is often customer specific
* Custom tracking is easy to implement using signals

Here's an example of tracking login_count and last_login_ip:

::

    # This code has not been tested

    from flask import request
    from flask_user.signals import user_logged_in

    @user_logged_in.connect_via(app)
    def _track_logins(sender, user, **extra):
        user.login_count += 1
        user.last_login_ip = request.remote_addr
        db.session.commit()

Here's an example of tracking an invalid password login attempt:

::
    # This code has not been tested

    from datetime import datetime
    from flask import request
    from flask_user.signals import user_password_failed

    @user_password_failed.connect_via(app)
    def _track_invalid_password_login_attempts(sender, user, **extra):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.lockout = True
        db.session.commit()
