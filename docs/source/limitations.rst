===========
Limitations
===========

As you will soon experience, a great many things in Flask-User can be customized
so it can behave exactly the way you want it to behave. But this documentation
would not be complete without first discussing what its limitations are.


Supported Databases
-------------------
Out-of-the box, Flask-User ships with a SQLAlchemyAdapter, allowing
support for many SQL databases including:

* Drizzle
* Firebird
* Microsoft SQL Server
* MySQL
* Oracle
* PostgreSQL
* SQLite
* Sybase

For a full list see http://docs.sqlalchemy.org/en/rel_0_9/dialects/index.html

Flask-User does abstract DB interactions through a 'DbAdapter' class,
so support for other databases is possible by writing a DbAdapter extension class.

Database table names
--------------------
No known restrictions


Database column names
---------------------
No known restrictions


Primary keys
------------
The primary key of the User table must be an Integer and may not be a compound key.


Data model field names
----------------------
Flask-User requires specific Data model field names, but accepts
arbitrary names for the Database column names.

Required Data model field names:

::

    # User authentication information
    User.username              or  UserAuth.username
    User.password              or  UserAuth.password
    User.reset_password_token  or  UserAuth.reset_password_token
                                   UserAuth.user_id

    # User email information
    User.email                 or  UserEmail.email
    User.confirmed_at          or  UserEmail.confirmed_at
                                   UserEmail.user_id

    # User information
    User.active

    # Relationships
    User.roles                 # only if @roles_required is used

    # Role information
    Role.name


SQLAlchemy offers a way to use specific Data model field names
with different Database column names:

::

    class User(db.Model, UserMixin)

        # Map Data model field 'email' to Database column 'email_address'
        email = db.Column('email_address', db.String(100))

        # Map Data model field 'active' to Database column 'is_active'
        active = db.Column('is_active', db.Boolean())


Flask versions
--------------
Flask-User has been tested with Flask 0.10


Python versions
---------------
Flask-User has been tested with Python 2.6, 2.7, 3.3 and 3.4


