.. _BasicApp:

Basic App
=========

The Basic App allows users to register and login with an email address
and requires proper SMTP settings.

Install Flask-User
------------------

We recommend making use of virtualenv and virtualenvwrapper::

    # Create virtual env
    mkvirtualenv my_app
    workon my_app

    # Create working directory
    mkdir -p ~dev/my_app           # or  mkdir C:\dev\my_app
    cd ~/dev/my_app                # or  cd C:\dev\my_app

    # Install Flask-User
    pip install flask-user

Create the basic_app.py file
----------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ~/dev/my_app/basic_app.py

.. literalinclude:: ../../example_apps/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 33-38, 52-53, 69-70, 90

Highlighted lines shows the few additional Flask-User code lines.

Configure Flask-Mail
--------------------
Make sure to properly configure Flask-Mail settings::

   # Flask-Mail SMTP Server settings
   MAIL_SERVER =
   MAIL_PORT =
   MAIL_USE_SSL =
   MAIL_USE_TLS =

   # Flask-Mail SMTP Account settings
   MAIL_USERNAME =
   MAIL_PASSWORD =

.. note::

   Gmail and Yahoo mail nowadays disable SMTP requests by default.
   Search the web for 'Gmail less secure apps' or 'Yahoo less secure apps'
   to learn how to change this default setting for your account.

   See :ref:`QuickStartApp` for an example without SMTP.


Run the Basic App
-----------------
Run the Basic App with the following command::

    cd ~/dev/my_app
    python basic_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive an EmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the quickstart_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

