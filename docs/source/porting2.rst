.. _Porting2:

Porting v0.6 to v9.0+ - Complete list of changes
================================================

For porting customized Flask-User v0.6 applications, here is a complete list of
changes that may cause incompatibility issues.

UserManager() setup
-------------------
We simplified the Flask-User setup by removing the need to specify the db_adapter explicitly::

    From v0.6
    ---------
    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager, SQLAlchemyAdapter

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User, UserEmailClass=UserEmail)
    user_manager = UserManager(db_adapter, app)


    To v0.9+
    --------
    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager    # No need for SQLAlchemyAdapter

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User, UserEmailClass=UserEmail)

The `db`  parameter type (for example `SQLAlchemy()` or `MongoEngine()`)
is used internally to select the appropriate DbAdapter.


UserManager customization
-------------------------
Flask-User customization now happens by extending a a CustomUserManager class
and by overriding its properties and methods::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():
            # override some properties
                ...

        # Override a method
        def some_custom_method():
            ....

``UserManager()`` now requires the ``app``, ``db`` and ``UserClass`` parameters, and optionally
accepts ``UserEmailClass`` and ``UserInvitationClass``.

If your code used to pass other parameters to the ``UserManager()``,
you'll have to move some code around to conform to the new way of customization.

.. seealso:: :ref:`UserManagerClass`

Data-model changes
------------------
The `confirmed_at` property name has been renamed to `email_confirmed_at` to better reflect what this property means.
Update your User data-model::

    # from v0.6
    # ---------
    class User(db.Model, UserMixin)
        confirmed_at = db.Column(db.DateTime())


    # to v0.9 with global rename of '.confirmed_at' to '.email_confirmed_at'
    # -------
    # Rename property name, but keep column name
    class User(db.Model, UserMixin)
        email_confirmed_at = db.Column('confirmed_at', db.DateTime())


    # to v0.9 without global rename
    # -------
    class User(db.Model, UserMixin)
        confirmed_at = db.Column('confirmed_at', db.DateTime())

        @property
        email_confirmed_at(self):
            return self.confirmed_at

        @email_confirmed_at.setter
        email_confirmed_at(self, value):
            self.confirmed_at = value

The optional UserAuth class has been obsoleted. See below for a workaround.

The UserInvite class name has been renamed to UserInvitation.
You may want to keep the old database table name like so::

    # From v0.6
    # class UserInvite(db.Model):

    # To v0.9
    class UserInvitation(db.Model):
        __tablename__ = 'user_invite'


Configuration settings changes
------------------------------
We renamed ``USER_ENABLE_RETYPE_PASSWORD`` to ``USER_REQUIRE_RETYPE_PASSWORD``
to better reflect what this setting does.

::

    # From v0.6
    # USER_ENABLE_RETYPE_PASSWORD = True

    # To v0.9+
    USER_REQUIRE_RETYPE_PASSWORD = True

We renamed ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL`` to
``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL``
to better reflect what this setting does.

::

    # From v0.6
    # USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = False

    # To v0.9+
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False

We split ``USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST`` into ``USER_SHOW_USERNAME_DOES_NOT_EXIST``
and ``USER_SHOW_EMAIL_DOES_NOT_EXIST`` and set the default to False for increased security --
Hackers won't be able to differentiate between an invalid password event
or a non-existing email/username event::

    # From v0.6
    # USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST = True

    # To v0.9+
    USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False

We replaced ``MAIL_DEFAULT_SENDER`` with ``USER_EMAIL_SENDER_EMAIL`` and ``USER_EMAIL_SENDER_NAME``
to enable support for multiple EmailMailer backends::

    # From v0.6
    # MAIL_DEFAULT_SENDER = '"App name" <info@example.com>'

    # To v0.9+
    USER_EMAIL_SENDER_EMAIL = 'info@example.com'    # Required for sending Emails
    USER_EMAIL_SENDER_NAME = 'App name'   # Optional

We replaced ``USER_PASSWORD_HASH`` with ``USER_PASSLIB_CRYPTCONTEXT_SCHEMES``
(and USER_PASSLIB_CRYPTCONTEXT_KEYWORDS) to allow full customization of password hashing::

    # From v0.6
    # USER_PASSWORD_HASH = 'bcrypt'    # This was a string

    # To v0.9+
    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['bcrypt']    # Notice that this is now a LIST of strings
    USER_PASSLIB_CRYPTCONTEXT_KEYWORDS = dict()


If you move from Flask-Login v0.2 to v0.3+
------------------------------------------
Since Flask-Login v0.3.0:
- the ``.is_authenticated()``, ``.is_active()``, and ``.is_anonymous()`` **methods**
- have been replaced by ``.is_authenticated``, ``.is_active``, and ``.is_anonymous`` **properties**


Password method changes
-----------------------
We changed the ``verify_password()`` parameters to receive a ``password_hash`` parameter
instead of the ``user`` parameter to keep the PasswordManager unaware of User objects::

    # From v0.6
    # user_manager.verify_password(password, user)


    # To v0.9
    user_manager.verify_password(password, user.password)

EmailManager() changes
----------------------
Email related methods have been moved from the UserManager class to a separate EmailManager class,
accessible through the UserManager.email_manager property.


TokenManager() changes
----------------------
The v0.6 `token_manager.generate_token()` assumed that IDs were limited to 16 digits.
This limitation has been removed in v0.9+, to support Mongo ObjectIDs.

In v0.9+, we added the last 8 bytes of the hashed passwords to `token_manager.generate_token()`
to invalidate tokens when a user changes their password.

As a result, the generated tokens are different, which will affect two areas:

- v0.6 user-session tokens, that were stored in a browser cookie, are no longer valid in v0.9+
  and the user will be required to login again.

- Unused v0.6 password-reset tokens and user-invitation tokens, are no longer valid in v0.9+
  and the affected users will have to issue new forgot-password emails and new
  user invitatin emails.
  This effect is mitigated by the fact that these tokens are meant to expire relatively quickly.

- user-session tokens and password-reset tokens become invalid if the user changes their password.

@confirm_email_required decorator deprecated
--------------------------------------------
The ``@confirm_email_required`` view decorator has been deprecated for security reasonse.

| In v0.6, the ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL`` setting removed
    confirmed email protection for all the views and required developers to re-protect
    the vulnerable views with ``@confirm_email_required``.
| In v0.9+ we adopt the opposite approach where the (renamed) ``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL=True``
    setting continues to protect all the views, except those decorated with the
    new ``@allow_unconfirmed_email`` decorator.


UserAuth class deprecated
-------------------------

Support for the optional v0.6 UserAuth class has been dropped in v0.9+ to simplify the Flask-User source code
and make it more readable for customization.

If you are using SQLAlchemy and choose to separate the uer authorization fields
from the user profile fields, you can use the workaround recipe below (this has
not been tested -- comments welcomed)::


    # Define the UserAuth data-model.
    class UserAuth(db.Model):
        __tablename__ = 'user_auths'
        id = db.Column(db.Integer, primary_key=True)

        # Relationship to user
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        user = db.relationship('User', uselist=False)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')


    # Define the User data-model. Make sure to add flask_user UserMixin!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
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


    # From v0.6
    # db_adapter = SQLAlchemyDbAdapter(db, User, UserAuthClass=UserAuth)
    # user_manager = UserManager(db_adapter, app)

    # To v0.9+
    user_manager = UserManager(app, db, User)
