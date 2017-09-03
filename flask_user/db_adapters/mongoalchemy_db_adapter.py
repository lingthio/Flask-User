from __future__ import print_function

from .sqlalchemy_db_adapter import SQLAlchemyDbAdapter

from flask import current_app

class MongoAlchemyDbAdapter(SQLAlchemyDbAdapter):
    """ Implements the DbAdapter interface to find, add, update and delete
    database objects using Flask-MongoAlchemy.
    """

    # Since MongoAlchemy is similar to SQLAlchemy, we extend
    # MongoAlchemyDbAdapter from SQLAlchemyDbAdapter
    # and re-use most of its methods.

    def __init__(self, db):
        """Args:
            db(MongoAlchemy): The MongoAlchemy object-database mapper instance.

        | Example:
        |    db = MongoAlchemy()
        |    db_adapter = MongoAlchemyDbAdapter(db)

        .. note::

            Object-class agnostic methods.
        """
        # This no-op method is defined only for Sphinx autodocs 'bysource' order
        super(MongoAlchemyDbAdapter, self).__init__(db)

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``."""

        # Translate Flask-User integer ID to MongoDB ObjectID
        hex_id = format(id, 'x')
        return ObjectClass.query.get(hex_id)

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        # This no-op method is defined only for Sphinx autodocs 'bysource' order
        return super(MongoAlchemyDbAdapter, self).find_objects(ObjectClass, **kwargs)

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.

        ``find_first_object(User, username='myname')`` translates to
        ``User.query.filter(User.username=='myname').first()``.
        """

        # This no-op method is defined only for Sphinx autodocs 'bysource' order
        return super(MongoAlchemyDbAdapter, self).find_first_object(ObjectClass, **kwargs)

    def ifind_first_object(self, ObjectClass, **kwargs):
        """Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case insensitive.
        """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("BaseAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter({ field : {"$regex": field_value, "$options": 'i'} })  # case INsensitive!!

        # Execute query
        return query.first()

    def add_object(self, ObjectClass, **kwargs):
        """Add a new object of type ``ObjectClass``,
        with fields and values specified in ``**kwargs``.
        """

        # This no-op method is defined only for Sphinx autodocs 'bysource' order
        return super(MongoAlchemyDbAdapter, self).add_object(ObjectClass, **kwargs)

    def update_object(self, object, **kwargs):
        """ Update an existing object, specified by ``object``,
        with the fields and values specified in ``**kwargs``.
        """
        super(MongoAlchemyDbAdapter, self).update_object(object, **kwargs)
        # Save changes to DB
        object.save()

    def delete_object(self, object):
        """ Delete object specified by ``object``. """
        self.db.session.remove(object)

    def commit(self):
        """Flush modified objects in the database session.

        .. note::

            User-class specific utility methods.
        """
        self.db.session.flush()

    def add_user_role(self, user, role_name, RoleClass=None):
        """ Add a ``role_name`` role to ``user``."""
        user.roles.append(role_name)
        user.save()

    def get_user_roles(self, user):
        """ Retrieve a list of user role names.

        .. note::

            Database specific utility methods.
        """
        return user.roles

    def create_all_tables(self):
        """This method does nothing, since document collections are created on first object operation."""
        pass

    def drop_all_tables(self):
        """Drop all document collections of the database.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        database_name = self.db.session.db._Database_name.database.name
        self.db.session.db.connection.drop_database(database_name)