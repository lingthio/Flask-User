from flask import current_app
from .tst_app import Role

def test_roles(db):
    um =  current_app.user_manager
    hashed_password = um.hash_password('Password1')
    User = um.db_adapter.UserClass

    # create users and roles
    role1 = Role(name='Role 1')
    role2 = Role(name='Role 2')

    # user0 has no roles
    user0 = User(username='user0', email='user0@example.com', password=hashed_password, active=True)
    db.session.add(user0)
    
    # user1 has only role1 
    user1 = User(username='user1', email='user1@example.com', password=hashed_password, active=True)
    user1.roles.append(role1)
    db.session.add(user1)
    
    # user2 has role1 and role2
    user2 = User(username='user2', email='user2@example.com', password=hashed_password, active=True)
    user2.roles.append(role1)
    user2.roles.append(role2)
    db.session.add(user2)
    db.session.commit()

    # test has_role()
    assert user0.has_role('Role 1')==False
    assert user0.has_role('Role 2')==False
    assert user0.has_role('Role 3')==False
    assert user0.has_role('Role 1', 'Role 2')==False
    assert user0.has_role('Role 2', 'Role 1')==False
    assert user0.has_role('Role 1', 'Role 2', 'Role 3')==False

    assert user1.has_role('Role 1')==True
    assert user1.has_role('Role 2')==False
    assert user1.has_role('Role 3')==False
    assert user1.has_role('Role 1', 'Role 2')==True
    assert user1.has_role('Role 2', 'Role 1')==True
    assert user1.has_role('Role 1', 'Role 2', 'Role 3')==True

    assert user2.has_role('Role 1')==True
    assert user2.has_role('Role 2')==True
    assert user2.has_role('Role 3')==False
    assert user2.has_role('Role 1', 'Role 2')==True
    assert user2.has_role('Role 2', 'Role 1')==True
    assert user2.has_role('Role 1', 'Role 2', 'Role 3')==True

    # test has_roles()
    assert user0.has_roles('Role 1')==False
    assert user0.has_roles('Role 2')==False
    assert user0.has_roles('Role 3')==False
    assert user0.has_roles('Role 1', 'Role 2')==False
    assert user0.has_roles('Role 2', 'Role 1')==False
    assert user0.has_roles('Role 1', 'Role 2', 'Role 3')==False

    assert user1.has_roles('Role 1')==True
    assert user1.has_roles('Role 2')==False
    assert user1.has_roles('Role 3')==False
    assert user1.has_roles('Role 1', 'Role 2')==False
    assert user1.has_roles('Role 2', 'Role 1')==False
    assert user1.has_roles('Role 1', 'Role 2', 'Role 3')==False

    assert user2.has_roles('Role 1')==True
    assert user2.has_roles('Role 2')==True
    assert user2.has_roles('Role 3')==False
    assert user2.has_roles('Role 1', 'Role 2')==True
    assert user2.has_roles('Role 2', 'Role 1')==True
    assert user2.has_roles('Role 1', 'Role 2', 'Role 3')==False

    # delete users and roles

