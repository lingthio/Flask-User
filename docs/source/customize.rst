Customize
=========

Flask-User is designed to be **largely configurable**,

- :ref:`ConfigureSettings`

and **almost fully customizable**.

- :ref:`CustomizeFormsAndViews`
- :ref:`CustomizeManagers`

.. _CustomizeFormsAndViews:

Customizing forms and view methods
----------------------------------

Custom settings, forms and view methods can be configured as follows::

    # Customize a form:
    from flask_user.user_manager_forms import LoginForm
    class CustomLoginForm(LoginForm):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):

            # Customize a form
            self.login_form = CustomLoginForm()

        # customize a view function
        def login_view_function(self):
            pass

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    | :ref:`UserManager__Forms` for a complete list of customizable forms.
    | :ref:`UserManager__Views` for a complete list of customizable view methods.


-------

.. _CustomizeManagers:

Customizing EmailManager, PasswordManager and TokenManager
----------------------------------------------------------

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





