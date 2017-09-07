.. _DbAdapterInterface:

DbAdapter Interface
===================

The DbAdapterInterface class defines an interface to find, add, update and remove
persistent database objects,
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`SQLAlchemyDbAdapter`
- :ref:`MongoEngineDbAdapter`

.. autoclass:: flask_user.db_adapters.db_adapter_interface.DbAdapterInterface

--------

.. _SQLAlchemyDbAdapter:

SQLAlchemyDbAdapter
-------------------

.. autoclass:: flask_user.db_adapters.sqlalchemy_db_adapter.SQLAlchemyDbAdapter

--------

.. _MongoEngineDbAdapter:

MongoEngineDbAdapter
---------------------

.. autoclass:: flask_user.db_adapters.mongoengine_db_adapter.MongoEngineDbAdapter


