Advanced Porting topics
=======================
.. include:: includes/submenu_defs.rst
.. include:: includes/porting_submenu.rst

--------

Flask-Login
-----------
We recommend NOT upgrading Flask-Login from v0.2.x to v0.3+ unless you need to.

Flask-Login changed
``user.is_authenticated``, ``user.is_anonymous`` and ``user.is_active``
from being **methods** in v0.2 to being **properties** in v0.3+.

This difference often requires changes in many places (in code and in template files)::

    user.is_authenticated()  -->  user.is_authenticated
    user.is_anonymous()      -->  user.is_anonymous
    user.is_active()         -->  user.is_active


TokenManager() changes
----------------------
The v0.6 TokenManager could only encrypt a single integer ID with less than 16 digits.

The v1.0+ TokenManager can now encrypt a list of items.
Each item can be an integer or a string.
Integers can be of any size.

This change enables us to encrypt Mongo Object IDs as well as the last 8 bytes of a
password, to invalidate tokens after their password changed.

As a result, the generated tokens are different, which will affect these areas:

- v0.6 user-session tokens, that were stored in a browser cookie, are no longer valid in v1.0+
  and the user will be required to login again.

- Unused v0.6 password-reset tokens and user-invitation tokens, are no longer valid in v1.0+
  and the affected users will have to issue new forgot-password emails and new
  user invitatin emails.
  This effect is mitigated by the fact that these tokens are meant to expire relatively quickly.

- user-session tokens and password-reset tokens become invalid if the user changes their password.


Python getters and setters
--------------------------
If you are unable to change property names, you can use Python's
getters and setters to form a bridge between required property names and actual ones.

Here's an example of how to map the v1.0 required ``email_confirmed_at`` property
to your existing ``confirmed_at`` property::

    # If the actual property (confirmed_at) name
    # differs from required name (email_confirmed_at).
    class User(db.Model, UserMixin)
            ...
        # Actual property
        confirmed_at = db.Column(db.DateTime())

        # Map required property name to actual property
        @property
        def email_confirmed_at(self):
            return self.confirmed_at

        @email_confirmed_at.setter
        def email_confirmed_at(self, value):
            self.confirmed_at = value

Supporting deprecated ``UserAuth`` data-models
----------------------------------------------

Because the optional ``UserAuth`` and ``User`` have a one-to-one relationship
to each other, you can use getters and setters to have Flask-User manage two objects
while specifying only the one ``User`` class::

    # This is your existing UserAuth data-model
    # -----------------------------------------
    class UserAuth(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        # Relationship to user
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        user = db.relationship('User', uselist=False)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())


    # This is your existing User data-model
    # -------------------------------------
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User information
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

        # One-to-one Relationship
        user_auth = db.relationship('UserAuth', uselist=False)

        # Create a UserAuth instance when a User instance is created
        def __init__(self, *args, **kwargs):
            super(User, self).__init__(*args, **kwargs)
            self.user_auth = UserAuth(user=self)


        # Map required v1.0 properties in the User data-model
        # to existing properties in the UserAuth data-model.
        # ---------------------------------------------------

        # Map the User.username field into the UserAuth.username field
        @property
        def username(self):
            return self.user_auth.username

        @username.setter
        def username(self, value)
            self.user_auth.username = value


        # Map the User.password field into the UserAuth.password field
        @property
        def password(self):
            return self.user_auth.password

        @password.setter
        def password(self, value)
            self.user_auth.password = value


        # Map the User.email field into the UserAuth.email field
        @property
        def email(self):
            return self.user_auth.email

        @email.setter
        def email(self, value)
            self.user_auth.email = value


        # Map the User.email_confirmed_at field into the UserAuth.confirmed_at field
        @property
        def email_confirmed_at(self):
            return self.user_auth.confirmed_at

        @email_confirmed_at.setter
        def email_confirmed_at(self, value)
            self.user_auth.confirmed_at = value


    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # -----------------------------------------------------------------
    # This code snippet has not yet been tested. You can email
    # ling.thio@gmail.com when it works or when you encounter problems.
    # When enough people tested this I will remove this comment.
    # Thank you!

Logging in without confirmed email addresses
--------------------------------------------
In v0.6, the ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL=True`` setting allowed users to
login regardless of whether their email addresses were confirmed or not. Sensitive
views were protected with an ``@confirm_email_required`` view decorator.
This left websites vulnerable to views that were unintentionally left unprotected.

In v1.0 we renamed the ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL`` to
``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL`` to better reflect what this setting does.
and we deprecated the ``@confirm_email_required`` view decorator.

In v1.0, we reduced the opportunities for mistakes, by taking the **opposite**
protection approach: Even with ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL=True``,
views with ``@login_required``, ``@roles_accepted``, and ``@roles_required decorators``
continue to be protected against users without confirmed email addresses.

If you want unconfirmed users to access certain views, you will need to add the
new ``@allow_unconfirmed_email`` decorator to each view that you choose to expose.

| This decorator **must follow** the @route decorator (as usual)
| THis decorator **must precede** any of the other Flask-Userdecorators

::

    @route(...)
    @allow_unconfirmed_email
    @login_required
    def unprotected_view():
        ...


--------

.. include:: includes/porting_submenu.rst
