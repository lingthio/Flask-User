""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function

class DbAdapterInterface(object):
    """ Define the DbAdapter interface to find, add, update and delete
    database objects using a specific object-database mapper.
    """

    def __init__(self, app, db):
        """
        Args:
            app(Flask): The Flask appliation instance.
            db: The object-database mapper instance.

        | Example:
        |     db = SQLAlchemy()
        |     db_adapter = SQLAlchemyDbAdapter(db)

        .. note::

            Generic methods.
        """
        self.app = app
        self.db = db

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        raise NotImplementedError

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        raise NotImplementedError

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.

        ``find_first_object(User, username='myname')`` translates to
        ``User.query.filter(User.username=='myname').first()``.
        """
        raise NotImplementedError

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case insensitive.

        ``ifind_first_object(User, email='myname@example.com')`` translates to
        ``User.query.filter(User.email.ilike('myname@example.com')).first()``.
        """
        raise NotImplementedError

    def add_object(self, ObjectClass, **kwargs):
        """ Add a new object of type ``ObjectClass``,
        with fields and values specified in ``**kwargs``.
        """
        raise NotImplementedError

    def update_object(self, object, **kwargs):
        """ Update an existing object, specified by ``object``,
        with the fields and values specified in ``**kwargs``.
        """
        # Convert name=value kwargs to object.name=value
        for key,value in kwargs.items():
            if hasattr(object, key):
                setattr(object, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(object), key))

    def delete_object(self, object):
        """ Delete object specified by ``object``."""
        raise NotImplementedError

    def commit(self):
        """Save modified objects in the database session.

        .. note::

            User-class specific utility methods.
        """
        raise NotImplementedError

    def add_user_role(self, user, role_name, RoleClass=None):
        """ Add a ``role_name`` role to ``user``."""
        raise NotImplementedError

    def get_user_roles(self, user):
        """Retrieve a list of user role names.

        .. note::

            Database specific utility methods.
        """
        raise NotImplementedError

    def create_all_tables(self):
        """Create database tables for all known database data-models."""

    def drop_all_tables(self):
        """Drop all tables.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """

