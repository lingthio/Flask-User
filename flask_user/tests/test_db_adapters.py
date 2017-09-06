from flask_mongoengine import MongoEngine
from flask_user.db_adapters import MongoEngineDbAdapter


def test_mongoengine_db_adapter(app):
    db = MongoEngine(app)
    db_adapter = MongoEngineDbAdapter(app, db)

    class User(db.Document):
        username = db.StringField(default='')
        roles = db.ListField(db.StringField(), default=[])

    username = 'Username'

    # Test create_all_tables
    db_adapter.drop_all_tables()
    db_adapter.create_all_tables()

    # Test add_object
    user1 = db_adapter.add_object(User, username=username)
    user2 = db_adapter.add_object(User, username='SecondUser')
    db_adapter.commit()

    # Test get_object
    user = db_adapter.get_object(User, '1234567890ab1234567890ab')
    assert user==None
    user = db_adapter.get_object(User, user1.id)
    assert user==user1

    # Test find methods
    users = db_adapter.find_objects(User, username='Xyz')
    assert not users
    users = db_adapter.find_objects(User, username=username)
    assert users[0]==user1
    user = db_adapter.find_first_object(User, username='Xyz')
    assert user==None
    user = db_adapter.find_first_object(User, username=username)
    assert user==user1
    user = db_adapter.ifind_first_object(User, username='xyz')
    assert user==None
    user = db_adapter.ifind_first_object(User, username=username.lower())
    assert user==user1

    # Test update_object
    db_adapter.update_object(user, username='NewUsername')
    db_adapter.commit()
    user = db_adapter.get_object(User, user.id)
    assert user==user1
    assert user.username=='NewUsername'

    # Test user_role methods
    db_adapter.add_user_role(user1, 'Admin')
    db_adapter.add_user_role(user1, 'Agent')
    user_roles = db_adapter.get_user_roles(user1)
    assert user_roles == ['Admin', 'Agent']

    # Test delete_object
    user1_id = user1.id
    db_adapter.delete_object(user1)
    db_adapter.commit()
    user = db_adapter.get_object(User, user1_id)
    assert user==None
    user = db_adapter.get_object(User, user2.id)
    assert user==user2

    # Test drop_all_tables
    db_adapter.drop_all_tables()
    user = db_adapter.get_object(User, user2.id)
    assert user==None




