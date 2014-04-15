=========
Basic App
=========
| The Basic App builds on the features of :doc:`recipes_minimal_app`:
| - **Internationalization**
| - **Login**, **Change password** and **Logout**
|
| With the addition of a only a few application config settings, it adds:
| - **Register with Username and Email**, **Change username**
| - **Email confirmation**, **Forgot password**
| - A combined Login or Register page
| - the ``create_app()`` application factory pattern (for automated tests)

Create basic_app.py
-------------------

Create ~/dev/example/basic_app.py with the content below.

Make sure to adjust the ``MAIL_*`` settings below to the correct SMTP server and SMTP account settings.

Highlighted code shows what was added to the Minimal App.

**!! This recipe requires Flask-User v0.4.9 or up !!** Please upgrade earlier versions.

.. literalinclude:: includes/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 3, 14-30, 48, 61-63

Run the Basic App
-----------------
Run the Basic App with the following command::

    cd ~/dev/example
    python basic_app.py

And point your browser to ``http://localhost:5000``.

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the basic_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

Up Next: :doc:`recipes_roles_required_app`
