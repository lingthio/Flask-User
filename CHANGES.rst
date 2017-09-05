Change history
==============

With v0.9 (alpha and beta) and v1.0 (stable) we broke compatibility with v0.6
to allow developers to customize Flask-User by overriding or extending
``UserManager`` attributes and methods.

We modified the DbAdapter interface to support MongoDB through MongoEngine.

We introduced the EmailMailer interface to support sending emails via SMTP, ``sendmail`` and SendGrid.

* v0.9.0 - First 1.0 alpha release

* v0.6 - No longer compatible
