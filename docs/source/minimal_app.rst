===========
Minimal App
===========
| The Minimal App offers features that do not require SMTP:
| - **Registration**, **Login**, **Change password** and **Logout**

Create minimal_app.py
---------------------

Create ~/dev/example/minimal_app.py with the content below.

.. literalinclude:: includes/minimal_app.py
   :language: python
   :linenos:
   :emphasize-lines: 4, 21-26, 31-33, 37

| The highlighted lines show how you can add User Registration and Login
| with only eleven lines of additional code.
| This is what we mean by 'Easy to setup' and 'Ready to use'.

Run the Minimal App
-------------------
Run the Minimal App with the following command::

    cd ~/dev/example
    python minimal_app.py

And point your browser to ``http://localhost:5000``.

Up Next: :doc:`basic_app`
