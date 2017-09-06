.. _BasicApp:

Basic App
=========

The Basic App builds on the QuickStart App by adding the following features:

- Register and Login with an email
- Confirm emails, Change passwords
- Role-base authorization
- Enable translations

Unlike the QuickStart App, the Basic App requires proper SMTP settings
and the installation of ``Flask-Babel`` and ``speaklater``.

Create a development environment
--------------------------------
We recommend making use of virtualenv and virtualenvwrapper::

    # Create virtual env
    mkvirtualenv my_app
    workon my_app

    # Create working directory
    mkdir -p ~dev/my_app           # or  mkdir C:\dev\my_app
    cd ~/dev/my_app                # or  cd C:\dev\my_app

Install required Python packages
--------------------------------
::

   pip install Flask-User
   pip install Flask-Babel
   pip install speaklater

Create the basic_app.py file
----------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ~/dev/my_app/basic_app.py

.. literalinclude:: ../../example_apps/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 11, 25-33, 50-51, 71-72, 74-78, 80-85, 87-88, 93-103, 124, 140

- Lines 25-33 configure ``Flask-Mail``. Make sure to use the correct settings or emails
   will not be sent.
- Lines 50-51 sets up ``Flask-Babel``.
- Lines 82-83 defines a required ``roles`` field in the User data-model.
- Lines 85-89 defines the Role data-model.
- Lines 91-96 defines the UserRoles association table.
- Lines 98-99 sets up Flask-User.
- Lines 104-114 creates the User ``user007@example.com`` and associates her with the ``Secret`` and ``Agent`` roles.
- Line 135 ensures that a user is logged in to access the ``members_page``.
- Line 151 ensures that a user is logged in and that they have either the ``Secret``+``Sauce`` roles
   or the ``Secret``+``Agent`` roles.

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

