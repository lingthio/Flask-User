Flask-User API
==============

- :ref:`UserManager`
- :ref:`EMailManager`
- :ref:`TokenManager`
- :ref:`DbAdapter`
- :ref:`EmailMailer`

.. define a newline macro
.. |br| raw:: html

    <br/>

--------

.. _UserManager:

UserManager class
-----------------

This class implements most of Flask-User's functionality.

Flask-User can be customized by implementing the ``customize()`` method.

.. autoclass:: flask_user.user_manager.UserManager
    :no-undoc-members:

--------

.. _EmailManager:

EmailManager class
------------------

This class manages the sending of Flask-User emails.

.. autoclass:: flask_user.email_manager.EmailManager

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

--------

.. _DbAdapter:

DbAdapter interface
-------------------

The DbAdapter class defines an interface to find, add, update and remove
persistent database objects
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`DbAdapterForSQLAlchemy`
- :ref:`DbAdapterForMongoAlchemy`

Other databases can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.db_adapters.db_adapter.DbAdapter

--------

.. _EmailMailer:

EmailMailer interface
----------------------
The EmailMailer class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`EmailMailerForFlaskMail`
- :ref:`EmailMailerForFlaskSendmail`
- :ref:`EmailMailerForSendgrid`

Other email mailers can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.email_mailers.email_mailer.EmailMailer

