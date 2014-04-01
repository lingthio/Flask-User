Miscellaneous
=============

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

    hashed_password = user.password
    does_match = user_manager.verify_password(password, hashed_password)

Account Tracking
----------------
Flask-User deliberately stayed away from implementing account tracking features because:

* What to track is often customer specific
* Where to store it is often customer specific
* Custom tracking is easy to implement using signals

Here's an example of tracking login_count and last_login_ip:

::

    # This code has not been tested

    @user_logged_in.connect_via(app)
    def _track_logins(sender, user, **extra):
        user.login_count += 1
        user.last_login_ip = request.remote_addr
        db.session.commit()