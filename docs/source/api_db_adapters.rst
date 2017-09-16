.. _DbAdapterInterface:

DbAdapter Interface
===================

The DbAdapterInterface class defines an interface to find, add, update and remove
persistent database objects,
while shielding the Flask-User code from the underlying implementation.

.. autoclass:: flask_user.db_adapters.db_adapter_interface.DbAdapterInterface
    :special-members: __init__

.. _CustomDbAdapters:

Implementing a CustomDbAdapter
------------------------------
You can write you own DbAdapter implementation by defining a CustomDbAdapter class
and configure Flask-User to use this class like so::

    # Define a CustomDbAdapter
    from flask_user.db_adapters import DbAdapterInterface
    class CustomDbAdapter(DbAdapterInterface):
        ...

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Customize Flask-User
    user_manager.db_adapter = CustomDbAdapter(app)

For an example, see `the SQLDbAdapter() implementation <https://github.com/lingthio/Flask-User/blob/master/flask_user/db_adapters/sql_db_adapter.py>`_.
