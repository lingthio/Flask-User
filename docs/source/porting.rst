============
Installation
============

Flask-User v0.9 breaks backwards compatibility with v0.6 in order to support custom UserManager subclasses.

UserManager() and init_app() parameter order
--------------------------------------------

Flask-User v0.9 accepts the `app` and `db_adapter` parameters to be specified to UserManager() and init_app()
in two different orders::

    db_adapter = SQLAlchemyAdapter(db, User)        # Define SQLAlchemy DB with User model
    user_manager = UserManager(app, db_adapter)     # Inititialize v0.9+ style

or::

    db_adapter = SQLAlchemyAdapter(db, User)        # Define SQLAlchemy DB with User model
    user_manager = UserManager(db_adapter, app)     # Inititialize v0.6 style

The v0.9+ style is recommended. The v0.6 style will be supported in Flask-User v0.9 and v1.0
but may be obsoleted in the future.


Config settings
---------------
USER_ENABLE_EMAIL: The default is now 'False'. Set this to True if emails are used.

Optional: It is now recommended to use the CustomUserManager.customize() method to configure Flask-User settings::

    # Define CustomUserManager subclass
    class CustomUserManager(UserManager):

        # Customize settings
        def customize(self, app):
            self.enable_email = True    # Note that it's 'enable_email' and not 'USER_ENABLE_EMAIL'
