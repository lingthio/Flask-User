Porting Customizations
======================

.. include:: includes/submenu_defs.rst
.. include:: includes/porting_submenu.rst

--------

Read this if you have:

    - Specified custom Form classes (the .py files)
    - Specified custom View functions
    - Specified custom Password or username validators
    - Specified a custom TokenManager
    - Used the optional UserAuth class

This topic assumes that you completed the porting tasks described in :doc:`porting_basics`.

UserManager customization
-------------------------
In v0.6, Flask-User was customized by adding parameters to the UserManager()
instantiation. For example::

    # Setup Flask-User
    db_adapter = SQLAlchemyAdaper(db, User)
    user_manager = UserManager(db_adapter, app,
        register_form = CustomRegisterForm,
        register_view_function = custom_register_view,
        password_validator = custom_password_validator,
        token_manager = CustomTokenManager())

In v1.0, Flask-User is customized by:
- Extending the ``CustomUserManager`` class
- Setting properties in its ``customize()`` method
- Overriding or extending methods

::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Override properties
            self.RegisterFormClass = CustomRegisterForm
            self.token_manager = CustomTokenManager(app)

        # Override methods
        def register_view(self):
            ...

        # Extend methods
        def password_validator(self):
            super(CustomUserManager, self).password_validator()
                ...

In v1.0, almost all ``UserManager`` initiation parameters have been obsolted and
now only accepts the following:

- Required parameters ``app``, ``db`` and ``UserClass``.
- Optional keyword parameters: ``UserEmailClass`` and ``UserInvitationClass``.

.. seealso:: :ref:`UserManagerClass`

Data-model changes
------------------
| The **email_confirmed_at** property has been renamed.
| See :doc:`porting_basics` for porting steps and :doc:`porting_advanced` for an advanced option.

| The **UserAuth class** has been deprecated.
| Support for the optional v0.6 ``UserAuth`` class has been dropped in v1.0+ to simplify the Flask-User source code
    and make it more readable and easier to customize.

See :doc:`porting_advanced` for a workaround if you can not merge the UserAuth and User classes.

| The **UserInvitation class** has been renamed.
| The v0.6 ``UserInvite`` class has been renamed to ``UserInvitation`` in v1.0+
    to reflect that it's an object and not an action.

Use the following approach to use the new class name while keeping the old table name::

    class UserInvitation(db.Model):
        __tablename__ = 'user_invite'
            ...

Password method changes
-----------------------
| We changed the ``verify_password()`` API
| from v0.6 ``verify_password(password, user)``
| to v1.0+ ``verify_password(password, password_hash)``
| to keep data-model knowledge out of the PasswordManager.

Please change::

    user_manager.verify_password(password, user)

into::

    verify_password(password, user.password)


@confirm_email_required decorator deprecated
--------------------------------------------
The ``@confirm_email_required`` view decorator has been deprecated for security reasons.

In v0.6, the ``USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL`` setting removed
confirmed email protection for all the views and required developers to re-protect
the vulnerable views with ``@confirm_email_required``.

In v1.0+ we adopt the opposite approach where the (renamed) ``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL=True``
setting continues to protect all the views, except those decorated with the
new ``@allow_unconfirmed_email`` decorator.


Contact us
----------
We believe this concludes the Porting steps for for applications with a high degree of
Flask-User customizations.

If, after reading :doc:`porting_advanced`,
you still think this page is incomplete, please email ling.thio@gmail.com.

--------

.. include:: includes/porting_submenu.rst
