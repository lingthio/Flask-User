==================
Roles Required App
==================
The Roles Required App builds on the features of :doc:`basic_app`:

* Register with username and email
* Email confirmation
* Login with username or email, Logout
* Protect pages from unauthenticated access
* Change username
* Change password
* Forgot password

And adds the following:

* Role-based Authorization


Single-file techniques
----------------------
| To keep the examples simple, we are using some unusual single-file techniques:
| - Using class based configuration instead of file based configuration
| - Using ``render_template_string()`` instead of ``render_template()``
| - Placing everything in one file

*None of these techniques are recommended outside of tutorial usage*.


Setup a development environment
-------------------------------
These tutorials assume that you are working with virtualenv and virtualenvwrapper
and that the code resides in ~/dev/example::

    # Create virtualenv 'example'
    mkvirtualenv example

    # Install required Python packages in the 'example' virtualenv
    workon example
    pip install flask-user
    pip install flask-mail

    # Change working directory
    mkdir -p ~dev/example
    cd ~/dev/example                # or C:\dev\example on Windows


Create roles_required_app.py
----------------------------

Create ~/dev/example/roles_required_app.py with the content below.

| Make sure to replace the following settings:
|     MAIL_USERNAME = 'email@example.com'
|     MAIL_PASSWORD = 'password'
|     MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
|     MAIL_SERVER   = 'smtp.gmail.com'
|     MAIL_PORT     = 465
|     MAIL_USE_SSL  = True
|     MAIL_USE_TLS  = False
| with settings that are appropriate for your SMTP server.

Highlighted lines shows the lines added to the Basic App.

.. literalinclude:: includes/roles_required_app.py
   :language: python
   :linenos:
   :emphasize-lines: 6, 64-66, 71-80, 89-96, 108, 123, 127-140

Run the Roles Required App
--------------------------
Run the Roles Required App with the following command::

    cd ~/dev/example
    python roles_required_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the roles_required_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

