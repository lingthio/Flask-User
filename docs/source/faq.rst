======
F.A.Q.
======

| **Q: What are the differences between Flask-User and Flask-Security?**
| A: The main reason why we wrote Flask-User is because we found it difficult to customize
  Flask-Security messages and functionality.

Flask-Security has been around since at least March 2012
and additionally offers Json/AJAX, MongoDB, Peewee, and Basic HTTP Authentication.

FLask-User has been designed with :doc:`Full customization <customization>` in mind,
exists since December 2013, and additionally offers Username login and Internationalization.
The code base contains 661 statements with a 98% test coverage.

| **Q: Can users login with usernames and email addresses?**
| A: Yes.
  Flask-User can be configured to enable usernames, email addresses or both.
  If both are enabled,
  users can log in with either their username or their email address.

| **Q: Does Flask-User work with existing hashed passwords?**
| A: Yes. It supports the following:
| - passwords hashed with any ``passlib`` hashing algorithms (via a config setting)
| - passwords hashed by Flask-Security (via a config setting)
| - custom password hashes (via custom functions)




