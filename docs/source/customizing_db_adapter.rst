.. _CustomizingDbAdapter:

Customizing the DbAdapter
=========================

Flask-User uses DbAdapters to manage user records in various databases.

Flask-User ships with the following DbAdapters:

- :ref:`CustomizingSQLAlchemyDbAdapter` for various SQL databases.
- :ref:`CustomizingMongoEngineDbAdapter` for MongoDB databases.

and developers can define their own:

- :ref:`CustomDbAdapter`

--------

.. _CustomizingSQLAlchemyDbAdapter:

SQLAlchemyDbAdapter
-------------------
Flask-User uses SQLAlchemyDbAdapter and installs Flask-SQLAlchemy by default.
No customization is required to work with SQL databases.

Configure the ``SQLALCHEMY_DATABASE_URI`` setting in your app config to point to the desired server and database.

--------

.. _CustomizingMongoEngineDbAdapter:

MongoEngineDbAdapter
--------------------
Flask-User ships with a MongoEngineDbAdapter, but Flask-MongoEngine must be installed manually::

    pip install Flask-MongeEngine

and minor customization is required to use and configure the MongoEngineDbAdapter::

    # Setup Flask-MongoEngine
    from Flask-MongoEngine import MongoEngine
    db = MongoEngine(app)

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Use the provided MongoEngineDbAdapter
            from flask_user.db_adapters import MongoEngineDbAdapter
            self.db_adapter = MongoEngineDbAdapter(db)

    # Define the User document
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):

        # User authentication information
        username = db.StringField(default='')
        email = db.StringField(default='')
        password = db.StringField()
        email_confirmed_at = db.DateTimeField(default=None)

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configure the ``MONGODB_SETTINGS`` setting in your app config to point to the desired server and database.

--------

.. _CustomDbAdapter:

Implement a custom DbAdapter
------------------------------

Flask-User allows developers to implement a custom DbAdapter that
conforms to the :ref:`DbAdapterInterface`::

    # Define a custom DbAdapter
    from flask_user.email_mailers import DbAdapter
    class CustomDbAdapter(DbAdapter):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Use the CustomDbAdapter
            self.db_adapter = CustomDbAdapter()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

