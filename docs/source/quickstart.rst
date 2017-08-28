QuickStart
==========

With less than a dozen lines of code, we can add User Authentication and Management
to existing Flask applications with the following additional functionality:

* User registration
* Email confirmation
* Authentication (Login and Logout)
* Change username
* Change password
* Forgot password

Install Flask-User
------------------

We recommend making use of virtualenv and virtualenvwrapper::

    mkvirtualenv my_app
    workon my_app
    pip install flask-user

    mkdir -p ~dev/my_app           # or  mkdir C:\dev\my_app
    cd ~/dev/my_app                # or  cd C:\dev\my_app


Create the quickstart_app.py file
---------------------------------

Create ~/dev/my_app/quickstart_app.py with the content below.

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

    cd ~/dev/my_app
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

