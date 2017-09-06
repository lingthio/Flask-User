Flask-User Customization
========================

Flask-User is designed to be **largely configurable** and **almost fully customizable**.

- :ref:`ConfiguringSettings`
- :ref:`CustomizingForms`
- :ref:`CustomizingValidators`
- :ref:`CustomizingManagers`
- :ref:`CustomizingDbAdapter`
- :ref:`CustomizingEmailMailer`

.. _CustomizingManagers:

Customizing the EmailManager, PasswordManager or TokenManager
-------------------------------------------------------------

Developers can customize the EmailManager PasswordManager and TokenManager as follows::

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





