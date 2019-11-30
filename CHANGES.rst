Change history
==============

With **v1.0** we simplified customization
by allowing developers to override or extend ``UserManager`` properties and methods.

We increased security by having the TokenManager accept parts of passwords,
in addition to the user ID, to invalidate tokens after a password has changed.
The TokenManager now also excepts IDs other than small integers.

Hashlib password hashing is completely configurable through two config settings:
``USER_PASSLIB_CRYPTCONTEXT_SCHEMES`` and ``USER_PASSLIB_CRYPTCONTEXT_KEYWORDS``.
Example: ``SCHEMES=['bcrypt', 'argon2']``, ``KEYWORDS=dict(bcrypt__rounds=12, argon2__memory_cost=512)``.

We added support for MongoDBs (through Flask-MongoEngine)
and for DynamoDBs (through Flask-Flywheel).

We introduced the EmailAdapter interface to support sending emails not only via SMTP,
but also via ``sendmail``, SendGrid, and custom EmailAdapters.

For all of the above we finally had to break compatibility with **v0.6 (stable)**.
For non-customized Flask-User apps, the porting is relatively straightforward.
See the 'Porting from v0.6 to v1.0+' section in our docs.

* v1.0.2.3:
    * Display "flash" message when change password fails
      (see `#239 <https://github.com/lingthio/Flask-User/issues/239>`_).
* v1.0.2.2:
    * Added new settings to ``UserManager`` which can be used to customize page
      footers: ``USER_APP_VERSION``, ``USER_CORPORATION_NAME``, and
      ``USER_COPYRIGHT_YEAR`` (see `#280 <https://github.com/lingthio/Flask-User/issues/280>`_).
    * Fixed crash when one tried to change username and ``USER_ENABLE_EMAIL``
      was falsy (see `#267 <https://github.com/lingthio/Flask-User/issues/267>`_).
* v1.0.2.1:
    * Added Slovak, Polish and Ukrainian translations.
    * Fixed bug in "Password Changed" email template (see `#250 <https://github.com/lingthio/Flask-User/issues/250>`_).
    * Fixed crash when USER_ENABLE_INVITE_USER is set (see `#223 <https://github.com/lingthio/Flask-User/issues/223>`_).
    * Updated min allowed version of ``passlib`` from 1.6 to 1.7 (see `#266 <https://github.com/lingthio/Flask-User/issues/266>`_).
* v1.0.2.0 - Production/Stable release. Dropped support for Python 2.6 and 3.3.
* v1.0.1.5 - Removed callbacks/auth0.
* v1.0.1.4 - Fixed calls to get_primary_user_email_object().
* v1.0.1.3 - Changed custom form class attribute names from something like ``self.register_form`` to something like ``self.RegisterFormClass``
* v1.0.1.2 - Use app.permanent_session_lifetime to limit user session lifetime.
* v1.0.1.1 - Alpha release. Breaks backward compatibility with v0.6.

* v0.6.* - Previous version. No longer supported.
* v0.5.* - Previous version. No longer supported.

