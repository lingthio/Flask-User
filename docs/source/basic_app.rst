Basic App
=========

The sample code below illustrates the power of using Flask-User with sensible defaults:
With just a dozen additional code statements,
a basic Flask application can be transformed to offer the following features:

* Register with username and email
* Email confirmation
* Login with username or email, Logout
* Protect pages from unauthenticated access
* Change username
* Change password
* Forgot password

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


Create the basic_app.py file
----------------------------

Create ~/dev/example/basic_app.py with the content below.

| Make sure to replace the following settings:
|     MAIL_USERNAME = 'email@example.com'
|     MAIL_PASSWORD = 'password'
|     MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
|     MAIL_SERVER   = 'smtp.gmail.com'
|     MAIL_PORT     = 465
|     MAIL_USE_SSL  = True
|     MAIL_USE_TLS  = False
| with settings that are appropriate for your SMTP server.

Highlighted lines shows the lines added to a basic Flask application.

.. literalinclude:: includes/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 5, 39-55, 60-62, 79


Run the Basic App
-----------------------
Run the Basic App with the following command::

    cd ~/dev/example
    python basic_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the basic_app.sqlite file and restart the app.
You may be using an old DB schema in that file.


Up Next
-------
:doc:`flask_user_starter_app`

