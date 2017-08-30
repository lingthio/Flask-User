from __future__ import print_function

from .db_adapter import DbAdapter

class MongoAlchemyDbAdapter(DbAdapter):
    """ Shield code from MongoAlchemy specific ORM calls."""

    # Some methods are defined in the DbAdapter base class.

    def __init__(self, db):
        """Specify the MongoAlchemy instance ``db``.

        | Examples:
        |    db = MongoAlchemy()
        |    db_adapter = MongoAlchemyDbAdapter(db)
        """
        super(MongoAlchemyDbAdapter, self).__init__(db)

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``."""

        # Translate Flask-User integer ID to MongoDB ObjectID
        hex_id = format(id, 'x')
        return ObjectClass.query.get(hex_id)

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case insensitive. """

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

    def update_object(self, object, **kwargs):
        """ Update an existing object, specified by ``object``,
        with the fields and values specified in ``**kwargs``. """
        super(MongoAlchemyDbAdapter, self).update_object(object, **kwargs)
        # Save changes to DB
        object.save()

    def delete_object(self, object):
        """ Delete object specified by ``object``. """
        self.db.session.remove(object)

    def commit(self):
        """Flush modified objects in the database session."""
        self.db.session.flush()
