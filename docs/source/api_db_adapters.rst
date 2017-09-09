.. _DbAdapterInterface:

DbAdapter Interface
===================

The DbAdapterInterface class defines an interface to find, add, update and remove
persistent database objects,
while shielding the Flask-User code from the underlying implementation.

.. autoclass:: flask_user.db_adapters.db_adapter_interface.DbAdapterInterface
    :special-members: __init__

Example implementation
----------------------
Here's the `SQLDbAdapter() implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/db_adapters/sql_db_adapter.py>`_.

Customizing Flask-User
----------------------
::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the CustomDbAdapter
            self.db_adapter = CustomDbAdapter(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

