QuickStart
==========

The sample code below illustrates the power of using Flask-User with sensible defaults:
With just a dozen additional code statements,
a basic Flask application can be transformed to offer the following features:

* User registration
* Email confirmation
* Login and Logout
* Authentication
* Change username
* Change password
* Forgot password


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
    mkdir -p ~dev/example           # or  mkdir C:\dev\example
    cd ~/dev/example                # or  C:\dev\example on Windows


Create the quickstart_app.py file
---------------------------------

Create ~/dev/example/quickstart_app.py with the content below.

Highlighted lines shows the lines added to a basic Flask application.

.. literalinclude:: includes/quickstart_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 32-35, 65-66, 84


Configure Flask-Mail
--------------------
| Make sure to replace the following Flask-Mail settings:
|     MAIL_USERNAME
|     MAIL_PASSWORD
|     MAIL_DEFAULT_SENDER
|     MAIL_SERVER
|     MAIL_PORT
|     MAIL_USE_SSL
|     MAIL_USE_TLS
| with settings that are appropriate for your SMTP server.


Run the QuickStart App
----------------------
Run the QuickStart App with the following command::

    cd ~/dev/example
    python quickstart_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the quickstart_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

