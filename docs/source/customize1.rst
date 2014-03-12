Customize One
=============

Level One customizations just require changing a setting in the application config.
These customizations have been well tested through our automated tests
and can be applied safely.

* `Customizing Features`_
* `Customizing Settings`_
* `Customizing Endpoint URLs`_


Customizing Features
--------------------
Features can be customized through the application's config

.. include:: includes/config_features.txt


Customizing Settings
--------------------
Settings can be customized through the application's config

.. include:: includes/config_settings.txt


Customizing Endpoint URLs
-------------------------
Endpoint URLs can be customized through the application's config

.. include:: includes/config_urls.txt


Customizing Email Templates
---------------------------
Email template files can be customized through the application's config

.. include:: includes/config_email_templates.txt


Customizing Form Templates
--------------------------
Form template files can be customized through the application's config

.. include:: includes/config_form_templates.txt


Obsoleted Settings
------------------
The following settings have been renamed and are now obsolete. Please rename to the new setting.

::

    # Obsoleted setting             # New setting
    USER_ENABLE_EMAILS              USER_ENABLE_EMAIL
    USER_ENABLE_USERNAMES           USER_ENABLE_USERNAME
    USER_ENABLE_RETYPE_PASSWORDS    USER_ENABLE_RETYPE_PASSWORD
    USER_LOGIN_WITH_USERNAME        USER_ENABLE_USERNAME
    USER_REGISTER_WITH_EMAIL        USER_ENABLE_EMAIL
    USER_RETYPE_PASSWORD            USER_ENABLE_RETYPE_PASSWORD