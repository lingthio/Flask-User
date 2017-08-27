""" This file shields Flask-User code from database/ORM specific functions.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from __future__ import print_function

from .db_adapter import DbAdapter

class BaseAlchemyDbAdapter(DbAdapter):
    """ This class the base class for SQLAlchemyAdapter and MongoAlchemyAdapter."""

    def get_object(self, ObjectClass, id):
        """ Retrieve object by ID """
        return ObjectClass.query.get(id)

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects matching the case sensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("BaseAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a filter to the query
            query = query.filter(field==field_value)

        # Execute query
        return query.all()


    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case sensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("BaseAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field==field_value)  # case sensitive!!

        # Execute query
        return query.first()

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case insensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("BaseAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field.ilike(field_value))  # case INsensitive!!

        # Execute query
        return query.first()

    def add_object(self, ObjectClass, **kwargs):
        """ Add an object of class 'ObjectClass' with fields and values specified in '**kwargs'. """
        object=ObjectClass(**kwargs)
        self.db.session.add(object)
        return object

    def update_object(self, object, **kwargs):
        """ Update object 'object' with the fields and values specified in '**kwargs'. """
        for key,value in kwargs.items():
            if hasattr(object, key):
                setattr(object, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(object), key))

    def delete_object(self, object):
        """ Delete object 'object'. """
        self.db.session.delete(object)

class SQLAlchemyDbAdapter(BaseAlchemyDbAdapter):
    """ This class shields the code from SQLAlchemy specifics."""

    def commit(self):
        self.db.session.commit()


class MongoAlchemyDbAdapter(BaseAlchemyDbAdapter):
    """ This class shields the code from MongoAlchemy specifics."""

    def get_object(self, ObjectClass, id):
        """ Retrieve object by ID """
        # Translate Flask-User integer ID to MongoDB ObjectID
        hex_id = format(id, 'x')
        return ObjectClass.query.get(hex_id)

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case insensitive filters in 'kwargs'. """

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
        # Update object
        super(MongoAlchemyDbAdapter, self).update_object(object, **kwargs)
        # Save changes to DB
        object.save()

    def delete_object(self, object):
        """ Delete object 'object'. """
        self.db.session.remove(object)

    def commit(self):
        self.db.session.flush()
