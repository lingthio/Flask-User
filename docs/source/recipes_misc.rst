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
