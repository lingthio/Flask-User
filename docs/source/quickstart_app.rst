QuickStart App
==============
.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst

--------

The QuickStart App allows users to register and login with a username
and avoids the need to configure SMTP settings.

Create a development environment
--------------------------------
We recommend making use of virtualenv and virtualenvwrapper::

    # Create virtual env
    mkvirtualenv my_app
    workon my_app

    # Create working directory
    mkdir -p ~dev/my_app           # or  mkdir C:\dev\my_app
    cd ~/dev/my_app                # or  cd C:\dev\my_app

Install required Python packages
--------------------------------
::

   pip install Flask-User

Create the quickstart_app.py file
---------------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ``~/dev/my_app/quickstart_app.py``

.. literalinclude:: ../../example_apps/quickstart_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 23-27, 41-42, 60-61, 81

Highlighted lines shows the few additional Flask-User code lines.


Run the QuickStart App
----------------------
Run the QuickStart App with the following command::

    cd ~/dev/my_app
    python quickstart_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive a SQLAlchemy error message, delete the quickstart_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst
