.. _RolesRequiredApp:

Roles Required App
==================
The Roles Required App demonstrate the use of the ``@roles_required`` decorator
to add role-based authorization to a Flask application.

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


Create the roles_required_app.py file
-------------------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ``~/dev/my_app/roles_required_app.py``

.. literalinclude:: ../../example_apps/roles_required_app.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 23-27, 41-42, 54-55, 57-60, 62-66, 71-72, 101, 118

Highlighted lines shows the few additional Flask-User code lines.


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

