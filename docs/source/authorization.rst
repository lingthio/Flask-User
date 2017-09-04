Authorization
=============
Authorization is the process of specifying and enforcing access rights of users to resources.

Flask-User offers role based authorization through the use of function decorators:

* `@login_required`_
* `@roles_required`_

@login_required
---------------
Decorate a view function with ``@login_required`` decorator to ensure that
the user is logged in before accessing that particular page
or an 'Unauthorized' error message will be shown.

::

    from flask_user import login_required

    @route('/profile')    # @route() must always be the outer-most decorator
    @login_required
    def profile_page():
        # render the user profile page

| Flask-User relies on Flask-Login to implement and offer the @login_required decorator along with its underlying current_user.is_authenticated() implementation.
| See the `Flask-Login Documentation <https://flask-login.readthedocs.org/en/latest/#flask.ext.login.login_required>`_

@roles_required
---------------
If a view function is decorated with the ``@roles_required`` decorator,
the use must be logged in to access that page
or an 'Unauthorized' error message will be shown.

In the example below the current user is required to have a role named 'Admin'::

    from flask_user import roles_required

    @route('/admin/dashboard')    # @route() must always be the outer-most decorator
    @roles_required('Admin')
    def admin_dashboard():
        # render the admin dashboard

Note: Comparison of role names is case sensitive, so ``'Admin'`` will NOT match ``'admin'``.

Simple AND/OR operations
~~~~~~~~~~~~~~~~~~~~~~~~

The @roles_required decorator accepts one or more role names.
At this level, if multiple role names are specified,
the user is required to have **all** the specified roles.
This is the AND operation.

Each list item at the previous level may be either a role name or a list or role names.
At this level, if a list of role names is specified,
the use is may have **any one** of the specified roles to gain access.
This is the OR operation.

In the example below, the user must always have the ``'Starving'`` role,
plus either the ``'Artist'`` role or the ``'Programmer'`` role::

    # Ensures that the user is ('Starving' AND (an 'Artist' OR a 'Programmer'))
    @roles_required('Starving', ['Artist', 'Programmer'])

Note: The nesting level only goes as deep as this example shows.


Required Tables
---------------

For @login_required only the User data-model is required

For @roles_required, the database must have the following data-models:

* The usual User data-model with an additional 'roles' relationship field
* A Role data-model with at least one string field called 'name'
* A UserRoles association data-model with a 'user_id' field and a 'role_id' field

Here's a SQLAlchemy example::

    # Define User data-model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=True, unique=True)
        ...
        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define Role data-model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define UserRoles data-model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

Roles are defined by adding rows to the role table with a specific Role.name value.

::

    # Create 'user007' user with 'secret' and 'agent' roles
    user1 = User(username='user007', email='user007@example.com', is_enabled=True,
                 password=user_manager.password_manager.hash_password('Password1'))
    role1 = Role(name='secret')
    role2 = Role(name='agent')

Users are assigned one or more roles by adding a records to the 'user_roles' table,
binding a User to one or more Roles.

::

    # Bind user to two roles
    user1.roles.append(role1)
    user1.roles.append(role2)

    # Store user and roles
    db.session.add(user1)
    db.session.commit()

