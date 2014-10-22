===============
Multi Email App
===============
| The Multi Email App builds on the features of :doc:`basic_app`:
| - **Internationalization**
| - **Login**, **Change password** and **Logout**
| - **Register with Username and Email**, **Change username**
| - **Email confirmation**, **Forgot password**
| - the ``create_app()`` application factory pattern
|
| And adds the following:
| - **Multiple Emails per User** (v0.5.1 and up)
|
| This app requires appropriate SMTP configuration.

Create multi_email_app.py
-------------------------

Create ~/dev/example/multi_email_app.py with the content below.

Make sure to adjust the ``MAIL_*`` settings below to the correct SMTP server and SMTP account settings.

Highlighted code shows what was added to the Basic App.

**!! This recipe requires Flask-User v0.5.1 or up !!** Please upgrade earlier versions.

| In a nut shell:
| - Define ``User`` model (username, password, etc)
| - Define ``UserEmail`` model (user_id, email, is_confirmed, is_primary, etc)
| - Define one-to-many relationship between User and UserEmail
| - Register User and UserEmail class through ``SQLAlchemyAdapter()``
| - Visit ``/user/manage-emails`` as an authenticated user.

.. literalinclude:: includes/multi_email_app.py
   :language: python
   :linenos:
   :emphasize-lines: 60-61, 64-71, 78, 103-104

Run the Multi Email App
-----------------------
Run the Multi Email App with the following command::

    cd ~/dev/example
    python multi_email_app.py

And point your browser to ``http://localhost:5000``.

If you receive an SendEmailError message,
or if the Registration form does not respond quickly
then you may have specified incorrect SMTP settings.

If you receive a 'AssertionError: No sender address has been set' error, you may
be using an old version of Flask-Mail which uses DEFAULT_MAIL_SENDER instead of MAIL_DEFAULT_SENDER.

If you receive a SQLAlchemy error message, delete the multi_email_app.sqlite file and restart the app.
You may be using an old DB schema in that file.

Up Next
-------
:doc:`recipes_misc`