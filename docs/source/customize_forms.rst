.. _CustomizeForms:

Customizing forms
=================

:ref:`UserManager__Forms` documents the complete list of customizable FLask-User forms.

For each form, you can customize the following:

- The **Form** that defines the form fields,
- The **View method** that prepares the form on an HTTP GET and processes the form data on an HTTP POST, and
- The **HTML template** that renders the form.

Copying HTML templates
----------------------
The HTML template files reside in the Flask-User package directory, whereever it's installed.
We'll need to copy these files into your local application's template directory before we
can change them.

1) Determine the location of where the Flask-User package is installed::

    import os
    import flask_user
    filename = flask_user.__file__
    directory = os.path.dirname(filename)
    print(directory)        # For python 2.x: print directory

    # Prints something like:
    # /Users/janedoe/.envs/my_app/lib/python2.7/site-packages/flask_user

2) Let's assume that your application's template directory is::

    ~/dev/my_app/app/templates/

3) Copy the template files, substituting your flask_user and your template directory accordingly::

    cp /Users/janedoe/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user ~/dev/my_app/app/templates/.
    cp /Users/janedoe/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user_base.html ~/dev/my_app/app/templates/.

You should now have an app/template/flask_user directory::

    ls -1 ~/dev/my_app/app/templates/flask_user

    # Expected output:
    # _authorized_base.html
    # _common_base.html
    # _macros.html
    # _public_base.html
    # change_password.html
    # change_username.html
    # email_templates
    # ... etc.

4) Optionally change Flask-User's layout template

- Forms that any user may access extend ``app/template/flask_user/_public_base.html``.
- Forms for authorized users may access extend ``app/template/flask_user/_authorized_base.html``.
- Both base templates extend ``app/template/flask_user/_common_base.html``.
- The ``_common_base.html`` finally extends ``app/template/flask_user_layout.html``.

It is likely that you want to use your own ``app/template/layout.html`` template,
and this base file hierarchy is put in place so that you only need to edit one file::

    # edit app/template/flask_user/_common_base.html
    #
    # replace:
    #     {% extends "flask_user_layout.html" %}
    #
    # with:
    #     {% extends "layout.html" %}

Steps 1) through 4) only need to be performed once.

Customizing HTML templates
--------------------------

Edit an HTML template file in your ``app/template/flask_user/`` directory and change it to your liking.

Customizing Forms
-----------------

Optionally, if you need to add fields to a Flask-User form, you will need to customize this form like so::

    # Make sure to add a field to your User class
    class User(db.Model, UserMixin):
            ...
        country = db.Column(db.String(100), nullable=False)

    # Customize the Register form:
    from flask_user.user_manager_forms import RegisterForm
    class CustomRegisterForm(RegisterForm):
        # Add a country field to the Register form
        country = StringField(_('Country'), validators=[DataRequired()])

    # Customize the User profile form:
    from flask_user.user_manager_forms import UserProfileForm
    class CustomUserProfileForm(UserProfileForm):
        # Add a country field to the UserProfile form
        country = StringField(_('Country'), validators=[DataRequired()])

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):

            # Configure customized forms
            # NB: assign ``= Form`` (the class) and not ``= Form()`` (the instance) !!
            self.register_form = CustomRegisterForm
            self.user_profile_form = CustomUserProfileForm

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    Notice that in a simple use case like this, the form will work without customizing
    the accompanying view method. This is because WTForm's ``populate_obj()`` function
    knows how to move data from ``form.country.data`` to ``user.country``
    (as long as the attribute names are identical).

.. seealso:: :ref:`UserManager__Forms` for a complete list of customizable forms.

Customizing view methods
------------------------

View methods contain the code that prepares forms (on an HTTP GET) and process forms (on an HTTP POST).

Optionally, if you want to change the default behaviour, you can customize the view methods like so::


    # Customize Flask-User
    class CustomUserManager(UserManager):

        # Override or extend the default login view method
        def login_view(self):
            pass

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. warning::

    View perform lots of intricate operations, so use this feature with caution.
    Be sure to read the source code of the default view function and make sure you understand
    all that it does before attempting to change its behavior.

    | Default view functions are defined here:
    | ``/Users/janedoe/.envs/my_app/lib/python2.7/site-packages/flask_user/user_manager_views.py``

.. seealso:: :ref:`UserManager__Views` for a complete list of customizable view methods.

