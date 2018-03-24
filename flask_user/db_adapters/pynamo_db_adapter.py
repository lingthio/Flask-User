""" This module implements the DBAdapter interface for Pynamo (which uses DynamoDB)"""

from __future__ import print_function

# Non-system imports are moved into the methods to make them an optional requirement

from flask_user.db_adapters import DbAdapterInterface


class PynamoDbAdapter(DbAdapterInterface):
    """ This object is used to shield Flask-User from PynamoDB specific functions.
    """

    def __init__(self, app, db=None):
        """Args:
            app(Flask): The Flask appliation instance.
            db(PynamoDB): The PynamoDB connection instance.

        | Example:
        |    app = Flask(__name__)
        |    db = ignored
        |    db_adapter = PynamoDbAdapter(app, db)
        """
        # This no-op method is defined to show it in Sphinx docs in order 'bysource'
        super(PynamoDbAdapter, self).__init__(app, db)

    def add_object(self, object):
        """ Add a new object to the database.

        | Session-based ODMs would call something like ``db.session.add(object)``.
        | Object-based ODMs would call something like ``object.save()``.
        """
        object.save()

    def commit(self):
        """Save all modified session objects to the database.

        | Session-based ODMs would call something like ``db.session.commit()``.
        | Object-based ODMs would do nothing.
        """
        pass

    def delete_object(self, object):
        """ Delete object from database.
        """
        object.delete()

    def find_objects(self, ObjectClass, **kwargs):
        """ Retrieve all objects of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case sensitive.
        """
        filter = None
        for k, v in kwargs.items():
            cond = ObjectClass.getattr(k) == v
            filter = cond if filter is None else filter & cond

        return ObjectClass.scan(filter)

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case sensitive.
        """
        filter = None
        for k, v in kwargs.items():
            cond = getattr(ObjectClass, k) == v
            filter = cond if filter is None else filter & cond

        return list(ObjectClass.scan(filter, limit=1))[0]

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object of type ``ObjectClass``,
        matching the specified filters in ``**kwargs`` -- case insensitive.

        | If USER_IFIND_MODE is 'nocase_collation' this method maps to find_first_object().
        | If USER_IFIND_MODE is 'ifind' this method performs a case insensitive find.
        """
        from pynamodb.attributes import UnicodeAttribute

        if self.user_manager.USER_IFIND_MODE == 'nocase_collation':
            return self.find_first_object(ObjectClass, **kwargs)

        # The below is horrendously slow on a large user database, but DynamoDB
        # has no support for case insensitive search, so we have to scan.
        # We try and be a little smart and use any non-unicode filters in the scan, thought.

        tfilters = {k: v.lower() for k, v in kwargs.items() if type(getattr(ObjectClass, k)) == UnicodeAttribute}

        ntfilter = None
        for k in [k for k in kwargs if k not in tfilters]:
            cond = getattr(ObjectClass, k) == kwargs[k]
            ntfilter = cond if ntfilter is None else ntfilter & cond

        for o in ObjectClass.scan(ntfilter):
            for k in tfilters:
                if getattr(o, k, None).lower() != kwargs[k]:
                    break
            else:
                # all match
                return o

        return None

    def get_object(self, ObjectClass, id):
        """ Retrieve object of type ``ObjectClass`` by ``id``.

        | Returns object on success.
        | Returns None otherwise.
        """
        try:
            return ObjectClass.get(id)
        except ObjectClass.DoesNotExist:
            return None

    def save_object(self, object):
        """ Save object to database.

        | Session-based ODMs would do nothing.
        | Object-based ODMs would do something like object.save().
        """
        object.save()

    # Database management methods
    # ---------------------------

    def __get_classes(self):
        db_attrs = ['UserClass', 'UserEmailClass', 'UserInvitationClass', 'RoleClass']
        klasses = []
        for a in db_attrs:
            klass = getattr(self.user_manager.db_manager, a, None)
            if klass is not None:
                klasses.append(klass)
        return klasses

    def create_all_tables(self):
        """Create database tables for all known database data-models."""
        for klass in self.__get_classes():
            if not klass.exists():
                klass.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    def drop_all_tables(self):
        """Drop all tables.

        .. warning:: ALL DATA WILL BE LOST. Use only for automated testing.
        """
        for klass in self.__get_classes():
            if klass.exists():
                klass.delete_table()
