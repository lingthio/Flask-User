.. _limitations:

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
Flask-User makes use of DbAdapters to support different databases.

It ships with a SQLAlchemyDbAdapter to support a wide range of SQL databases via Flask-SQLAlchemy
(Firebird, Microsoft SQL Server, MySQL, Oracle, PostgreSQL, SQLite, Sybase and more).

It ships with a MongoEngineDbAdapter to support MongoDB databases via Flask-MongoEngine.

Other DbAdapter interfaces can be implemented to support other Databases.


Flexible data-model class names
-------------------------------
No known restrictions.

Flask-User relies on a User class and optionally on a Role, UserRoles, UserEmail and/or UserInvitation class.
The names of these classes can be anything you choose::

    class Client(db.Model, UserMixin):
        ...

    user_manager = UserManager(app, db, Client)


Fixed data-model attribute names
--------------------------------

The following data-model attribute names are fixed::

    User.id
    User.password
    User.username                   # optional
    User.email                      # optional
    User.email_confirmed_at         # optional
    User.active                     # optional
    User.roles                      # optional
    User.user_emails                # optional
    UserEmail.email                 # optional
    UserEmail.email_confirmed_at    # optional
    Role.id                         # optional
    Role.name                       # optional

The following attribute names are flexible::
    UserEmail.id                    # optional
    UserRoles.id                    # optional
    UserRoles.user_id               # optional
    UserRoles.role_id               # optional

If you have existing code, and are unable to globally change a fixed attribute name,
consider using Python's getter and setter properties as a bridge::

    class User(db.Model, UserMixin):
            ...
        # Existing code uses email_address instead of email
        email_address = db.Column(db.String(255), nullable=False, unique=True)
            ...

        # define email getter
        @property
        def email(self):
            return self.email_address   # on user.email: return user.email_address

        # define email setter
        @email.setter
        def email(self, value):
            self.email_address = value  # on user.email='xyz': set user.email_address='xyz'


SQL table names
---------------
No known restrictions when using SQLAlchemy.

SQLAlchemy allows table names to be different from their corresponding class names::

    class User(db.Model, UserMixin):
        __tablename__ = 'clients'
            ....

SQL column names
----------------
No known restrictions when using SQLAlchemy.

SQLAlchemy allows column names to be different from their corresponding attribute names::

    class User(db.Model, UserMixin):
            ...
        # Map Python Data-model attribute 'email' to SQL column 'email_address'
        email = db.Column('email_address', db.String(100))

        # Map Python Data-model attribute 'active' to SQL column 'is_active'
        active = db.Column('is_active', db.Boolean())


Primary keys
------------
Without customization, the primary key of the User, UserEmail, UserInvitation and Role tables:

- must be named ``id``
- must be of type ``int``
- may not be a compound key.

Customization may offer a way to use primary keys named other than ``id``.

Customization may offer a way to use primary keys of types other than ``int``
as long as they can be converted into an ``str``.

As an example, the :ref:`MongoEngineDbAdapter` accepts primary keys of type ObjectID,
which can be converted to a string with ``str(id)``.




