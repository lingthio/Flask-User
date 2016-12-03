==================
Roles Required App
==================
The Roles Required App builds on the features of :doc:`basic_app`:

* Register form
* Login form
* Logout link
* Authorize pages that require a logged in user
* Change username form
* Change password form

And adds the following:

* Role-based Authorization


Single-file techniques
----------------------
| To keep the examples simple, we are using some unusual single-file techniques:
| - Using class based configuration instead of file based configuration
| - Using ``render_template_string()`` instead of ``render_template()``
| - Placing everything in one file

*None of these techniques are recommended for use outside of tutorial.*


Setup a development environment
-------------------------------
These tutorials assume that you are working with virtualenv and virtualenvwrapper
and that the code resides in ~/dev/example::

    # Create virtualenv 'example'
    mkvirtualenv example

    # Install required Python packages in the 'example' virtualenv
    workon example
    pip install flask-user

    # Change working directory
    mkdir -p ~dev/example
    cd ~/dev/example                # or C:\dev\example on Windows


Create roles_required_app.py
----------------------------

Create ~/dev/example/roles_required_app.py with the content below.

Highlighted lines shows the lines added to the Basic App to produce the Roles Required App

.. literalinclude:: includes/roles_required_app.py
   :language: python
   :linenos:
   :emphasize-lines: 5, 50-63, 72-79, 112

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

