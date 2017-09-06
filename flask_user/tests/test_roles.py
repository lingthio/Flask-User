from flask import current_app
from flask_sqlalchemy import SQLAlchemy


def test_roles(db):
    um =  current_app.user_manager
    db_adapter= um.db_adapter
    password_hash = um.password_manager.hash_password('Password1')
    User = um.UserClass

    if isinstance(db, SQLAlchemy):
        from .tst_app import Role
        RoleClass = Role
    else:
        RoleClass = None

    # user0 has no roles
    user0 = db_adapter.add_object(User, username='user0', email='user0@example.com', password=password_hash)

    # user1 has only role1
    user1 = db_adapter.add_object(User, username='user1', email='user1@example.com', password=password_hash)
    db_adapter.add_user_role(user1, 'Role 1', RoleClass=RoleClass)

    # user2 has role1 and role2
    user2 = db_adapter.add_object(User, username='user2', email='user2@example.com', password=password_hash)
    db_adapter.add_user_role(user2, 'Role 1', RoleClass=RoleClass)
    db_adapter.add_user_role(user2, 'Role 2', RoleClass=RoleClass)

    # Save everything to the DB
    db_adapter.commit()

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

    # Delete users
    db_adapter.delete_object(user1)
    db_adapter.delete_object(user1)

    # Delete roles
    if isinstance(db, SQLAlchemy):
        role1 = db_adapter.find_first_object(RoleClass, name='Role 1')
        db_adapter.delete_object(role1)
        role2 = db_adapter.find_first_object(RoleClass, name='Role 2')
        db_adapter.delete_object(role2)

    db_adapter.commit()


