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

* v1.0.1.1 - Alpha release

* v0.6.* - Incompatible production version
