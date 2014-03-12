=======
Recipes
=======

Here we explain the use of Flask-User through code recipes.

**Programming Environment**
These tutorials assume that you are working with virtualenv and virtualenvwrapper
and that the code resides in ~/dev/example::

    mkvirtualenv my_env
    workon my_env
    pip install flask-user

    mkdir -p ~dev/example
    cd ~/dev/example                # or C:\dev\example on Windows

| **Single-file techniques**
| To keep the examples simple and in a single file, we are using some unusual techniques:
| - Placing everything in one file
| - Use of class based configuration instead of file based configuration
| - Use of ``render_template_string`` instead of ``render_template``
| *None of these techniques are recommended outside of tutorial usage*.

| **Minimal App**
| The :doc:`minimal_app` offers features that do not require SMTP:
| - **Registration**, **Login**, **Change password** and **Logout**

| **Basic App**
| The :doc:`basic_app` builds on Minimal App and adds:
| - **Login with Username** and **Change username**
| - **Email confirmation** and **Forgot password** (requires SMTP)
| - the ``create_app()`` application factory pattern

| **Roles Required App**
| The :doc:`roles_required_app` builds on Basic App and adds:
| - **Role-based Authorization** (v0.3.7 and up)

.. toctree::
    :maxdepth: 1

    minimal_app
    basic_app
    roles_required_app

See :doc:`customization` and :doc:`api` for more information.

