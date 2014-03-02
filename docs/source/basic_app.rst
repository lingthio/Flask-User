=========
Basic App
=========
| The Basic App builds on Minimal App and adds:
| - the ``create_app()`` application factory pattern
| - **Login with Username** and **Change username**
| - **Email confirmation** and **Forgot password**
| This app requires appropriate SMTP configuration.

Create basic_app.py
-------------------

Create ~/dev/example/basic_app.py with the content below.

Make sure to adjust the ``MAIL_*`` settings below to the correct SMTP server and SMTP account settings.

.. literalinclude:: includes/basic_app.py
   :language: python



Run the Basic App
-----------------
Run the Basic App with the following command::

    cd ~/dev/example
    python basic_app.py

And point your browser to ``http://localhost:5000``.

If you receive an EmailException error message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

See also: :doc:`minimal_app` and :doc:`customize`
