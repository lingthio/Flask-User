================================
Porting Flask-User v0.6 to v0.9+
================================

Flask-User v0.9 breaks backwards compatibility with v0.6 in order to support custom UserManager subclasses.

UserManager() and init_app() parameter order
--------------------------------------------
Flask-User v0.9 changed the parameter order for UserManager() and init_app()::

    user_manager = UserManager(app, db_adapter)     # v0.9 style call

For backward compatibility reasons, the v0.6 parameter order is also supported, but not recommended::

    user_manager = UserManager(db_adapter, app)     # v0.6 style call

The v0.6 style will be suppored in v0.9 and v1.0, but will be obsoleted in the future.


verify_password() parameter order
---------------------------------
Flask-User v0.9 changed the parameter order for verify_password::

    verify_password(user, password)                 # v0.9 style call

For backward compatibility reasons, the v0.6 parameter order is also supported, but not recommended::

    verify_password(password, user)                 # v0.6 style call

The v0.6 style will be suppored in v0.9 and v1.0, but will be obsoleted in the future.


Config settings
---------------
USER_ENABLE_EMAIL: The default is now 'False'. Set this to True if emails are used.

Optional: It is now recommended to use the CustomUserManager.customize() method to configure Flask-User settings::

    # Define CustomUserManager subclass
    class CustomUserManager(UserManager):

        # Customize settings
        def customize(self, app):
            self.ENABLE_EMAIL = True    # Note that it's 'ENABLE_EMAIL' and not 'USER_ENABLE_EMAIL'
