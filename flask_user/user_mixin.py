from flask import current_app
from flask_login import UserMixin as LoginUserMixin

class UserMixin(LoginUserMixin):
    """ This class adds methods to the User model class required by Flask-Login and Flask-User."""

    def get_id(self):
        """Converts a User ID and parts of a User password hash to a token."""

        # This function is used by Flask-Login to store a User ID securely as a browser cookie.
        # It encrypts
        # - the User ID (to retrieve the User later), and
        # - part of the User hashed password (to invalidate the token after a password change)
        # This function works in tandem with UserMixin.get_user_by_token()
        user_manager = current_app.user_manager
        user_id = self.id
        password_ends_with = self.password[-8:]
        user_token = user_manager.token_manager.generate_token(
            user_id,               # User ID
            password_ends_with,    # Last 8 characters of user password
        )
        # print("UserMixin.get_id: ID:", self.id, "token:", user_token)
        return user_token

    @classmethod
    def get_user_by_token(cls, token, expiration_in_seconds):
        # This function works in tandem with UserMixin.get_id()

        # Verifies a token and decrypts a User ID and parts of a User password hash
        user_manager = current_app.user_manager
        data_items = user_manager.token_manager.verify_token(token, expiration_in_seconds)

        # Verify password_ends_with
        token_is_valid = False
        if data_items:
            user_id = data_items[0]
            password_ends_with = data_items[1]
            user = user_manager.get_user_by_id(user_id)
            # Make sure that last 8 characters of user password matches
            token_is_valid = user and user.password[-8:]==password_ends_with

        return user if token_is_valid else None

    def has_role(self, *specified_role_names):
        """ Return True if the user has one of the specified roles. Return False otherwise.

            has_roles() accepts a 1 or more role name parameters
                has_role(role_name1, role_name2, role_name3).

            For example:
                has_roles('a', 'b')
            Translates to:
                User has role 'a' OR role 'b'
        """

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles: return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # Return True if one of the role_names matches
        for role_name in specified_role_names:
            if role_name in user_role_names:
                return True

        # Return False if none of the role_names matches
        return False


    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.

            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).

            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.

            For example:
                has_roles('a', ('b', 'c'), d)
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        # Allow developers to attach the Roles to the User or the UserProfile object
        if hasattr(self, 'roles'):
            roles = self.roles
        else:
            if hasattr(self, 'user_profile') and hasattr(self.user_profile, 'roles'):
                roles = self.user_profile.roles
            else:
                roles = None
        if not roles: return False

        # Translates a list of role objects to a list of role_names
        user_role_names = [role.name for role in roles]

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in user_role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in user_role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True

