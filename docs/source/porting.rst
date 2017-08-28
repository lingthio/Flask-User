=====================
Porting v0.6 to v1.0+
=====================

With Flask-User v0.1 through v0.6 we gained insights for an improved Flask-User API,
but we were unable to implement these improvements due to backwards compatibility.

With Flask-User v1.0, we decided to add these improvements at the cost of breaking backward compatibility.

This page describes describes the changes required to make a Flask-User v0.6 application
work with Flask-User v1.0.

UserManager() setup
-------------------
We simplified the Flask-User setup by removing the need to specify the db_adapter explicitly.

Flask-User v0.6::

    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager, SQLAlchemyAdapter

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User, UserEmailClass=UserEmail)
    user_manager = UserManager(db_adapter, app)

Flask-User v1.0::

    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager    # No need for SQLAlchemyAdapter

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User, UserEmailClass=UserEmail)

The `db`  parameter can be any Database instance (for example `SQLAlchemy()` or a `MongoAlchemy()`) and the
appropriate DbAdapter will be configured internally.


PasswordManager() changes
-------------------------
Password related methods have been moved from the UserManager class to a separate PasswordManager class,
accessible through the UserManager.password_manager attribute.

We renamed `verify_password()` to `verify_user_password()` to better reflect what this method does.

We changed the `verify_user_password()` parameter order to be consistent with the parameter order of `update_user_hashed_password()`.

We renamed `update_password()` to `update_user_hashed_password()` to better reflect what this method does.

we renamed the `PASSWORD_HASH` setting to `PASSWORD_HASH_SCHEME` to better reflect what this setting means.

We removed the hash scheme option `"plaintext"` for security reasons.

Flask-User v0.6::

    verify_password(password, user)    # v0.6 parameter order
    update_password(user, hashed_password)

Flask-User v1.0::

    password_manager.verify_user_password(user, password)    # v0.6 parameter order
    password_manager.update_user_hashed_password(user, hashed_password)

As a courtesy, we allow both `verify_user_password()` parameter orders in v1.0, but a warning will
be issued and the v0.6 style will be obsoleted in the future.


EmailManager() changes
----------------------
Email related methods have been moved from the UserManager class to a separate EmailManager class,
accessible through the UserManager.email_manager attribute.


TokenManager() changes
----------------------
The v0.6 `_encode_id()` and `_decode_id()` assumed that IDs were limited to 16 digits.

This limitation has been removed in v1.0, to support Mongo ObjectIDs.

As a result, the generated tokens are different, which will affect two areas:

- v0.6 user-sessions that were stored in a browser cookie, are no longer valid in v1.0 and the user will be
required to login again.

- v0.6 password tokens that were sent in password reset emails are no longer valid in v1.0
and the user will have to issue a new forgot-password email request.
This effect is mitigated by the fact that these tokens are meant to expire relatively quickly.


