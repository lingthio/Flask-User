Basic App
=========
.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst

--------

The Basic App builds on the QuickStart App by adding the following features:

- Register and Login with an email
- Confirm emails, Change passwords
- Role-base authorization
- Enable translations

Unlike the QuickStart App, the Basic App requires proper SMTP settings
and the installation of ``Flask-BabelEx``.

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

   # Uninstall Flask-Babel if needed
   pip uninstall Flask-Babel

   # Install Flask-BabelEx and Flask-User
   pip install Flask-BabelEx
   pip install Flask-User

Create the basic_app.py file
----------------------------

- Open your favorite editor,
- Copy the example below, and
- Save it as ~/dev/my_app/basic_app.py

.. literalinclude:: ../../example_apps/basic_app.py
   :language: python
   :linenos:
   :emphasize-lines: 11, 25-32, 56-57, 88-89, 133, 151

- Lines 25-32 configure ``Flask-Mail``. Make sure to use the correct settings or emails
   will not be sent.

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

   See :doc:`quickstart_app` for an example without SMTP.


Configure your browser
----------------------
If you want to see translation in action, you will need to change and prioritize
a :ref:`supported language <SupportedLanguages>` (one that is other than 'English')
in your browser language preferences.

For Google Chrome:

- Chrome > Preferences. Search for 'Language'.
- Expand the 'Language' bar > Add languages.
- Check the 'Dutch' checkbox > Add.
- Make sure to move it to the top: Three dots > Move to top.


Run the Basic App
-----------------
Run the Basic App with the following command::

    cd ~/dev/my_app
    python basic_app.py

And point your browser to ``http://localhost:5000``.


Troubleshooting
---------------

If you receive an EmailError message, or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a SQLAlchemy error message, you may be using an old DB schema.
Delete the quickstart_app.sqlite file and restart the app.

If you don't see any translations, you may not have installed ``Flask-BabelEx``,
or you may not have prioritized a supported language in your browser settings.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/quickstart_submenu.rst
