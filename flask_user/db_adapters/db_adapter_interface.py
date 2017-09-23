"""This module defines the DbAdapter interface.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

class DbAdapterInterface(object):
    """ Define the DbAdapter interface to manage objects in various databases.

    This interface supports session-based ODMs (``db.session.add()/commit()``)
    as well as object-based ODMs (``object.save()``).
    """

    def __init__(self, app, db):
        """
        Args:
            app(Flask): The Flask appliation instance.
            db: The object-database mapper instance.
        """
        self.app = app
        self.db = db
        self.user_manager = self.app.user_manager

    def add_object(self, object):
        """ Add a new object to the database.

        | Session-based ODMs would call something like ``db.session.add(object)``.
        | Object-based ODMs would call something like ``object.save()``.
        """
        raise NotImplementedError

    def commit(self):
        """Save all modified session objects to the database.

        | Session-based ODMs would call something like ``db.session.commit()``.
        | Object-based ODMs would do nothing.
        """
        raise NotImplementedError

    def delete_object(self, object):
        """ Delete object from database.
        """
        raise NotImplementedError

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case sensitive.
        """
        raise NotImplementedError

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case sensitive.
        """
        raise NotImplementedError

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case insensitive.

        | If USER_IFIND_MODE is 'nocase_collation' this method maps to find_first_object().
        | If USER_IFIND_MODE is 'ifind' this method performs a case insensitive find.
        """
        raise NotImplementedError

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        raise NotImplementedError

    def save_object(self, object):
        """ Save object to database.

        | Session-based ODMs would do nothing.
        | Object-based ODMs would do something like object.save().
        """
        raise NotImplementedError


    # Database management methods
    # ---------------------------

    def create_all_tables(self):
        """Create database tables for all known database data-models."""
        raise NotImplementedError

    def drop_all_tables(self):
        """Drop all tables.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        raise NotImplementedError

