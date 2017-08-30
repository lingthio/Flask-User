Flask-User API
==============

- UserManager_
- DbAdapter_
- TokenManager_

.. define a newline macro
.. |br| raw:: html

    <br/>

--------

.. _UserManager:

UserManager
-----------

This is the main class that implements most of Flask-User's functionality.

Flask-User can be customized by extending methods such as the ``customize()`` method::

    # Setup Flask
    app = Flask(__name__)

    # Setup SQLAlchemy
    db = SQLAlchemy(app)

    # Customize Flask-User
    class MyCustomFlaskUser(FlaskUser):
        def customize():
            # Add customization here
            self.token_manager = MyJwtTokenManager()
            self.email_manager = MySendGridEmailManager()

    # Setup Flask-User
    user_manager = MyCustomFlaskUser(app, db, User)

.. autoclass:: flask_user.user_manager.UserManager
    :members:
    :inherited-members:
    :undoc-members:

--------

.. _DbAdapter:

DbAdapter
---------

The DbAdapter class defines an interface to find, add, update and remove persistent
database objects while shielding the Flask-User code from the underlying implementation.

The :ref:`SQLAlchemyDbAdapter` class implements the DbAdapter interface for SQLAlchemy.

The :ref:`MongoAlchemyDbAdapter` class implements the DbAdapter interface for MongoAlchemy.

Other databases can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.db_adapters.db_adapter.DbAdapter
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
