Flask-User API
==============

- UserManager_
- DbAdapter_
- EmailAdapter_
- TokenManager_

.. define a newline macro
.. |br| raw:: html

    <br/>

--------

.. _UserManager:

UserManager
-----------

This is the main class that implements most of Flask-User's functionality.

Flask-User can be customized by extending methods such as the ``customize()`` method

.. autoclass:: flask_user.user_manager.UserManager
    :members:
    :inherited-members:
    :undoc-members:

--------

.. _DbAdapter:

DbAdapter interface
-------------------

The DbAdapter class defines an interface to find, add, update and remove
persistent database objects
while shielding the Flask-User code from the underlying implementation.

The :ref:`SQLAlchemyDbAdapter` class implements this interface for Flask-SQLAlchemy.

The :ref:`MongoAlchemyDbAdapter` class implements this interface for Flask-MongoAlchemy.

Other databases can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.db_adapters.db_adapter.DbAdapter
    :members:
    :inherited-members:
    :undoc-members:

--------

.. _EmailAdapter:

EmailAdapter interface
----------------------
The EmailAdapter class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

The :ref:`FlaskMailEmailAdapter` class implements this interface for Flask-Mail.

The :ref:`FlaskSendmailEmailAdapter` class implements this interface for Flask-Sendmail.

Other email mailers can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.email_adapters.email_adapter.EmailAdapter
    :members:
    :inherited-members:
    :undoc-members:

--------

.. _TokenManager:

TokenManager
------------

The TokenManager generates and verifies timestamped, signed and encrypted tokens.

These tokens are used in the following places:

* To securely store User IDs in the browser session cookie.
* To provide secure tokens in email-confirmation emails.
* To provide secure tokens in reset-password emails.

.. autoclass:: flask_user.managers.token_manager.TokenManager
    :members:
    :inherited-members:
    :undoc-members:
