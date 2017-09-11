from .db_adapter_interface import DbAdapterInterface
from .sql_db_adapter import SQLDbAdapter
from .mongo_db_adapter import MongoDbAdapter
from .dynamo_db_adapter import DynamoDbAdapter

def select_db_adapter(app, db):
    """Determines the appropriate DbAdapter based on the ``db`` parameter type."""
    db_adapter = None

    # Check if db is a SQLAlchemy instance
    if db_adapter is None:
        try:
            from flask_sqlalchemy import SQLAlchemy
    
            if isinstance(db, SQLAlchemy):
                db_adapter = SQLDbAdapter(app, db)
        except ImportError:
            pass  # Ignore ImportErrors
    
    # Check if db is a MongoEngine instance
    if db_adapter is None:
        try:
            from flask_mongoengine import MongoEngine
    
            if isinstance(db, MongoEngine):
                db_adapter = MongoDbAdapter(app, db)
        except ImportError:
            pass  # Ignore ImportErrors
    
    # Check if db is a Flywheel instance
    if db_adapter is None:
        try:
            from flask_flywheel import Flywheel
    
            if isinstance(db, Flywheel):
                db_adapter = DynamoDbAdapter(app, db)
        except ImportError:
            pass  # Ignore ImportErrors

    return db_adapter