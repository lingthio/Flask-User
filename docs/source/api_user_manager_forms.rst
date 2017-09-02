.. _UserManager__Forms:

- :ref:`UserManagerForms`
- :ref:`UserManagerValidators`

.. _FlaskUserForms:

Flask-User forms
================

Below is a complete list of customizable Flask-User forms.

.. _AddEmailForm:

AddEmailForm
------------

.. autoclass:: flask_user.forms.AddEmailForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _ChangeUsernameForm:

ChangeUsernameForm
------------------

.. autoclass:: flask_user.forms.ChangeUsernameForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _EditUserProfileForm:

EditUserProfileForm
-------------------

.. autoclass:: flask_user.forms.EditUserProfileForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _ForgotPasswordForm:

ForgotPasswordForm
------------------

.. autoclass:: flask_user.forms.ForgotPasswordForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _InviteUserForm:

InviteUserForm
--------------

.. autoclass:: flask_user.forms.InviteUserForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _LoginForm:

LoginForm
---------

.. autoclass:: flask_user.forms.LoginForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _RegisterUserForm:

RegisterUserForm
----------------

.. autoclass:: flask_user.forms.RegisterUserForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _ResendEmailConfirmationForm:

ResendEmailConfirmationForm
---------------------------

.. autoclass:: flask_user.forms.ResendEmailConfirmationForm
    :no-undoc-members:
    :no-inherited-members:

--------

.. _ResetPasswordForm:

ResetPasswordForm
-----------------

.. autoclass:: flask_user.forms.ResetPasswordForm
    :no-undoc-members:
    :no-inherited-members:

.. _FlaskUserValidators:

Flask-User validators
=====================

.. _password_validator:

Password validator
------------------

.. autofunction:: flask_user.forms.password_validator

You can customize this validator as follows::

    # Define your custom validator
    def custom_password_validator(form, field):
        pass
        
    # Customize Flask-User
    class CustomUserManager(UserManager):
    
        def customize(self):
            self.password_validator = custom_password_validator
    
    user_manager = CustomUserManager(app, db, User)

.. _username_validator:

Username validator
------------------

.. autofunction:: flask_user.forms.username_validator

You can customize this validator as follows::

    # Define your custom validator
    def custom_username_validator(form, field):
        pass
        
    # Customize Flask-User
    class CustomUserManager(UserManager):
    
        def customize(self):
            self.username_validator = custom_username_validator
    
    user_manager = CustomUserManager(app, db, User)



