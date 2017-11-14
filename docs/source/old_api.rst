Flask-User API
==============
* `Template variables`_
* `Template functions`_
* `Signals`_

Template variables
------------------
The following template variables are available for use in email and form templates:

.. include:: includes/template_variables.txt

Template functions
------------------
The following template functions are available for use in email and form templates:

.. include:: includes/template_functions.txt

hash_password()
~~~~~~~~~~~~~~~
::

    user_manager.hash_password(password)
    # Returns hashed 'password' using the configured password hash
    # Config settings: USER_PASSWORD_HASH_MODE = 'passlib'
    #                  USER_PASSWORD_HASH      = 'bcrypt'
    #                  USER_PASSWORD_SALT      = SECRET_KEY


verify_password()
~~~~~~~~~~~~~~~~~~~~~~
::

    user_manager.verify_password(password, user.password)
    # Returns True if 'password' matches the user's 'hashed password'
    # Returns False otherwise.

Signals
-------
.. include:: includes/signals.txt
