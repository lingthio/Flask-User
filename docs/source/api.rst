Flask-User API
==============

- :ref:`UserManagerClass`
- :ref:`UserManager__Settings`
- :ref:`UserManager__Utils`
- :ref:`UserManager__Views`
- :ref:`ViewDecorators`
- :ref:`FlaskUserForms`
- :ref:`DBManager`
- :ref:`EMailManager`
- :ref:`PasswordManager`
- :ref:`TokenManager`
- :ref:`DbAdapterInterface`
- :ref:`EmailAdapterInterface`

--------

.. _DBManager:

DBManager class
---------------

This class manages database objects.

.. autoclass:: flask_user.db_manager.DBManager

--------

.. _EmailManager:

EmailManager class
------------------

This class manages the sending of Flask-User emails.

.. autoclass:: flask_user.email_manager.EmailManager

.. seealso:: :ref:`Customizing the EmailManager <CustomizingManagers>`.

--------

.. _PasswordManager:

PasswordManager class
---------------------

The PasswordManager generates and verifies hashed passwords.

.. autoclass:: flask_user.password_manager.PasswordManager
    :no-undoc-members:

.. seealso:: :ref:`Customizing the PasswordManager <CustomizingManagers>`.

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

.. seealso:: :ref:`Customizing the TokenManager <CustomizingManagers>`.
