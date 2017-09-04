Flask-User Customization
========================

Flask-User is designed to be **largely configurable** and **almost fully customizable**.

- :ref:`ConfiguringSettings`
- :ref:`CustomizingForms`
- :ref:`CustomizingValidators`
- :ref:`CustomizingDbAdapter`
- :ref:`CustomizingEmailMailer`
- :ref:`CustomizingManagers`

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

        def customize(self):

            # Customize Flask-User managers
            self.email_manager = CustomEmailManager()
            self.password_manager = CustomPasswordManager('bcrypt')
            self.token_manager = CustomTokenManager(app.config['SECRET_KEY'])

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    | :ref:`EmailManager`,
    | :ref:`PasswordManager`, and
    | :ref:`TokenManager`.





