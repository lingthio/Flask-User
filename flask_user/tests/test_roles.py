import datetime

from flask import current_app
from flask_login import login_user, logout_user

from flask_user import login_required, roles_accepted, roles_required, allow_unconfirmed_email

def test_decorators(app, request):

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
    User = um.db_manager.UserClass

    # Create Mock objects (They will NOT be persisted to DB. We can use dummy IDs here)
    user = um.db_manager.UserClass(id=1, password='abcdefgh', email_confirmed_at=None)
    role_a = um.db_manager.RoleClass(id=1, name='A')
    role_b = um.db_manager.RoleClass(id=2, name='B')

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

