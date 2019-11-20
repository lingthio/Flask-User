Porting Basics
==============
.. include:: includes/submenu_defs.rst
.. include:: includes/porting_submenu.rst

--------

Package installs
----------------
::

    # Remove unused Python packages
    pip uninstall Flask-User     # Uninstall v0.6
    pip uninstall py-crypt       # This may already be absent
    pip uninstall Flask-Babel    # We're requiring Flask-BabelEx now

    # Install new Python packages
    pip install Flask-BabelEx    # Only if you require internationalization
    pip install Flask-User       # Install v1.0

Use: ``pip freeze | grep Flask-User`` to show the installed Flask-User version,
and update your requirements.txt file accordingly::

    # In requirements.txt:
    Flask-User==0.9.{X}

Flask-User setup
----------------
We've removed the need to specify the type of DbAdapter during application setup.

From v0.6::

    from flask_user import UserManager, UserMixin, SQLAlchemyAdapter
        ...
    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)

To v1.0+::

    from flask_user import UserManager, UserMixin  # No SQLAlchemyAdapter here!!
        ...
    # Setup Flask-User
    user_manager = UserManager(app, db, User)

Make sure to stop using the legacy SQLAlchemyAdapter or DbAdapter
classes as they will trigger legacy warning exceptions.

USER\_... config settings
-------------------------
Some v0.6 ``USER_...`` settings have been renamed in v1.0 to better reflect
what these settings means. v1.0 still honors the old v0.6 names, but
a deprecation warning message will be printed.

We recommend resolving these warning messages by renaming the following settings:

.. code-block:: none

    Replace: USER_ENABLE_RETYPE_PASSWORD
       with: USER_REQUIRE_RETYPE_PASSWORD

    Replace: USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL
       with: USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL

    Replace: USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST
       with: USER_SHOW_EMAIL_DOES_NOT_EXIST
           & USER_SHOW_USERNAME_DOES_NOT_EXIST

    Replace: MAIL_DEFAULT_SENDER     = '"App name" <info@example.com>'
       with: USER_EMAIL_SENDER_NAME  = 'App name'
           & USER_EMAIL_SENDER_EMAIL = info@example.com


User.email_confirmed_at property
--------------------------------
We renamed the ``User.confirmed_at`` property to ``User.email_confirmed_at``
to better reflect what it represents.

Replace v0.6::

    class User(db.Model, UserMixin)
            ...
        confirmed_at = db.Column(db.DateTime())

With v1.0+::

    class User(db.Model, UserMixin)
        email_confirmed_at = db.Column('confirmed_at', db.DateTime())

Notice how SQLAlchemy allows us to keep using the old ``confirmed_at`` column name
with the new ``email_confirmed_at`` property.

See :doc:`porting_advanced` for a workaround if you can not rename this property.

Form template customization
---------------------------
No known porting steps are needed for customized .html files.

Email template customization
----------------------------
No known porting steps are needed for customized .html and .txt files.

Contact us
----------
We believe this concludes the Basic Porting steps for **for applications with
minimal Flask-User customization**.

If, after reading :doc:`porting_customizations` and :doc:`porting_advanced`,
you still think this page is incomplete, please email ling.thio@gmail.com.

--------

.. include:: includes/porting_submenu.rst
