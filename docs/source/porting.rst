=====================
Porting v0.6 to v9.0+
=====================

Ever since Flask-User v0.4, we had plans to improve Flask-User but were held back
by wanting to maintain backwards compatibility.

With Flask-User v1.0 (and its v0.9 alpha/beta) we decided it was time to move forward,
breaking compatibility with v0.6.

Customization underwent a major redesign, so the more you customized
Flask-User v0.6 the more you'll have to change.

Porting non-customized Flask-User v0.6 applications
---------------------------------------------------
When we ported the non-customized Flask-User-demo app, these are the changes we had to make::

    - requirements.txt:
        - Replace: Flask-User==0.6.{X}
             with: Flask-User==0.9.{Y}

    - Flask-User v0.6 leaves py-crypt
        - Run: pip -r requirements.txt

    - application.py (where the app gets initialized):
        - Remove the SQLAlchemyAdaper import
        - Replace: db_adapter = SQLAlchemyAdapter(db, User);
                   user_manager = UserManager(db_adapter, app)
             with: user_manager = UserManager(app, db, User)

    - Entire code base:
        - Replace: confirmed_at = db.Column(db.DateTime())
             with: email_confirmed_at = db.Column('confirmed_at', db.DateTime())
             # This changes the property name, but keeps the old database column name)
        - Replace: confirmed_at
             with: email_confirmed_at
        - Replace: @accept_roles
             with: @roles_required.
        - Replace: .hash_pasword(password)
             with: .password_manager.hash_password(password)

If you upgrade from Flask-Login 2.x to Flask-Login 3.0+, you'll need to::
    - Replace: is_authenticated()   # method
         with: is_authenticated     # propery
    - Replace: is_anonymous()   # method
         with: is_anonymous     # propery
    - Replace: is_active()   # method
         with: is_active     # propery


Issues
------
::

    Python 2.7, SECRET_KEY = '\xb9\x8d\xb5\xc2\xc4Q\xe7\x8ej\xe0\x05\xf3\xa3kp\x99l\xe7\xf2i\x00\xb1-\xcd'
    token_manager.py", line 49: key = flask_secret_key.encode()
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xb9 in position 0: ordinal not in range(128)







This page describes describes the changes required to make a Flask-User v0.6 application
work with Flask-User v0.9+.

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

Flask-User v0.9+::

    from flask_sqlalchemy import SQLAlchemy
    from flask_user import UserManager    # No need for SQLAlchemyAdapter

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User, UserEmailClass=UserEmail)

The `db`  parameter can be any Database instance (for example `SQLAlchemy()` or a `MongoEngine()`) and the
appropriate DbAdapter will be configured internally.

Configuration settings changes
------------------------------
We split ``USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST`` into ``USER_SHOW_USERNAME_DOES_NOT_EXIST``
and ``USER_SHOW_EMAIL_DOES_NOT_EXIST`` and set the default to False for increased security.

We renamed ``USER_REQUIRE_RETYPE_PASSWORD`` to ``USER_REQUIRE_RETYPE_PASSWORD`` to better reflect what this setting does.

Flask-User v0.6::

    USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST = True

    USER_REQUIRE_RETYPE_PASSWORD = True

Flask-User v0.9+::

    USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False

    USER_REQUIRE_RETYPE_PASSWORD = True


Data-model changes
------------------
The `confirmed_at` property name has been renamed to `email_confirmed_at` to better reflect what this property means.

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

Flask-User v0.9+ (keeping the original database column names)::

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

Database table names
--------------------
Table names have been renamed to plural to reflect standard SQL practices::

    def class User(db.Model, UserMixin):
        __tablename__ = 'users'

    def class Role(db.Model):
        __tablename__ = 'roles'

    def class UserEmail(db.Model):
        __tablename__ = 'user_emails'

    def class UserInvitation(db.Model):
        __tablename__ = 'user_invitations'

Foreign keys must be updated accordingly::

    'user.id' --> 'users.id'
    'role.id' --> 'roles.id'

Flask-Login v0.3+ required
--------------------------
Since Flask-Login v0.3.0, ``is_authenticated()``, ``is_active()``, and ``is_anonymous()``
**methods** have been replaced by ``is_authenticated``, ``is_active``, and ``is_anonymous`` **properties**.


PasswordManager() changes
-------------------------
Password related methods have been moved from the UserManager class to a separate PasswordManager class,
accessible through the UserManager.password_manager property.

We changed the ``verify_password()`` parameters to receive a ``hashed_password` parameter
instead of the ``user`` parameter.

Flask-User v0.6::

    verify_password(password, user)

Flask-User v0.9+::

    password_manager.verify_password(password, hashed_password)


EmailManager() changes
----------------------
Email related methods have been moved from the UserManager class to a separate EmailManager class,
accessible through the UserManager.email_manager property.

Introducing EmailMailers
------------------------
Flask-User v0.6 only supported sending emails through SMTP.

With v0.9+ we introduced multiple EmailMailer classes that can send Email via SMTP, ``sendmail``,
SendGrid and custom EmailMailers.

The v0.6 ``MAIL_DEFAULT_SENDER`` config setting has been replaced with the v0.9+ ``FLASK_USER_EMAIL_SENDER_EMAIL``,
and ``FLASK_USER_EMAIL_SENDER_NAME`` settings.

Flask-User v0.6::

    MAIL_DEFAULT_SENDER = '"App name" <info@example.com>'

Flask-User v0.9+::

    FLASK_USER_EMAIL_SENDER_EMAIL = 'info@example.com'    # Required for sending Emails
    FLASK_USER_EMAIL_SENDER_NAME = 'App name'   # Optional


TokenManager() changes
----------------------
The v0.6 `token_manager.generate_token()` assumed that IDs were limited to 16 digits.
This limitation has been removed in v0.9+, to support Mongo ObjectIDs.

In v0.9+, we added the last 8 bytes of the hashed passwords to `token_manager.generate_token()`
to invalidate tokens when a user changes their password.

As a result, the generated tokens are different, which will affect two areas:

- v0.6 user-session tokens, that were stored in a browser cookie, are no longer valid in v0.9+
  and the user will be required to login again.

- v0.6 password-reset tokens, that were sent in password reset emails, are no longer valid in v0.9+
  and the user will have to issue a new forgot-password email request.
  This effect is mitigated by the fact that these tokens are meant to expire relatively quickly.

- user-session tokens and password-reset tokens become invalid if the user changes their password.

UserAuth class
--------------

The optional v0.6 UserAuth class has been fully obsoleted in v0.9+ to simplify the Flask-User source code.

If you are using SQLAlchemy and choose to separate the uer authorization fields
from the user profile fields, you can use the workaround recipe below::


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
