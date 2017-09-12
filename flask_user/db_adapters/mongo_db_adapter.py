"""This module implements the DbAdapter interface for MongoEngine.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user.db_adapters import DbAdapterInterface


class MongoDbAdapter(DbAdapterInterface):
    """ Implements the DbAdapter interface to find, add, update and delete
    database objects using Flask-MongoEngine.
    """

    def __init__(self, app, db):
        """Args:
            app(Flask): The Flask appliation instance.
            db(MongoEngine): The MongoEngine object-database mapper instance.

        | Example:
        |    app = Flask(__name__)
        |    db = MongoEngine()
        |    db_adapter = MongoDbAdapter(app, db)
        """
        # This no-op method is defined to show it in Sphinx docs in order 'bysource'
        super(MongoDbAdapter, self).__init__(app, db)

    def add_object(self, object):
        """Add object to db session. Only for session-centric object-database mappers."""
        object.save()

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        try:
            object = ObjectClass.objects.get(id=id)
        except (ObjectClass.DoesNotExist, ObjectClass.MultipleObjectsReturned):
            object = None
        return object

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        # Retrieve all matching objects
        return ObjectClass.objects(**kwargs).all()

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.

        ``find_first_object(User, username='myname')`` translates to
        ``User.query.filter(User.username=='myname').first()``.
        """

        # Retrieve first object
        return ObjectClass.objects(**kwargs).first()

    def save_object(self, object, **kwargs):
        """ Save object. Only for non-session centric Object-Database Mappers."""
        object.save()

    def delete_object(self, object):
        """ Delete object specified by ``object``. """
        object.delete()

    def commit(self):
        """This method does nothing for MongoDbAdapter.
        """
        pass


    # Database management methods
    # ---------------------------

    def create_all_tables(self):
        """This method does nothing for MongoDbAdapter."""
        pass

    def drop_all_tables(self):
        """Drop all document collections of the database.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """

        # Retrieve database name from application config
        app = self.db.app
        mongo_settings = app.config['MONGODB_SETTINGS']
        database_name = mongo_settings['db']

        # Flask-MongoEngine is built on MongoEngine, which is built on PyMongo.
        # To drop database collections, we need to access the PyMongo Database object,
        # which is stored in the PyMongo MongoClient object,
        # which is stored in app.extensions['mongoengine'][self]['conn']
        py_mongo_mongo_client = app.extensions['mongoengine'][self.db]['conn']
        py_mongo_database = py_mongo_mongo_client[database_name]

        # Use the PyMongo Database object
        for collection_name in py_mongo_database.collection_names():
            py_mongo_database.drop_collection(collection_name)
