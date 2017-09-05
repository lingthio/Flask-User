.. _ConfiguringSettings:

Configuring settings
====================

Flask-User default features and settings can overridden in one of two ways:

1) By changing the settings in the application config file::

    # Customize Flask-User settings
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False

2) By changing the setting in the ``UserManager.customize()``::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):

            # Customize Flask-User settings
            self.USER_ENABLE_EMAIL = True
            self.USER_ENABLE_USERNAME = False

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

``UserManager.customize()`` settings take precedence over the application config file settings.

Flask-User settings
-------------------

Below is a complete list of configurable Flask-User settings and their defaults.

Note: Ignore the `__Settings` part of the class name.
It's a trick we use to split the code and docs across several files.

.. autoclass:: flask_user.user_manager_settings.UserManager__Settings
    :private-members:
    :noindex:


To keep the code base simple and robust, we offer no easy way to change
the '/user' base URLs or the '/flask_user' base directories in bulk.
Please copy them from this page, then use your editor to bulk-change these settings.

