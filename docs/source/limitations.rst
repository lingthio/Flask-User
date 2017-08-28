===========
Limitations
===========

We want to be transparent about what this package can and can not do.


Python versions
---------------
Flask-User has been tested with Python |supported_python_versions_and|


Flask versions
--------------
Flask-User has been tested with Flask 0.10, 0.11 and 0.12


Supported Databases
-------------------
Flask-User uses a 'DatabaseAdapter' to shield its functionality from
the underlying database. It ships with a DatabaseAdapter for SQLAlchemy.

SQLAlchemy supports many SQL databases, including:

* Firebird
* Microsoft SQL Server
* MySQL
* Oracle
* PostgreSQL
* SQLite
* Sybase

The DatabaseAdapter can be subclassed to support other Databases.


Python data-model class names
-----------------------------
No known restrictions.

Flask-User relies on a User class and optionally on a UserEmail, UserInvitation and Role class.
The names of these classes can be anything you choose.


Python data-model attribute names
---------------------------------

If a single User data-model class is specified, the following attribute names are fixed::

    User.id
    User.password

    User.email                 # If FLASK_USER_ENABLE_EMAIL is True
    User.email_confirmed_at    # If FLASK_USER_ENABLE_EMAIL is True

    User.username              # If FLASK_USER_ENABLE_USERNAME is True

    User.active        # Optional, to enable activation/deactivation of users

    User.roles         # Optional, only for role-based authorization
    Role.id            # Optional, only for role-based authorization
    Role.name          # Optional, only for role-based authorization

    User.user_emails   # Optional, only for multiple emails per user


| If your existing code uses different attribute names you have two options:
| 1) Rename these attributes throughout your code base
| 2) Use Python's property and propery-setters to translate attribute names

::

    class User(db.Model, UserMixin):
            ...
        email_address = db.Column(db.String(255), nullable=False, unique=True)
            ...

        @property
        def email(self):
            return self.email_address   # on user.email: return user.email_address

        @email.setter
        def email(self, value):
            self.email_address = value  # on user.email='xyz': set user.email_address='xyz'


Note: Depending on Flask-User configuration settings, some attributes may move to other data-model classes,
such as UserEmail. These configurations will be discussed elsewhere.


SQL table names
---------------
No known restrictions


SQL column names
----------------
No known restrictions.

Note: Even though some Python data-model attribute names are fixed,
SQLAlchemy allows column names to be different from their corresponding attribute names.

::

    class User(db.Model, UserMixin)

        # Map Python Data-model attribute 'email' to SQL column 'email_address'
        email = db.Column('email_address', db.String(100))

        # Map Python Data-model attribute 'active' to SQL column 'is_active'
        active = db.Column('is_active', db.Boolean())


Primary keys
------------
The primary key of the User, UserEmail, UserInvitation and Role tables:

- must be named 'id'
- must be an Integer
- may not be a compound key.




