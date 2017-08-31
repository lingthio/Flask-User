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

Configuration settings changes
------------------------------
We split ``USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST`` into ``USER_SHOW_USERNAME_DOES_NOT_EXIST``
and ``USER_SHOW_EMAIL_DOES_NOT_EXIST`` and set the default to False for increased security.

Flask-User v0.6::

    USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST = True

Flask-User v1.0::

    USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False


Data-model changes
------------------
The `confirmed_at` attribute name has been renamed to `email_confirmed_at` to better reflect what this attribute means.

Flask-User v0.6::

    class User(db.Model, UserMixin):
            ....
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

    or:

    class UserEmail(db.Model, UserMixin):
            ....
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

Flask-User v1.0 (keeping the original database column names)::

    class User(db.Model, UserMixin):
            ....
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column('confirmed_at', db.DateTime())

    or:

    class UserEmail(db.Model, UserMixin):
            ....
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column('confirmed_at', db.DateTime())

The optional UserAuth class has been obsoleted. See below for a workaround.


Flask-Login v0.3+ required
--------------------------
Since Flask-Login v0.3.0, `is_authenticated()`, `is_active()`, and `is_anonymous()`
**methods** have been replaced by `is_authenticated`, `is_active`, and `is_anonymous` **properties**.


PasswordManager() changes
-------------------------
Password related methods have been moved from the UserManager class to a separate PasswordManager class,
accessible through the UserManager.password_manager attribute.

We renamed `verify_password()` to `verify_user_password()` to better reflect what this method does.

We changed the `verify_user_password()` parameter order to be consistent with the parameter order of `update_user_hashed_password()`.

We renamed `update_password()` to `update_user_hashed_password()` to better reflect what this method does.

we renamed the `PASSWORD_HASH` setting to `PASSWORD_HASH` to better reflect what this setting means.

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
The v0.6 `token_manager.generate_token()` assumed that IDs were limited to 16 digits.
This limitation has been removed in v1.0, to support Mongo ObjectIDs.

In v1.0, we added the last 8 bytes of the hashed passwords to `token_manager.generate_token()`
to invalidate tokens when a user changes their password.

As a result, the generated tokens are different, which will affect two areas:

- v0.6 user-session tokens, that were stored in a browser cookie, are no longer valid in v1.0
  and the user will be required to login again.

- v0.6 password-reset tokens, that were sent in password reset emails, are no longer valid in v1.0
  and the user will have to issue a new forgot-password email request.
  This effect is mitigated by the fact that these tokens are meant to expire relatively quickly.

- user-session tokens and password-reset tokens become invalid if the user changes their password.

UserAuth class
--------------

The optional v0.6 UserAuth class has been fully obsoleted in v1.0 to simplify the Flask-User source code.

If you are using SQLAlchemy and choose to separate the uer authorization fields
from the user profile fields, you can use the workaround recipe below::


    # Define the UserAuth data model.
    class UserAuth(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        # Relationship to user
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        user = db.relationship('User', uselist=False)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')


    # Define the User data model. Make sure to add flask_user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())

        # User information
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

        # Relationships
        user_auth = db.relationship('UserAuth', uselist=False)


        # Create UserAuth instance when User instance is created
        def __init__(self, *args, **kwargs):
            super(User, self).__init__(*args, **kwargs)
            self.user_auth = UserAuth(user=self)


        # Map the User.username field into the UserAuth.username field
        @property
        def username(self):
            return user_auth.username

        @username.setter
        def username(self, value)
            user_auth.username = value


        # Map the User.password field into the UserAuth.password field
        @property
        def password(self):
            return user_auth.password

        @password.setter
        def password(self, value)
            user_auth.password = value
