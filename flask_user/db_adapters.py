""" This file shields Flask-User code from database/ORM specific functions.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from datetime import datetime
from flask_login import current_user

class DBAdapter(object):
    """ This object is used to shield Flask-User from ORM specific functions.
        It's used as the base class for ORM specific adapters like SQLAlchemyAdapter."""
    def __init__(self, db, UserClass, UserProfileClass=None, EmailClass=None):
        self.db = db
        self.UserClass = UserClass          # email, password, etc.
        self.UserProfileClass = UserProfileClass    # For Additional registration fields
        self.EmailClass = EmailClass        # For multiple emails per user


class SQLAlchemyAdapter(DBAdapter):
    """ This object is used to shield Flask-User from SQLAlchemy specific functions."""
    def __init__(self, db, UserClass, UserProfileClass=None, EmailClass=None):
        super(SQLAlchemyAdapter, self).__init__(db, UserClass, UserProfileClass, EmailClass)

    def find_object(self, ObjectClass, **kwargs):
        """ Find object of class 'ObjectClass' by specified '**kwargs' -- case sensitive!! """
        # Prepare base query
        query = ObjectClass.query
        # For all name/value pairs in **kwargs
        for field_name, field_value in kwargs.items():
            # Retrieve Class attribute from field_name
            field = getattr(ObjectClass, field_name, None)
            if not field:
                raise KeyError("SQLAlchemyAdapter.find_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))
            # Add query filter
            query = query.filter(field==field_value)  # case sensitive!!
        # Execute query
        return query.first()

    def ifind_object(self, ObjectClass, **kwargs):
        """ Find object of class 'ObjectClass' by specified '**kwargs' -- case INsensitive!! """
        # Prepare base query
        query = ObjectClass.query
        # For all name/value pairs in **kwargs
        for field_name, field_value in kwargs.items():
            # Retrieve Class attribute from field_name
            field = getattr(ObjectClass, field_name, None)
            if not field:
                raise KeyError("SQLAlchemyAdapter.find_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))
            # Add query filter
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
        self.db.session.commit()

    def commit(self):
        self.db.session.commit()