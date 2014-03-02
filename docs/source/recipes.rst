=======
Recipes
=======

Here we explain the use of Flask-User through code recipes.

| To keep the examples simple and in a single file, we are using some unusual practices:
| - Use of class based configuration instead of file based configuration
| - Use of ``render_template_string`` instead of ``render_template``
| - Placing everything in one file
| Please do not use these techniques outside of tutorial usage.

**Programming Environment**
These tutorials assume that you are working with virtualenv and virtualenvwrapper
and that the code resides in ~/dev/example::

    mkvirtualenv my_env
    workon my_env
    pip install flask-user

    mkdir -p ~dev/example       # or C:\dev\example on Windows
    cd ~/dev/example


| **Minimal App**
| The :doc:`minimal_app` offers features that do not require SMTP:
| - **Registration**, **Login**, **Change password** and **Logout**

| **Basic App**
| The :doc:`basic_app` builds on Minimal App and adds:
| - the ``create_app()`` application factory pattern
| - **Login with Username** and **Change username**
| - **Email confirmation** and **Forgot password**
| This app requires appropriate SMTP configuration.

.. toctree::
    :maxdepth: 1

    minimal_app
    basic_app

See :doc:`customize` and :doc:`api` for more information.

