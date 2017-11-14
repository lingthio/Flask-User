.. _ConfiguringSettings:

Configuring settings
====================
.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst

--------

Flask-User default features and settings can overridden through the app config::

    # Customize Flask-User settings
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False

Flask-User settings
-------------------

Below is a complete list of configurable Flask-User settings and their defaults.

Note: Ignore the `__Settings` part of the class name.
It's a trick we use to split the code and docs across several files.

.. autoclass:: flask_user.user_manager__settings.UserManager__Settings
    :private-members:
    :noindex:


To keep the code base simple and robust, we offer no easy way to change
the '/user' base URLs or the '/flask_user' base directories in bulk.
Please copy them from this page, then use your editor to bulk-change these settings.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
