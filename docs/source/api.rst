Flask-User API
==============

- :ref:`UserManager`
- :ref:`UserManager__Settings`
- :ref:`EMailManager`
- :ref:`PasswordManager`
- :ref:`TokenManager`
- :ref:`DbAdapters`
- :ref:`EmailMailers`

--------

.. _EmailManager:

EmailManager class
------------------

This class manages the sending of Flask-User emails.

.. autoclass:: flask_user.email_manager.EmailManager

You can customize the default EmailManager like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):

            # Customize EmailManager
            from flask_user.email_manager import EmailManager
            class CustomEmailManager(EmailManager)
                pass
            
            # Configure custom EmailManager
            self.email_manager = CustomEmailManager()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. _PasswordManager:

PasswordManager class
---------------------

The PasswordManager generates and verifies hashed passwords.

.. autoclass:: flask_user.password_manager.PasswordManager
    :no-undoc-members:

You can customize the default PasswordManager like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Customize PasswordManager
            from flask_user.password_manager import PasswordManager
            class CustomPasswordManager(PasswordManager)
                pass
            
            # Configure custom PasswordManager
            self.password_manager = CustomPasswordManager()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. _TokenManager:

TokenManager class
------------------

The TokenManager generates and verifies timestamped, signed and encrypted tokens.

These tokens are used in the following places:

* To securely store User IDs in the browser session cookie.
* To provide secure tokens in email-confirmation emails.
* To provide secure tokens in reset-password emails.

.. autoclass:: flask_user.token_manager.TokenManager
    :no-undoc-members:

You can customize the default TokenManager like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Customize TokenManager
            from flask_user.token_manager import TokenManager
            class CustomTokenManager(TokenManager)
                pass
            
            # Configure custom TokenManager
            self.token_manager = CustomTokenManager()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)
