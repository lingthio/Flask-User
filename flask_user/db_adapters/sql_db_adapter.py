"""This module implements the DbAdapter interface for SQLAlchemy.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user.db_adapters import DbAdapterInterface


class SQLDbAdapter(DbAdapterInterface):
    """ Implements the DbAdapter interface to find, add, update and delete
    database objects using Flask-SQLAlchemy.
    """

    # Almost all methods are defined in the DbAdapter base class.

    def __init__(self, app, db):
        """Args:
            app(Flask): The Flask appliation instance.
            db(SQLAlchemy): The SQLAlchemy object-database mapper instance.

        | Example:
        |     app = Flask(__name__)
        |     db = SQLAlchemy()
        |     db_adapter = SQLDbAdapter(app, db)

        .. note::

            Generic methods.
        """
        # This no-op method is defined to show it in Sphinx docs in order 'bysource'
        super(SQLDbAdapter, self).__init__(app, db)

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        return ObjectClass.query.get(id)

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        # Convert each name/value pair in '**kwargs' into a filter
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
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.

        ``find_first_object(User, username='myname')`` translates to
        ``User.query.filter(User.username=='myname').first()``.
        """

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
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case insensitive.

        ``ifind_first_object(User, email='myname@example.com')`` translates to
        ``User.query.filter(User.email.ilike('myname@example.com')).first()``.
        """

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
        """ Add a new object of type ``ObjectClass``,
        with fields and values specified in ``**kwargs``.
        """
        object=ObjectClass(**kwargs)
        self.db.session.add(object)
        return object

    def update_object(self, object, **kwargs):
        """ Update an existing object, specified by ``object``,
        with the fields and values specified in ``**kwargs``.
        """
        # Convert name=value kwargs to object.name=value
        super(SQLDbAdapter, self).update_object(object, **kwargs)

    def delete_object(self, object):
        """ Delete object specified by ``object``."""
        self.db.session.delete(object)

    def commit(self):
        """Save modified objects in the database session.

        .. note::

            User-class specific utility methods.
        """
        self.db.session.commit()

    def add_user_role(self, user, role_name, RoleClass=None):
        """ Add a ``role_name`` role to ``user``."""
        # Get or add role
        role = self.find_first_object(RoleClass, name=role_name)
        if not role:
            role = self.add_object(RoleClass, name=role_name)
        user.roles.append(role)

    def get_user_roles(self, user):
        """ Retrieve a list of user role names.

        .. note::

            Database specific utility methods.
        """
        return [role.name for role in user.roles]

    def create_all_tables(self):
        """Create database tables for all known database data-models."""
        self.db.create_all()

    def drop_all_tables(self):
        """Drop all tables of the database.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        self.db.drop_all()
