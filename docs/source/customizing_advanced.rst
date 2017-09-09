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

.. _CustomDbAdapters:

Custom DbAdapters
=================

Flask-User uses DbAdapters to manage user records in various databases.

Flask-User ships with the following DbAdapters:

- ``SQLDbAdapter()`` for SQL databases using SQLAlchemy
- ``MongoDbAdapter()`` for MongoDB database using MongoEngine

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

Here's the `SQLDbAdapter() implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/db_adapters/sql_db_adapter.py>`_.


.. _CustomEmailMailers:

Custom EmailMailers
===================

Flask-User uses EmailMailers to send email via various methods.

Flask-User ships with the following EmailMailers:

- ``SMTPEmailMailer()`` for sending email via SMTP.
- ``SendmailEmailMailer()`` for sending email via ``sendmail``.
- ``SendgridEmailMailer()`` for sending email via SendGrid.

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

Here's the `SMTPEmailMailer() implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/email_mailers/smtp_email_mailer.py>`_.


--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
