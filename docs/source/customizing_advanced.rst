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
        ...

    # Customize the PasswordManager
    from flask_user import PasswordManager
    class CustomPasswordManager(PasswordManager):
        ...

    # Customize the TokenManager
    from flask_user import TokenManager
    class CustomTokenManager(TokenManager):
        ...

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Customize Flask-User managers
    user_manager.email_manager = CustomEmailManager(app)
    user_manager.password_manager = CustomPasswordManager(app, 'bcrypt')
    user_manager.token_manager = CustomTokenManager(app)

.. seealso::

    | :ref:`EmailManager`,
    | :ref:`PasswordManager`, and
    | :ref:`TokenManager`.

--------

Implementing a CustomDbAdapter
------------------------------

--------

See :ref:`CustomDbAdapters`

Implementing a CustomEmailAdapter
---------------------------------

See :ref:`CustomEmailAdapters`

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
