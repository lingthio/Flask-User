.. _DbAdapterInterface:

DbAdapter Interface
===================

The DbAdapterInterface class defines an interface to find, add, update and remove
persistent database objects,
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`SQLDbAdapter`
- :ref:`MongoDbAdapter`

.. autoclass:: flask_user.db_adapters.db_adapter_interface.DbAdapterInterface

--------

.. _SQLDbAdapter:

SQLDbAdapter
-------------------

.. autoclass:: flask_user.db_adapters.sql_db_adapter.SQLDbAdapter

--------

.. _MongoDbAdapter:

MongoDbAdapter
---------------------

.. autoclass:: flask_user.db_adapters.mongodb_db_adapter.MongoDbAdapter


