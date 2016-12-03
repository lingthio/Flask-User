============
Installation
============

Flask-User v1.0 breaks backwards compatibility with v0.6 in major ways.

Derived CustomUserManager class
-------------------------------

Instead of customizing Flask-User through config settings and init_app() parameters,
v1.0 now relies on creating a custom subclass.

Old:

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

New:

    # Create custom UserManager subclass
    class CustomUserManager(UserManager):

        # Customize settings
        def customize(self, app):

            # Specify a SQLAlchemy DB Adapter with a User model
            self.db_adapter = SQLAlchemyAdapter(db, User)

    # Setup Flask-User
    user_manager = CustomUserManager(app)     # Init Flask-User and bind to app


Config settings
---------------
USER_ENABLE_EMAIL: The default is now 'False'. Set this to True if emails are used.

Optional: It is now recommended to use the CustomUserManager.customize() method to configure Flask-User settings:

    # Create CustomUserManager class
    class CustomUserManager(UserManager):

        # Customize settings
        def customize(self, app):

            # Specify a SQLAlchemy DB Adapter with a User model
            self.db_adapter = SQLAlchemyAdapter(db, User)

            # Customize settings
            self.ENABLE_EMAIL = True    # Note that it's 'ENABLE_EMAIL' and not 'USER_ENABLE_EMAIL'
