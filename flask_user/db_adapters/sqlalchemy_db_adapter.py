from __future__ import print_function

from .db_adapter import DbAdapter

class SQLAlchemyDbAdapter(DbAdapter):
    """ Implements the DbAdapter interface to find, add, update and delete
    database objects using Flask-SQLAlchemy.
    """

    # Almost all methods are defined in the DbAdapter base class.

    def __init__(self, db):
        """Specify the SQLAlchemy instance ``db``.

        | Example:
        |    db = SQLAlchemy()
        |    db_adapter = SQLAlchemyDbAdapter(db)
        """
        super(SQLAlchemyDbAdapter, self).__init__(db)

