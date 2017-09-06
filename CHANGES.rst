Change history
==============

With **v0.9 (alpha and beta)** and **v1.0 (stable)** we
allow developers to customize Flask-User by overriding or extending
``UserManager`` properties and methods.

We re-wrote the TokenManager to support MongoDB IDs and adding parts of the password
to the token to invalidate tokens after a password change.

Password hashing can be completely configured using ``USER_PASSLIB_CRYPTCONTEXT_SCHEMES``
and USER_PASSLIB_CRYPTCONTEXT_KEYWORDS settings.

We modified the DbAdapter interface slightly to support MongoDB through MongoEngine
and custom DbAdapters.

We introduced the EmailMailer interface to support sending emails via SMTP, ``sendmail``,
SendGrid, and custom EmailMailers.

For all of the above we finally had to break compatibility with **v0.6 (stable)**.
For non-customized Flask-User apps, the porting is relatively straightforward.
See the 'Porting from v0.6 to v0.9+' section in our docs.

* v0.9.0 - First 1.0 alpha release

* v0.6.* - No longer compatible
