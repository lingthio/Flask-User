"""This module defines the DbAdapter interface.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

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
        """
        self.app = app
        self.db = db

    def add_object(self, ObjectClass, **kwargs):
        """ Add a new object of type ``ObjectClass``,
        with fields and values specified in ``**kwargs``.
        """
        raise NotImplementedError

    def commit(self):
        """Save modified objects in the database session.
        Only used by session-centric object-database mappers.
        """
        raise NotImplementedError

    def delete_object(self, object):
        """ Delete object specified by ``object``."""
        raise NotImplementedError

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        raise NotImplementedError

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
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


    # Database management methods
    # ---------------------------

    def create_all_tables(self):
        """Create database tables for all known database data-models."""

    def drop_all_tables(self):
        """Drop all tables.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """

