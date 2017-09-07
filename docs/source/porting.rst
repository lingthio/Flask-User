Porting v0.6 to v9.0+
=====================

Ever since Flask-User v0.4, we had plans to improve Flask-User but were held back
by our desire to maintain backwards compatibility for a while.

With Flask-User v1.0 (and its v0.9 alpha/beta) we decided it was time to move forward,
breaking compatibility with v0.6.

Porting non-customized Flask-User v0.6 applications
---------------------------------------------------
The porting of non-customized Flask-User v0.6 applications is a relative straightforward process.

Update your requirements.txt file::

    # From:
    Flask-User==0.6.{X}

    # To:
    Flask-User==0.9.{Y}

Make sure to uninstall py-crypt and install bcrypt::

    pip uninstall py-crypt    # This may already be absent
    pip install bcrypt        # This may already be installed

Update your application initialization code::

    # from v0.6
    # ---------
    from flask_user import UserManager, UserMixin, SQLAlchemyAdapter
        ...
    db_adapter = SQLAlchemyAdaper(db, User)
    user_manager = UserManager(db_adapter, app)


    # to v0.9
    # -------
    from flask_user import UserManager, UserMixin
        ...
    user_manager = UserManager(app, db, User)

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

BTW: Old Flask-User examples showed a deprecated field called ``reset_password_token``.
You may as well take the time now to remove these fields from the data-models and
database tables.

Resolve deprecation warnings (optional but recommended)::

    - Replace: USER_ENABLE_RETYPE_PASSWORD
         with: USER_REQUIRE_RETYPE_PASSWORD

    - Replace: USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL
         with: USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL

    - Replace: USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST
         with: USER_SHOW_USERNAME_DOES_NOT_EXIST and USER_SHOW_EMAIL_DOES_NOT_EXIST

    - Replace: MAIL_DEFAULT_SENDER = '"App name" <info@example.com>'
         with: USER_EMAIL_SENDER_NAME = 'App name'
               USER_EMAIL_SENDER_EMAIL = 'info@example.com'

    - Replace: .verify_password(password, user)
         with: .verify_password(password, user.password)

    - Replace: @accept_roles
         with: @roles_required


Porting customized Flask-User v0.6 applications
-----------------------------------------------
See :ref:`Porting2`.
