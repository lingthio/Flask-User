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
When we ported non-customized Flask-User apps, these are the changes we had to make::

    - requirements.txt:
        - Replace: Flask-User==0.6.{X}
             with: Flask-User==0.9.{Y}
        - pip uninstall py-crypt    # Left behind by some older Flask-User installs
        - Run: pip -r requirements.txt

    - application.py (where the app gets initialized):
        - Remove the SQLAlchemyAdaper import
        - Replace: db_adapter = SQLAlchemyAdapter(db, User)
                   user_manager = UserManager(db_adapter, app)
             with: user_manager = UserManager(app, db, User)

    - Entire code base:
        - Replace: USER_ENABLE_RETYPE_PASSWORD
             with: USER_REQUIRE_RETYPE_PASSWORD
        - Replace: confirmed_at = db.Column(db.DateTime())
             with: email_confirmed_at = db.Column('confirmed_at', db.DateTime())
                   # This changes the property name, but keeps the old database column name)
        - Replace: confirmed_at
             with: email_confirmed_at (or use getters and setters to alias this field)
        - Replace: @accept_roles
             with: @roles_required.
        - Replace: .hash_pasword(password)
             with: .password_manager.hash_password(password)


Complete list of incompatible changes
=====================================

Configuration settings changes
------------------------------
We renamed ``USER_ENABLE_RETYPE_PASSWORD`` to ``USER_REQUIRE_RETYPE_PASSWORD`` to better reflect what this setting does.

We split ``USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST`` into ``USER_SHOW_USERNAME_DOES_NOT_EXIST``
and ``USER_SHOW_EMAIL_DOES_NOT_EXIST`` and set the default to False for increased security --
Hackers won't be able to differentiate between an invalid password event
or a non-existing email/username event.

Flask-User v0.6::

    USER_ENABLE_RETYPE_PASSWORD = True

    USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST = True


Flask-User v0.9+::

    USER_REQUIRE_RETYPE_PASSWORD = True

    USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False


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


UserManager customization
-------------------------
Flask-User customization now happens by extending a CustomUserManager class from UserManager,
and by overriding some properties and methods:

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():
            # override some properties
                ....

        # Override a method
        def some_custom_method():
            ....

If your code passes custom parameters to the UserManager() instantiation,
you'll have to move some code around to conform to the new way of customization.

The only parameters allowed in v0.9+ are:

    - app
    - db
    - UserClass
    - UserEmailClass    # Optional
    - UserInvitationClass    # Optional

Data-model changes
------------------
The `confirmed_at` property name has been renamed to `email_confirmed_at` to better reflect what this property means.
Remember that you can change the property name and keep the old column name like so::

    # Map 'email_confirmed_at' property to 'confirmed_at' column
    email_confirmed_at = db.Column('confirmed_at', db.DateTime())

The optional UserAuth class has been obsoleted. See below for a workaround.

The UserInvite class name has been renamed to UserInvitation.

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


If you move from Flask-Login v0.2 to v0.3+
------------------------------------------
Since Flask-Login v0.3.0:
- the ``is_authenticated``, ``is_active``, and ``is_anonymous`` **properties**
- have replaced the ``is_authenticated()``, ``is_active()``, and ``is_anonymous()`` **methods**.


PasswordManager() changes
-------------------------
Password related methods have been moved from the UserManager class to a separate PasswordManager class,
accessible through the UserManager.password_manager property.

We changed the ``verify_password()`` parameters to receive a ``hashed_password` parameter
instead of the ``user`` parameter to keep the PasswordManager unaware of User objects.

Flask-User v0.6::

    user_manager.hash_password(password)
    user_manager.verify_password(password, user)

Flask-User v0.9+::

    user_manager.password_manager.hash_password(password)
    user_manager.password_manager.verify_password(password, user.password)


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
