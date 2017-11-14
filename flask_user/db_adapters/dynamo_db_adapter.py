"""This module implements the DbAdapter interface for Flywheel.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from __future__ import print_function
import pdb

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user.db_adapters import DbAdapterInterface


class DynamoDbAdapter(DbAdapterInterface):
    """ Implements the DbAdapter interface to find, add, update and delete
    database objects using Flask-Flywheel.
    """

    def __init__(self, app, db):
        """Args:
            app(Flask): The Flask appliation instance.
            db(Flywheel): The Flywheel object-database mapper instance.

        | Example:
        |    app = Flask(__name__)
        |    db = Flywheel()
        |    db_adapter = DynamoDbAdapter(app, db)
        """
        # This no-op method is defined to show it in Sphinx docs in order 'bysource'
        super(DynamoDbAdapter, self).__init__(app, db)

    def add_object(self, object):
        """Add object to db session. Only for session-centric object-database mappers."""
        if object.id is None:
            object.get_id()
        self.db.engine.save(object)

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        print('dynamo.get(%s, %s)' % (ObjectClass, str(id)))
        resp = self.db.engine.get(ObjectClass, [id])
        if resp:
            return resp[0]
        else:
            return None

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.
        """

        print('dynamo.find_objects(%s, %s)' % (ObjectClass, str(kwargs)))

        query = self.db.engine.query(ObjectClass)
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("DynamoDBAdapter.find_objects(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field == field_value)

        # Execute query
        return query.all(desc=True)

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the filters specified in ``**kwargs`` -- case sensitive.

        ``find_first_object(User, username='myname')`` translates to
        ``User.query.filter(User.username=='myname').first()``.
        """

        print('dynamo.find_first_object(%s, %s)' % (ObjectClass, str(kwargs)))
        query = self.db.engine.query(ObjectClass)
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError("DynamoDBAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field == field_value)

        # Execute query
        out = query.first(desc=True)#, attributes=['password'])
        return out

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case insensitive.

        | If USER_IFIND_MODE is 'nocase_collation' this method maps to find_first_object().
        | If USER_IFIND_MODE is 'ifind' this method performs a case insensitive find.
        """
        # Call regular find() if USER_IFIND_MODE is nocase_collation
        if self.user_manager.USER_IFIND_MODE=='nocase_collation':
            return self.find_first_object(ObjectClass, **kwargs)

        raise NotImplementedError

    def save_object(self, object, **kwargs):
        """ Save object. Only for non-session centric Object-Database Mappers."""
        self.db.engine.sync(object)

    def delete_object(self, object):
        """ Delete object specified by ``object``. """
        #pdb.set_trace()
        self.db.engine.delete_key(object)#, userid='abc123', id='1')
        print('dynamo.delete_object(%s)' % object)
        #self.db.session.delete(object)

    def commit(self):
        """This method does nothing for DynamoDbAdapter.
        """
        # pdb.set_trace()
        print('dynamo.commit()')
        #self.db.engine.sync()
        # self.db.session.commit()


    # Database management methods
    # ---------------------------

    def create_all_tables(self):
        """This method does nothing for DynamoDbAdapter."""
        self.db.engine.create_schema()

    def drop_all_tables(self):
        """Drop all document collections of the database.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        self.db.engine.delete_schema()
