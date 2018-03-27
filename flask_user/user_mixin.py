"""This module implements the UserMixin class for Flask-User.
This Mixin adds required methods to User data-model.
"""

from flask import current_app
from flask_login import UserMixin as FlaskLoginUserMixin

class UserMixin(FlaskLoginUserMixin):
    """ This class adds required methods to the User data-model.

    Example:
        class User(db.Model, UserMixin):
            ...
    """

    def get_id(self):
        """Converts a User ID and parts of a User password hash to a token."""

        # This function is used by Flask-Login to store a User ID securely as a browser cookie.
        # The last part of the password is included to invalidate tokens when password change.
        # user_id and password_ends_with are encrypted, timestamped and signed.
        # This function works in tandem with UserMixin.get_user_by_token()
        user_manager = current_app.user_manager

        user_id = self.id
        password_ends_with = '' if user_manager.USER_ENABLE_AUTH0 else self.password[-8:]
        user_token = user_manager.generate_token(
            user_id,               # User ID
            password_ends_with,    # Last 8 characters of user password
        )
        # print("UserMixin.get_id: ID:", self.id, "token:", user_token)
        return user_token

    @classmethod
    def get_user_by_token(cls, token, expiration_in_seconds=None):
        # This function works in tandem with UserMixin.get_id()
        # Token signatures and timestamps are verified.
        # user_id and password_ends_with are decrypted.

        # Verifies a token and decrypts a User ID and parts of a User password hash
        user_manager = current_app.user_manager
        data_items = user_manager.verify_token(token, expiration_in_seconds)

        # Verify password_ends_with
        token_is_valid = False
        if data_items:

            # Load user by User ID
            user_id = data_items[0]
            password_ends_with = data_items[1]
            user = user_manager.db_manager.get_user_by_id(user_id)
            user_password = '' if user_manager.USER_ENABLE_AUTH0 else user.password[-8:]

            # Make sure that last 8 characters of user password matches
            token_is_valid = user and user_password==password_ends_with

        return user if token_is_valid else None

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

        # Translates a list of role objects to a list of role_names
        user_manager = current_app.user_manager
        role_names = user_manager.db_manager.get_user_roles(self)

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True

