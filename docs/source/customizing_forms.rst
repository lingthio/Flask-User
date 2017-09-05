.. _CustomizingForms:

Customizing Forms
=================

The following Flask-User forms can be customized:

- :ref:`AddEmailForm`
- :ref:`ChangeUsernameForm`
- :ref:`EditUserProfileForm`
- :ref:`ForgotPasswordForm`
- :ref:`InviteUserForm`
- :ref:`LoginForm`
- :ref:`RegisterUserForm`
- :ref:`ResendEmailConfirmationForm`
- :ref:`ResetPasswordForm`

For each form, you can customize the following:

- :ref:`CustomizingHtmlTemplates` that renders the form,
- :ref:`CustomizingForms2` that defines the form fields, and
- :ref:`CustomizingViewMethods` that prepares the form (on HTTP GET) and processes the form data (on HTTP POST).


--------

.. _CopyingHTMLTemplates:

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

Steps 1) through 3) only need to be performed once.

--------

.. _CustomizingHTMLTemplates:

Customizing HTML templates
--------------------------

You must :ref:`copy HTML Templates<CopyingHTMLTemplates>` before you can modify them.

After you've copied the templates, you can edit any HTML template file
in your ``app/template/flask_user/`` directory,
and change it to your liking.

All Flask-User templates extend from ``app/template/flask_user_layout.html``.
You can configure all Flask-User templates to extend from your own template by::

    editing app/template/flask_user/_common_base.html, and

    replacing:
        {% extends "flask_user_layout.html" %}

    with:
        {% extends "layout.html" %}

--------

.. _CustomizingForms2:

Customizing Forms
-----------------

Optionally, if you need to add form fields to a Flask-User form, you will need to customize that form like so::

    # Customize the User class
    class User(db.Model, UserMixin):
            ...
        country = db.Column(db.String(100), nullable=False)

    # Customize the Register form:
    from flask_user.forms import RegisterForm
    class CustomRegisterForm(RegisterForm):
        # Add a country field to the Register form
        country = StringField(_('Country'), validators=[DataRequired()])

    # Customize the User profile form:
    from flask_user.forms import UserProfileForm
    class CustomUserProfileForm(UserProfileForm):
        # Add a country field to the UserProfile form
        country = StringField(_('Country'), validators=[DataRequired()])

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):

            # Configure customized forms
            self.register_form = CustomRegisterForm
            self.user_profile_form = CustomUserProfileForm
            # NB: assign:  xyz_form = XyzForm   -- the class!
            #   (and not:  xyz_form = XyzForm() -- the instance!)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    :ref:`UserManager__Forms` shows a complete list of customizable forms.

    `Default forms are defined here
    <https://github.com/lingthio/Flask-User/blob/master/flask_user/forms.py>`_

.. note::

    Notice that in a simple use case like this, the form will work without customizing
    the accompanying view method. This is because WTForm's ``populate_obj()`` function
    knows how to move data from ``form.country.data`` to ``user.country``
    (as long as the property names are identical).

--------

.. _CustomizingViewMethods:

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

    View methods perform lots of intricate operations, so use this feature with caution.
    Be sure to read the source code of the default view method and make sure you understand
    all that it does before attempting to modify its behavior.

    `Default view methods are defined here
    <https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager_views.py>`_

.. seealso:: :ref:`UserManager__Views` for a complete list of customizable view methods.

--------

.. _CustomizingValidators:

Customizing Form field Validators
---------------------------------

Flask user ships with default username and password form field validators that can be customized like so::

    from wtforms import ValidationError

    # Customize Flask-User
    class CustomUserManager(UserManager):

        # Override the default password validator
        def password_validator(form, field):
            if not some_condition:
                raise ValidationError('Some error message.')

        # Override the default username validator
        def password_username(form, field):
            if not some_condition:
                raise ValidationError('Some error message.')

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

| `Default validators are defined here <https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager.py>`_
| (Search for ``def password_validator`` or ``def username_validator``).
