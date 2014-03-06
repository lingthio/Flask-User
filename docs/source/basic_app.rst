=========
Basic App
=========
| The Basic App builds on Minimal App:
| - **Registration**, **Login**, **Change password** and **Logout**
|
| and adds:
| - **Login with Username** and **Change username**
| - **Email confirmation** and **Forgot password**
| - the ``create_app()`` application factory pattern (for automated tests)
|
| This app requires appropriate SMTP configuration.

Create basic_app.py
-------------------

Create ~/dev/example/basic_app.py with the content below.

Make sure to adjust the ``MAIL_*`` settings below to the correct SMTP server and SMTP account settings.

.. literalinclude:: includes/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 3, 14-27, 44, 58-60

Highlighted code shows what was added from the Minimal App.

Run the Basic App
-----------------
Run the Basic App with the following command::

    cd ~/dev/example
    python basic_app.py

And point your browser to ``http://localhost:5000``.

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a SQLAlchemy error message, delete the basic_app.db file and restart the app.
You may be using an old DB schema in that file.

Up Next: :doc:`roles_required_app`
