""" This file shields Flask-User code from database/ORM specific functions.
"""

# Copyright (c) 2013 by Ling Thio
# Author: Ling Thio (ling.thio@gmail.com)
# License: Simplified BSD License, see LICENSE.txt for more details.


from __future__ import print_function

class DbAdapter(object):
    """ Define the DbAdapter interface to find, add, update and delete
    database objects using a specific object-database mapper.
    """

    def __init__(self, db):
        """Specify the database object-mapper instance ``db``.

        | Example:
        |     db = SQLAlchemy()
        |     db_adapter = SQLAlchemyDbAdapter(db)
        """
        self.db = db

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``."""
        raise NotImplementedError

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive. """

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
        with fields and values specified in ``**kwargs``. """
        raise NotImplementedError

    def update_object(self, object, **kwargs):
        """ Update an existing object, specified by ``object``,
        with the fields and values specified in ``**kwargs``. """
        raise NotImplementedError

    def delete_object(self, object):
        """ Delete object specified by ``object``. """
        raise NotImplementedError

    def commit(self):
        """Save modified objects in the database session."""
        raise NotImplementedError

    def get_user_role_names(self, user):
        """ Retrieve a list of user role names."""
        raise NotImplementedError

