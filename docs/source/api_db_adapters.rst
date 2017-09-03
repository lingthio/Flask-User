.. _DbAdapters:

DbAdapter interface
===================

The DbAdapter class defines an interface to find, add, update and remove
persistent database objects
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`SQLAlchemyDbAdapter`
- :ref:`MongoEngineDbAdapter`

Other databases can be supported by writing your own :ref:`CustomDbAdapter`.

.. autoclass:: flask_user.db_adapters.db_adapter.DbAdapter

--------

.. _SQLAlchemyDbAdapter:

SQLAlchemyDbAdapter
-------------------

.. autoclass:: flask_user.db_adapters.sqlalchemy_db_adapter.SQLAlchemyDbAdapter

Flask-User ships with SQLAlchemyDbAdapter and installs Flask-SQLAlchemy.

Simply supply a SQLAlchemy instance as the ``db`` parameter of UserManager()::

    db = SQLAlchemy(app)
    user_manager = UserManager(app, db, User)

--------

.. _MongoEngineDbAdapter:

MongoEngineDbAdapter
---------------------

.. autoclass:: flask_user.db_adapters.mongoengine_db_adapter.MongoEngineDbAdapter

Flask-User ships with MongoEngineDbAdapter, but you will need
to manually install Flask-MongoEngine::

    pip install Flask-MongoEngine

and supply a MongoEngine instance as the ``db`` parameter of UserManager()::

    from flask_mongoengine import MongoEngine
    db = MongoEngine(app)
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
