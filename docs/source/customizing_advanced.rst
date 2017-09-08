Advanced Customizations
=======================
.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst

--------

.. _CustomizingManagers:

Customizing the Email, Password and Token Managers
--------------------------------------------------

Developers can customize the EmailManager, the PasswordManager, and the TokenManager as follows::

    # Customize the EmailManager
    from flask_user import EmailManager
    class CustomEmailManager(EmailManager):
        pass

    # Customize the PasswordManager
    from flask_user import PasswordManager
    class CustomPasswordManager(PasswordManager):
        pass

    # Customize the TokenManager
    from flask_user import TokenManager
    class CustomTokenManager(TokenManager):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):

            # Customize Flask-User managers
            self.email_manager = CustomEmailManager(app)
            self.password_manager = CustomPasswordManager(app, 'bcrypt')
            self.token_manager = CustomTokenManager(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    | :ref:`EmailManager`,
    | :ref:`PasswordManager`, and
    | :ref:`TokenManager`.

.. _CustomizingDbAdapters:

Customizing DbAdapters
======================

Flask-User uses DbAdapters to manage user records in various databases.

Flask-User ships with the following DbAdapters:

- :ref:`CustomizingSQLDbAdapter` for various SQL databases.
- :ref:`CustomizingMongoDbAdapter` for MongoDB databases.

and developers can define their own:

- :ref:`CustomDbAdapter`

--------

.. _CustomizingSQLDbAdapter:

SQLDbAdapter
-------------------
Flask-User uses SQLDbAdapter and installs Flask-SQLAlchemy by default.
No customization is required to work with SQL databases.

Configure the ``SQLALCHEMY_DATABASE_URI`` setting in your app config to point to the desired server and database.

--------

.. _CustomizingMongoDbAdapter:

MongoDbAdapter
--------------------
Flask-User ships with a MongoDbAdapter, but Flask-MongoEngine must be installed manually::

    pip install Flask-MongeEngine

and minor customization is required to use and configure the MongoDbAdapter::

    # Setup Flask-MongoEngine
    from Flask-MongoEngine import MongoEngine
    db = MongoEngine(app)

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided MongoDbAdapter
            from flask_user.db_adapters import MongoDbAdapter
            self.db_adapter = MongoDbAdapter(app, db)

    # Define the User document
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):

        # User authentication information
        username = db.StringField(default='')
        email = db.StringField(default='')
        password = db.StringField()
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configure the ``MONGODB_SETTINGS`` setting in your app config to point to the desired server and database.

--------

.. _CustomDbAdapter:

Implement a custom DbAdapter
------------------------------

Flask-User allows developers to implement a custom DbAdapter that
conforms to the :ref:`DbAdapterInterface`::

    # Define a custom DbAdapter
    from flask_user.email_mailers import DbAdapter
    class CustomDbAdapter(DbAdapter):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the CustomDbAdapter
            self.db_adapter = CustomDbAdapter(app, db)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. _CustomizingEmailMailers:

Customizing the EmailMailer
===========================

Flask-User uses EmailMailers to send email via various methods.

Flask-User ships with the following EmailMailers:

- :ref:`CustomizingSMTPEmailMailer` for sending email via SMTP.
- :ref:`CustomizingSendmailEmailMailer` for sending email via ``sendmail``.
- :ref:`CustomizingSendgridEmailMailer` for sending email via SendGrid.

and developers can define their own:

- :ref:`CustomEmailMailer`.

--------

.. _CustomizingSMTPEmailMailer:

SMTPEmailMailer
---------------
Flask-User uses the SMTPEmailMailer and install Flask-Mail by default.
No customization is required to use SMTPEmailMailer to send emails via SMTP.

Configure the ``MAIL_...`` settings in your app config to point to the desired SMTP server and account.

--------

.. _CustomizingSendmailEmailMailer:

SendmailEmailMailer
-------------------
Flask-User ships with a SendmailEmailMailer, but Flask-Sendmail must be installed manually::

    pip install Flask-Sendmail

and minor customization is required use to SendmailEmailMailer to send emails via ``sendmail``.::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided SendmailEmailMailer
            from flask_user.email_mailers import SendmailEmailMailer
            self.email_mailer = SendmailEmailMailer(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

No configuration is required (other than setting up sendmail on your system).

---------

.. _CustomizingSendgridEmailMailer:

SendgridEmailMailer
-------------------
Flask-User ships with a SendgridEmailMailer, but sendgrid-python needs to be installed manually::

    pip install sendgrid

and minor customization is required to use SendgridEmailMailer to send emais via SendGrid::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the provided SendgridEmailMailer
            from flask_user.email_mailers import SendgridEmailMailer
            self.email_mailer = SendgridEmailMailer(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configuration: TBD.

--------

.. _CustomEmailMailer:

Implement a custom EmailMailer
------------------------------

Flask-User allows developers to implement a custom EmailMailer that
conforms to the :ref:`EmailMailerInterface`::

    # Define a custom EmailMailer
    from flask_user.email_mailers import EmailMailer
    class CustomEmailMailer(EmailMailer):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the CustomEmailMailer
            self.email_mailer = CustomEmailMailer(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
