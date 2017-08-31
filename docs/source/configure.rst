Configure
=========

Flask-User is designed to be **largely configurable** and **almost fully customizable**.

Flask-User default features and settings can overridden in one of two ways:

1) By changing the settings in the application config file::

    # Customize Flask-User settings
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False

2) By changing the setting in the ``UserManager.customize()``::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Customize Flask-User settings
            self.USER_ENABLE_EMAIL = True
            self.USER_ENABLE_USERNAME = False

The :ref:`UserManager` documents all Flask-User settings (over 70 of them).

If a setting is defined in both the application config file and in ``UserManager.customize()``,
the ``UserManager.customize()`` setting will override the config file setting.

To keep the code base simple and robust, we offer no easy way to change
the '/user' base URL or the '/flask_user' base directory in bulk.
Please copy them from the :ref:`UserManager` docs use your editor to find-and-replace these bases.

