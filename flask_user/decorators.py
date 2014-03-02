from functools import wraps

from flask import current_app
from flask.ext.login import current_user

def _user_has_roles(*required_roles):
    '''
    Check to see if user has all required roles
    This function accepts a variable number of arguments
    Each argument can be a Role name or a tuple of Sub-role names.
    Roles are AND-ed. Sub-roles are OR-ed.
        @_user_has_roles('a', ('b', 'c'))
    Translates to User must have: role 'a' AND (role 'b' OR role 'c')
    '''

    user = current_user
    user_roles = [role.name for role in user.roles]

    for role in required_roles:
        if isinstance(role, (list, tuple)):
            authorized = False
            for sub_role in role:
                if sub_role in user_roles:
                    authorized = True
                    break       # Found valid sub-role: break out of loop
            if not authorized:
                return False    # All sub-roles failed: Deny authorization.
        else:
            if not role in user_roles:
                return False    # One role failed: Deny authorization.

    return True

def roles_required(*required_roles):
    '''
    Decorator for view function that require users to have certain roles.
    This decorator accepts a variable number of arguments
    Each argument can be a role name or a tuple of role names.
    Tuples are OR-ed, arguments are AND-ed.
        @role_required( ('a','b'), 'c')
    Translates to User must have: (role 'a' OR role 'b') AND role 'c'
    '''
    def wrapper(func):
        @wraps(func)

        def decorated_view(*args, **kwargs):
            # User must be logged in and have the required roles
            if current_user.is_authenticated() and _user_has_roles(*required_roles):
                return func(*args, **kwargs)

            # Redirect to login page
            return current_app.user_manager.lm.unauthorized()

        return decorated_view

    return wrapper
