from __future__ import print_function

from .db_adapter import DbAdapter

class SQLAlchemyDbAdapter(DbAdapter):
    """ Shield code from SQLAlchemy specific ORM calls."""

    # Almost all methods are defined in the DbAdapter base class.

    def __init__(self, db):
        """Specify the SQLAlchemy instance ``db``.

        | Examples:
        |    db = SQLAlchemy()
        |    db_adapter = SQLAlchemyDbAdapter(db)
        """
        super(SQLAlchemyDbAdapter, self).__init__(db)

