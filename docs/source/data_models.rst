===========
Data-models
===========

Note: The code examples below assume the use of Flask-SQLAlchemy

User data-model
---------------
In its simplest form, Flask-User makes use of a single User data-model class::

    # Define User data-model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User Authentication fields
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False)

        # User fields
        active = db.Column(db.Boolean()),
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

Optional UserEmail data-model
-----------------------------
Flask-User can be configured to allow for multiple emails per users, pointing to the same user account
and sharing the same password. In this configuration, a separate UserEmail data-model class must be specified.

The 'is_primary' attribute defines with email receives account notification emails.

::

    # Define User data-model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User Authentication fields
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False)

        # Relationship
        user_emails = db.relationship('UserEmail')


    # Define UserEmail data-model
    class UserEmail(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        user = db.relationship('User', uselist=False)

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, server_default='0')


    # Setup Flask-User
    user_manager = UserManager(app, User, UserEmailClass=UserEmail)


Optional Role and UserRoles data-models
---------------------------------------

The Role and UserRoles data-models are only required for role-based authentication.
In this configuration, the User data-model MUST define a 'roles' relationship attribute.

The Role data-model holds the name of each role. This name will be matched to the @roles_required
function decorator in a CASE SENSITIVE manner.

The UserRoles data-model associates Users with their Roles.

::

    # Define the User data-model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        ...

        # Relationships
        roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))

    # Define the Role data-model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles data-model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


Fixed attribute names
---------------------
All the attribute names mentioned above (except `first_name` and `last_name`) are fixed
(they must be named this way).

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


Flexible database column names
------------------------------
SQLAlchemy allows the database column name to be different from the data-model attribute name.
To use the data-model attribute `email` with the database column name `email_address`::

    email = db.Column('email_address', db.String(255), nullable=False, unique=True)

