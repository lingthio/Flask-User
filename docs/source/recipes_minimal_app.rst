Minimal App
===========
| With only nine additional lines of code, the Minimal App offers the following features:
| - **Internationalization**
| - **Register with Username**, **Login**, **Change password** and **Logout**

Create minimal_app.py
---------------------

Create ~/dev/example/minimal_app.py with the content below.

The highlighted lines show Flask-User specific code.

**!! This recipe requires Flask-User v0.4.9 or up !!** Please upgrade earlier versions.

.. literalinclude:: includes/minimal_app.py
   :language: python
   :linenos:
   :emphasize-lines: 4, 28-32, 38-39, 57

Run the Minimal App
-------------------
Run the Minimal App with the following command::

    cd ~/dev/example
    python minimal_app.py

And point your browser to ``http://localhost:5000``.

To test Internationalization, set your browser to use 'Dutch' as the preferred language.

If you receive a SQLAlchemy error message, delete the minimal_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

Up Next
-------
:doc:`recipes_basic_app`
