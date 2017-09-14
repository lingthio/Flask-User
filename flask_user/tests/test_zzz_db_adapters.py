from flask_user.db_adapters import MongoDbAdapter
from flask_user.db_manager import DBManager


def test_mongoengine_db_adapter(app):
    # Make sure Flask-MongoEngine and MongoEngine are installed
    try:
        from flask_mongoengine import MongoEngine
        from mongoengine import connect
    except ImportError:
        return

    # Import ConnectionError or MongoEngineConnectionError, depending on version
    try:
        from mongoengine.connection import MongoEngineConnectionError   # 0.11.0+
    except ImportError:
        from mongoengine.connection import ConnectionError as MongoEngineConnectionError   # 0.10.9 and down

    # Make sure that a MongoDB server is up and running on localhost:27017
    try:
        db = MongoEngine(app)
    except MongoEngineConnectionError:
        return

    class User(db.Document):
        username = db.StringField(default='')
        roles = db.ListField(db.StringField(), default=[])

    db_manager = DBManager(app, db, UserClass=User)

    username = 'username'

    # Test create_all_tables
    db_manager.drop_all_tables()
    db_manager.create_all_tables()

    # Test add_object
    user1 = db_manager.add_user(username='username')
    user2 = db_manager.add_user(username='SecondUser')
    db_manager.commit()

    # Test tokenizing MongoDB IDs
    token_manager = app.user_manager.token_manager
    token = token_manager.generate_token(user1.id)
    assert(token_manager.verify_token(token, 3600))

    # Test get_object
    user = db_manager.get_user_by_id('1234567890ab1234567890ab')
    assert user==None
    user = db_manager.get_user_by_id(user1.id)
    assert user==user1

    # Test find methods
    user = db_manager.find_user_by_username('Xyz')
    assert user==None
    user = db_manager.find_user_by_username(username)
    assert user==user1

    # Test find_objects, directly through adapter
    users = db_manager.db_adapter.find_objects(User)

    # Test save_object
    user.username='NewUsername'
    db_manager.save_object(user)
    db_manager.commit()
    user = db_manager.get_user_by_id(user.id)
    assert user==user1
    assert user.username=='NewUsername'

    # Test user_role methods
    db_manager.add_user_role(user1, 'Admin')
    db_manager.add_user_role(user1, 'Agent')
    user_roles = db_manager.get_user_roles(user1)
    assert user_roles == ['Admin', 'Agent']

    # Test delete_object
    user1_id = user1.id
    db_manager.delete_object(user1)
    db_manager.commit()
    user = db_manager.get_user_by_id(user1_id)
    assert user==None
    user = db_manager.get_user_by_id(user2.id)
    assert user==user2

    # Test drop_all_tables
    db_manager.drop_all_tables()
    user = db_manager.get_user_by_id(user2.id)
    assert user==None




