.. _limitations:

===========
Limitations
===========

We want to be transparent about what this package can and can not do.


Python versions
---------------
Flask-User has been tested with Python 2.7, 3.4, 3.5, 3.6, 3.7 and 3.8.


Flask versions
--------------
Flask-User works with Flask 0.9+


Supported Databases
-------------------
Flask-User makes use of DbAdapters to support different databases.

It ships with a SQLDbAdapter to support a wide range of SQL databases via Flask-SQLAlchemy
(Firebird, Microsoft SQL Server, MySQL, Oracle, PostgreSQL, SQLite, Sybase and more).

It ships with a MongoDbAdapter to support MongoDB databases via Flask-MongoEngine.

Custom DbAdapters can be implemented to support other Databases.


Supported Email Mailers
-----------------------
Flask-User makes use of EmailAdapters to send email via several platforms.

It ships with a SMTPEmailAdapter a SendmailEmailAdapter and a SendGridEmailAdapter
to send emails via SMTP, ``sendmail`` and SendGrid.

Custom EmailAdapters can be implemented to support other Email Mailers.


Fixed app.user_manager name
---------------------------

An initialized UserManager() instance will assign itself to the ``app.user_manager`` property.
This ``app.user_manager`` name can not be changed.


Fixed data-model property names
--------------------------------

The following data-model property names are fixed::

    User.id
    User.password
    User.username                      # optional
    User.email                         # optional
    User.email_confirmed_at            # optional
    User.active                        # optional
    User.roles                         # optional
    User.user_emails                   # optional
    Role.name                          # optional
    UserEmail.id                       # optional
    UserEmail.email                    # optional
    UserEmail.email_confirmed_at       # optional
    UserInvitation.id                  # optional
    UserInvitation.email               # optional
    UserInvitation.invited_by_user_id  # optional


If you have existing code, and are unable to globally change a fixed property name,
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


Flexible data-model class, SQL table, and SQL column names
----------------------------------------------------------------
| Data-model class names are unrestricted.
| SQL table names are unrestricted.
| SQL column names are unrestricted.

Here is an example of a data-model class with different class, table and column names::

    # Use of the Member class name (instead of User)
    class Member(db.Model, UserMixin):

        # Use of the 'members' SQL table (instead of 'users')
        __tablename__ = 'members'
            ...
        # Use of the 'email_address' SQL column (instead of 'email')
        email = db.Column('email_address', db.String(255), nullable=False, unique=True)

    # Setup Flask-User
    user_manager = UserManager(app, db, Member)    # Specify the Member class


Primary keys
------------
Even though Flask-User relies on the following:

- Primary key is a single property named ``id``.
- ``id`` properties are:

  - integers,
  - or strings,
  - or offer a string representation with ``str(id)``.

Developers can still support primary key properties named other than ``id``::

    class User(db.Model, UserMixin):
        # Composite primary key
        pk = db.Column(db.Integer, primary_key=True)
            ...
        # Map: id=user.id to: id=user.pk
        @property
        def id(self):
            return self.pk

        # Map: user.id=id to: user.pk=id
        @id.setter
        def id(self, value):
            self.pk = value

Developers can still support composite primary keys::

    class User(db.Model, UserMixin):
        # Composite primary key
        pk1 = db.Column(db.Integer, primary_key=True)
        pk2 = db.Column(db.String, primary_key=True)
            ...
        # Map:  id=user.id  to:  id=str(pk1)+'|'+pk2
        @property
        def id(self):
            return str(self.pk1)+'|'+self.pk2    # Naive concatenation

        # Map:  user.id=str(pk1)+'|'+pk2  to:  user.pk1=pk1; user.pk2=pk2;
        @id.setter
        def id(self, value):
            items = value.split('|',1)    # Naive split
            self.pk1 = int(items[0])
            self.pk2 = items[1]

Developers can customize the TokenManager to accept IDs without string representations.
