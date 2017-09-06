Change history
==============

With **v0.9 (alpha and beta)** and **v1.0 (stable)** we
allow developers to customize Flask-User by overriding or extending
``UserManager`` properties and methods.

We re-wrote the TokenManager to support MongoDB IDs and adding parts of the password
to the token to invalidate tokens after a password change.

We modified the DbAdapter interface to support MongoDB through MongoEngine.

We introduced the EmailMailer interface to support sending emails via SMTP, ``sendmail`` and SendGrid.

For all of the above we finally had to break compatibility with **v0.6 (stable)**.

* v0.9.0 - First 1.0 alpha release

* v0.6.* - No longer compatible
