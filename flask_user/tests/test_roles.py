import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user

from flask_user import login_required, roles_accepted, roles_required, allow_unconfirmed_email

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

def test_decorators(request):

    # Setup view functions with decorators
    # ------------------------------------
    
    def standard_view():
        return 'view'

    @login_required
    def login_required_view():
        return 'view'

    @roles_accepted('A', 'B')
    def roles_accepted_view():
        return 'view'

    @roles_required('A', 'B')
    def roles_required_view():
        return 'view'

    @allow_unconfirmed_email
    def without_view():
        return 'view'

    @allow_unconfirmed_email
    @login_required
    def login_required_without():
        return 'view'

    @allow_unconfirmed_email
    @roles_accepted('A', 'B')
    def roles_accepted_without():
        return 'view'

    @allow_unconfirmed_email
    @roles_required('A', 'B')
    def roles_required_without():
        return 'view'

    um =  current_app.user_manager
    User = um.UserClass

    # Create objects with mockup IDs and password
    user = User(id=1, password='abcdefgh', email_confirmed_at=None)
    role_a = um.RoleClass(id=1, name='A')
    role_b = um.RoleClass(id=2, name='B')

    with current_app.test_request_context():
        # Test decorators with an unauthenticated user
        assert standard_view() == 'view'
        assert login_required_view() != 'view'
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert without_view() != 'view'
        assert login_required_without() != 'view'
        assert roles_accepted_without() != 'view'
        assert roles_required_without() != 'view'

        # Test decorators with a logged in user without a confirmed email
        login_user(user)
        assert login_required_view() != 'view'
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert without_view() == 'view'
        assert login_required_without() == 'view'

        user.roles = []
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() != 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_a]
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_b]
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_a, role_b]
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() == 'view'

        # Test decorators with a logged in user with a confirmed email
        user.email_confirmed_at = datetime.datetime.utcnow()
        assert login_required_view() == 'view'
        assert without_view() == 'view'
        assert login_required_without() == 'view'

        user.roles = []
        assert roles_accepted_view() != 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() != 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_a]
        assert roles_accepted_view() == 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_b]
        assert roles_accepted_view() == 'view'
        assert roles_required_view() != 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() != 'view'

        user.roles = [role_a, role_b]
        assert roles_accepted_view() == 'view'
        assert roles_required_view() == 'view'
        assert roles_accepted_without() == 'view'
        assert roles_required_without() == 'view'

        logout_user()
