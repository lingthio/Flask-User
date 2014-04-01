==================
Roles Required App
==================
| The Roles Required App builds on the features of :doc:`recipes_basic_app`:
| - **Internationalization**
| - **Register**, **Login**, **Change password** and **Logout**
| - **Login with Username** and **Change username**
| - **Email confirmation** and **Forgot password**
| - the ``create_app()`` application factory pattern
|
| With a simple ``@roles_required`` function decorator, it adds:
| - **Role-based Authorization** (v0.3.7 and up)
|
| This app requires appropriate SMTP configuration.

Create roles_required_app.py
----------------------------

Create ~/dev/example/roles_required_app.py with the content below.

Make sure to adjust the ``MAIL_*`` settings below to the correct SMTP server and SMTP account settings.

.. literalinclude:: includes/roles_required_app.py
   :language: python
   :linenos:
   :emphasize-lines: 6, 55-64, 75-77, 87-95, 130

Highlighted code shows what was added from the Basic App.

Run the Roles Required App
--------------------------
Run the Roles Required App with the following command::

    cd ~/dev/example
    python roles_required_app.py

And point your browser to ``http://localhost:5000``.

If you receive an SendEmailError error message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the roles_required_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

Next :doc:`customization`