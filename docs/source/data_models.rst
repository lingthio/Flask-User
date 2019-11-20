===========
Data-models
===========

Note: The code examples below assume the use of Flask-SQLAlchemy

User data-model
---------------
In its simplest form, Flask-User makes use of a single data-model class called User::

    # Define User data-model
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
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

The ``active`` property is optional. Add it if your application needs
to disable users. Flask-User will not let users login if this field is set to ``False``.

Flexible class name
-------------------
The ``User`` class name can be anything you want::

    class Client(db.Model, UserMixin):
        ...

    user_manager = UserManager(app, db, Client)

Fixed data-model property names
--------------------------------

The following data-model property names are fixed::

    User.id
    User.username           # optional
    User.password
    User.email              # optional
    User.email_confirmed_at # optional
    User.active             # optional
    User.roles              # optional
    User.user_emails        # optional
    Role.id                 # optional
    Role.name               # optional

The following property names are flexible::

    UserRoles.id            # optional
    UserRoles.user_id       # optional
    UserRoles.role_id       # optional

If you have existing code, and are unable to globally change the fixed property names,
consider using helper getters and setters as a bridge::

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

Flexible database column names
------------------------------
SQLAlchemy allows developers to specify a database column name different from their corresponding
data-model property name like so::

    class User(db.Model, UserMixin):
            ...
        # Map email property to email_address column
        email = db.Column('email_address', db.String(255), nullable=False, unique=True)

.. _RoleAndUserRoleDataModels:

Optional Role and UserRoles data-models
---------------------------------------

The optional ``Role`` and ``UserRoles`` data-models are only required for role-based authentication.
In this configuration, the ``User`` data-model must aslo define a ``roles`` relationship property.

The Role data-model holds the name of each role. This name will be matched to the @roles_required
function decorator in a **CASE SENSITIVE** manner.

The ``UserRoles`` data-model associates Users with their Roles.

::

    # Define the User data-model
    class User(db.Model, UserMixin):
            ...
        # Relationships
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

Roles are defined by adding rows to the Role table with a specific Role.name value.

::

    admin_role = Role(name='Admin')
    db.session.commit()

Users are assigned one or more roles by adding them to the User.roles property::

    # Create 'user007' user with 'secret' and 'agent' roles
    user1 = User(
        username='user007', email='admin@example.com', active=True,
        password=user_manager.hash_password('Password1'))
    user1.roles = [admin_role,]
    db.session.commit()


Optional UserEmail data-model
-----------------------------
Flask-User can be configured to allow for multiple emails per users, pointing to the same user account
and sharing the same password. In this configuration, a separate UserEmail data-model class must be specified.

::

    # Define User data-model
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)

        # User Authentication fields
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False)

        # Relationship
        user_emails = db.relationship('UserEmail')


    # Define UserEmail data-model
    class UserEmail(db.Model):
        __tablename__ = 'user_emails'
        id = db.Column(db.Integer, primary_key=True)

        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        user = db.relationship('User', uselist=False)

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, server_default='0')


    # Setup Flask-User
    user_manager = UserManager(app, User, UserEmailClass=UserEmail)

The ``is_primary`` property defines which email receives account notification emails.


