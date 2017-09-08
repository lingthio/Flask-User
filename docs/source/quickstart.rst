QuickStart
==========
.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst

--------

With less than a dozen lines of code, we can extend existing Flask applications
with the following additional functionality:

* User registration with username and/or email
* Email confirmation
* User authentication (Login and Logout)
* Change username
* Change password
* Forgot password

Choose a QuickStart app
-----------------------

- :doc:`quickstart_app` -- Login with username. No need to configure SMTP.
- :doc:`basic_app` -- Login with email, Role-based authentication, and Translations.
- :doc:`mongodb_app` -- QuickStart App for MongoDB.

Flask-User-starter-app
----------------------

While the example apps provide a quick way to illustrate the use of Flask-User,
we do not recommend its single-file techniques.

The Flask-User-starter-app follows typical Flask application practices using multiple files
in an organized directory structure::

    app/
        commands/
        models/
        static/
        templates/
        views/
    tests/

See https://github.com/lingthio/Flask-User-starter-app

This may serve as a great starting place to create your next Flask application.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst
