======
F.A.Q.
======

| **Q: Can I see a preview?**
| A: Yes you can: `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_

| **Q: What's the relationship between Flask-User and Flask-Login?**
| A: Flask-User manages **users** and uses Flask-Login to manage **user sessions**.
| Flask-User is built on top of Flask-Login to provide the register/login/change forms and to manages the email verification, the user authentication and the user authorization.

| **Q: What are the differences between Flask-User and Flask-Security?**
| A: The main reason why I wrote Flask-User was because I found it difficult to customize
  Flask-Security messages and functionality (in 2013) and because it didn't offer
  Username login, multiple emails per user, and Internationalization.

Flask-User has been designed with :doc:`Full customization <customizing>` in mind
and additionally offers Username login and Internationalization.
It exists since December 2013 and contains 661 statements with a 98% test coverage.

Flask-Security has been around since at least March 2012
and additionally offers Json/AJAX, MongoDB, Peewee, and Basic HTTP Authentication.

| **Q: Can users login with usernames and email addresses?**
| A: Yes.
  Flask-User can be configured to enable usernames, email addresses or both.
  If both are enabled,
  users can log in with either their username or their email address.

| **Q: Does Flask-User work with existing hashed passwords?**
| A: Yes. It supports the following:
| - passwords hashed by any ``passlib`` hashing algorithm (via a config setting)
| - passwords hashed by Flask-Security (via a config setting)
| - custom password hashes (via custom functions)

| **Q: What databases does Flask-User support?**
| A: Any database that SQLAlchemy supports (via SqlAlchemyAdapter)
| and other databases (via custom DBAdapters)

Flask-User shields itself from database operations through a DBAdapter.
It ships with a SQLAlchemyAdapter, but the API is very simple, so other adapters
can be easily added. See :ref:`DbAdapterInterface`.



