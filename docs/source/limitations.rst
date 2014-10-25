===========
Limitations
===========

As you will soon experience, a great many things in Flask-User can be customized
so it can behave exactly the way you want it to behave. But this documentation
would not be complete without also discussing what its limitations are.


Python versions
--------
Flask-User has been tested with Python 2.6, 2.7, 3.3 and 3.4


Flask versions
--------
Flask-User has been tested with Flask 0.10


Supported Databases
--------
Out-of-the box, Flask-User ships with a SQLAlchemyAdapter, allowing for support of any
SQL database that SQLAlchemy v0.9 supports, including:

Drizzle, Firebird, Microsoft SQL Server, MySQL, Oracle, PostgreSQL, SQLite, Sybase

See http://docs.sqlalchemy.org/en/rel_0_9/dialects/index.html for a full list

Flask-User does abstract DB interactions through a 'DbAdapter' class,
so support for other databases is possible by writing a DbAdapter extension class.


User model field names
--------

Though the User model table name, and the primary key field name can be customized,
the remaining field names MUST be named as follows:

::

  # User model
  user.username                 # Required only if USER_ENABLE_USERNAME is True
  user.email                    # Required only if USER_ENABLE_EMAIL is True
  user.confirmed_at             # Required only if USER_ENABLE_CONFIRM_EMAIL is True
  user.password                 # Required
  user.reset_password_token     # Required
  user.roles                    # Required only if @roles_required is used
  user.user_auth                # Required only if a UserAuthClass is specified in DBAdapter()


Role model field names
--------

Though the User model table name, and the primary key field name can be customized,
the remaining field names MUST be named as follows:

::

  # Role model
  role.name                     # Required if @roles_required is used


Primary keys
--------

Though the primary key fields of the User and Role models may be named differently than 'id',
the primary key type MUST be an integer and can not be a compound key.

