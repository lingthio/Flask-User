===============
User DataModels
===============

Flask-User distinguishes between the following groups of user information:

1. User Authentication information such as username and password
2. User Email information such as email address and confirmed_at
3. User information such as first_name and last_name
4. User Role information

Flask-User allows the developer to store Authentication, Email and User information in one DataModel or across several DataModels.

Flask-User requires User Role information to be stored in a Role DataModel and an UserRole association table.


All-in-one User DataModel
-------------------------
If you'd like to store all user information in one DataModel, use the following:

::

    # Define User model. Make sure to add flask.ext.user UserMixin !!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User Authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

        # User Email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name = db.Column(db.String(50), nullable=False, default='')

        def is_active(self):
          return self.is_enabled

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User


Separated User/UserAuth DataModel
---------------------------------
If you'd like to store User Authentication information separate from User information, use the following:

::

    # Define User DataModel
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name = db.Column(db.String(50), nullable=False, default='')

        def is_active(self):
          return self.is_enabled

    # Define UserAuth DataModel. Make sure to add flask.ext.user UserMixin!!
    class UserAuth(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

        # Relationships
        user = db.relationship('User', uselist=False, foreign_keys=user_id)

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User, UserAuthClass=UserAuth)
    user_manager = UserManager(db_adapter, app)


UserEmail DataModel
-------------------
Separating User Email information from User information allows for support of multiple emails per user.

It can be applied to both the All-in-one User DataModel and the separated User/UserAuth DataModel

::

    # Define User DataModel. Make sure to add flask.ext.user UserMixin !!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        ...
        # Relationship
        user_emails = db.relationship('UserEmail')

    # Define UserEmail DataModel.
    class UserEmail(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        is_primary = db.Column(db.Boolean(), nullable=False, default=False)

        # Relationship
        user = db.relationship('User', uselist=False)


User Roles DataModel
--------------------

The Roles table holds the name of each role. This name will be matched to the @roles_required
function decorator in a CASE SENSITIVE manner.

::

    # Define the Role DataModel
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

The UserRoles DataModel associates Users with their Roles.

It can be applied to both the All-in-one User DataModel and the separated User/UserAuth DataModel

::

    # Define the User DataModel. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        ...
        # Relationships
        roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))

    # Define the UserRoles DataModel
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))



Porting Flask-User v0.5 applications to Flask-User v0.6
-------------------------------------------------------
For applications using the All-in-one User DataModel, no changes are required.

For applications using the separated User/UserAuth DataModel, v0.6 maintains backward compatibility,
but future versions may not, and it is therefore recommended to make the following changes:

* Change ``SQLAlchemyAdapter(db, User, UserProfile=UserProfile)`` to
  ``SQLAlchemyAdapter(db, UserProfile, UserAuth=User)``.

* Move the UserMixin from ``class User(db.Model)`` to ``class UserProfile(db.Model, UserMixin)``

* Move the ``roles`` relationship from class User to class UserProfile.

* Move the UserRoles.user_id association from 'user.id' to 'user_profile.id'.
  This requires a DB schema change.

* If it's possible to rename table names, please rename User to UserAuth and UserProfile to User.
  This would require a DB schema change.
