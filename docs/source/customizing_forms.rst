Customizing Forms
=================

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst

--------

The following Flask-User forms can be customized:

- AddEmailForm
- ChangeUsernameForm
- EditUserProfileForm
- ForgotPasswordForm
- InviteUserForm
- LoginForm
- RegisterForm
- ResendEmailConfirmationForm
- ResetPasswordForm

For each form, you can customize the following:

- :ref:`CustomizingFormTemplates`
- :ref:`CustomizingFormClasses`
- :ref:`CustomizingFormValidators`
- :ref:`CustomizingFormViews`


--------

.. _CustomizingFormTemplates:

Customizing Form Templates
--------------------------

Before we can customize any of the form templates, we'll need to copy them
from the Flask-User install directory to your application's template directory.

Copying Form template files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Determine the location of where the Flask-User package is installed::

    # In a python shell, type the following:
    import os
    import flask_user
    print(os.path.dirname(flask_user.__file__))

    # Prints something like:
    # ~/.envs/my_app/lib/python3.6/site-packages/flask_user

2) The examples below assume the following::

    flask_user dir: ~/.envs/my_app/lib/python3.6/site-packages/flask_user
    app dir:        ~/dev/my_app

Adjust the examples below to your specific environment.

3) Copy the form template files, substituting your flask_user and your app/templates directory accordingly::

    # IMPORTANT:
    # If you've already worked on customizing email templates, you can (and must) skip this step,
    # since you've already copied the form templates along with the email templates.

    cp ~/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user ~/dev/my_app/app/templates/.
    cp ~/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user_base.html ~/dev/my_app/app/templates/.

You should now have an app/template/flask_user directory::

    ls -1 ~/dev/my_app/app/templates/flask_user

Expected output::

    _authorized_base.html
    _common_base.html
    _macros.html
    _public_base.html
    change_password.html
    change_username.html
    emails
        ...

Steps 1) through 3) only need to be performed once.

Editing Form template files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

After you've copied the Form template files,
you can edit any template file in your ``app/templates/flask_user/`` directory,
and change it to your liking.

All Flask-User templates extend from ``app/template/flask_user_layout.html``.
You can configure all Flask-User templates to extend from your own layout template by::

    editing app/template/flask_user/_common_base.html, and

    replacing:
        {% extends "flask_user_layout.html" %}

    with:
        {% extends "layout.html" %}

--------

.. _CustomizingFormClasses:

Customizing Form Classes
------------------------

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
            self.RegisterFormClass = CustomRegisterForm
            self.UserProfileFormClass = CustomUserProfileForm
            # NB: assign:  xyz_form = XyzForm   -- the class!
            #   (and not:  xyz_form = XyzForm() -- the instance!)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. seealso::

    :ref:`FlaskUserForms` shows a complete list of customizable forms.

    `Default forms are defined here
    <https://github.com/lingthio/Flask-User/blob/master/flask_user/forms.py>`_

.. note::

    Notice that in a simple use case like this, the form will work without customizing
    the accompanying view method. This is because WTForm's ``populate_obj()`` function
    knows how to move data from ``form.country.data`` to ``user.country``
    (as long as the property names are identical).

--------

.. _CustomizingFormValidators:

Customizing Form Validators
---------------------------

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

| Examples:
| `The default password_validator() <https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager.py#L219>`_.
| `The default username_validator() <https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager.py#L243>`_.

--------

.. _CustomizingFormViews:

Customizing Form Views
----------------------

View methods contain the code that prepares forms (on an HTTP GET) and process forms (on an HTTP POST).

Optionally, if you want to change the default behaviour, you can customize the view methods like so::


    # Customize Flask-User
    class CustomUserManager(UserManager):

        # Override or extend the default login view method
        def login_view(self):
            ...

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

.. warning::

    View methods perform lots of intricate operations, so use this feature with caution.
    Be sure to read the source code of the default view method and make sure you understand
    all that it does before attempting to modify its behavior.

    `Default view methods are defined here
    <https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager__views.py>`_

.. seealso:: :ref:`UserManager__Views` for a complete list of customizable view methods.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
