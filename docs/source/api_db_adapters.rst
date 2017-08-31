.. _DbAdapters:

DbAdapter interface
===================

The DbAdapter class defines an interface to find, add, update and remove
persistent database objects
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`DbAdapterForSQLAlchemy`
- :ref:`DbAdapterForMongoAlchemy`

Other databases can be supported by writing your own :ref:`CustomDbAdapter`.

.. autoclass:: flask_user.db_adapters.db_adapter.DbAdapter

--------

.. _DbAdapterForSQLAlchemy:

DbAdapterForSQLAlchemy
----------------------

.. autoclass:: flask_user.db_adapters.db_adapter_for_sqlalchemy.DbAdapterForSQLAlchemy
    :member-order: alphabetical

Flask-User ships with DbAdapterForSQLAlchemy and installs Flask-SQLAlchemy.

Simply supply a SQLAlchemy instance as the ``db`` parameter of UserManager()::

    db = SQLAlchemy(app)
    user_manager = UserManager(app, db, User)

--------

.. _DbAdapterForMongoAlchemy:

DbAdapterForMongoAlchemy
------------------------

.. autoclass:: flask_user.db_adapters.db_adapter_for_mongoalchemy.DbAdapterForMongoAlchemy
    :member-order: alphabetical

Flask-User ships with DbAdapterForMongoAlchemy, but you will need
to manually install Flask-MongoAlchemy::

    pip install Flask-MongoAlchemy

and supply a MongoAlchemy instance as the ``db`` parameter of UserManager()::

    db = MongoAlchemy(app)
    user_manager = UserManager(app, db, User)

--------

.. _CustomDbAdapter:

Custom DbAdapter
----------------
If you wrote you own custom DbAdapter, you can customize Flask-User like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure custom DbAdapter
            from some.path import CustomDbAdapter
            self.db_adapter = CustomDbAdapter(db)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)
