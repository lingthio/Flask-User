MongoDB App
===========
.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst

--------

Flask-User can work with MongoDB databases by replacing the default SQLDbAdapter
with the provided MongoDbAdapter.

The MONGODB_SETTINGS in this example requires a MongoDB server running on localhost:27017 (its default).

Install Flask-User
------------------

We recommend making use of virtualenv and virtualenvwrapper::

    # Create virtual env
    mkvirtualenv my_app
    workon my_app

    # Create working directory
    mkdir -p ~dev/my_app           # or  mkdir C:\dev\my_app
    cd ~/dev/my_app                # or  cd C:\dev\my_app

    # Install Flask-User
    pip install flask-user

Install Flask-MongoEngine
-------------------------

::

   # Install Flask-MongoEngine
   pip install Flask-MongoEngine


Create the mongodb_app.py file
------------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ``~/dev/my_app/mongodb_app.py``

.. literalinclude:: ../../example_apps/mongodb_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 25-29, 43-44, 58-59, 79

Highlighted lines shows the few additional Flask-User code lines.


Run the MongoDB App
-------------------
Run the MongoDB App with the following command::

    cd ~/dev/my_app
    python mongodb_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

[TBD]

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst
