Authorization
=============
Authorization is the process of specifying and enforcing access rights of users to resources.

Flask-User offers role based authorization through the use of function decorators:

* `@login_required`_
* `@roles_required`_

@login_required
---------------
Decorate a view function with @login_required to ensure that
the user is logged in before accessing that particular page:

::

    from flask.ext.user import login_required

    @login_required
    @route('/profile')
    def profile_page():
        # render the user profile page

| Flask-User relies on Flask-Login to implement and offer the @login_required decorator along with its underlying current_user.is_authenticated() implementation.
| See the `Flask-Login Documentation <https://flask-login.readthedocs.org/en/latest/#flask.ext.login.login_required>`_

@roles_required
---------------
Decorate a view function with @roles_required to ensure that
the user is logged in and has sufficient role-based access rights that particular page.

In the example below the current user is required to have the 'admin' role::

    from flask.ext.user import roles_required

    @roles_required('admin')
    @route('/admin/dashboard')
    def admin_dashboard():
        # render the admin dashboard

Note: Comparison of role names is case sensitive, so 'Member' will NOT match 'member'.

Multiple string arguments -- the AND operation
~~~~~~~~

The @roles_required decorator accepts multiple strings if the current_user is required to have
**ALL** of these roles.

In the example below the current user is required to have the **ALL** of these roles::

    @roles_required('dark', 'tall', 'handsome')
    # Multiple string arguments require ALL of these roles

Multiple string arguments represent the 'AND' operation.

Array arguments -- the OR operation
~~~~~~~~

The @roles_required decorator accepts an array (or a tuple) of roles.

In the example below the current user is required to have **One or more** of these roles::

    @roles_required(['funny', 'witty', 'hilarious'])
    # Notice the usage of square brackets representing an array.
    # Array arguments require at least ONE of these roles.

AND/OR operations
~~~~~~~~
The potentially confusing syntax described above allows us to construct
complex AND/OR operations.

| In the example below the current user is required to have
| either (the 'starving' AND the 'artist' roles)
| OR (the 'starving AND the 'programmer' roles)

::

    @roles_required('starving', ['artist', 'programmer'])
    # Ensures that the user is ('starving' AND (an 'artist' OR a 'programmer'))

Note: The nesting level only goes as deep as this example shows.



Required Tables
--------------

For @login_required only the User model is required

For @roles_required, the database must have the following models:

* The usual User model with an additional 'roles' relationship field
* A Role model with at least one string field called 'name'
* A UserRoles association model with a 'user_id' field and a 'role_id' field

Here's a SQLAlchemy example::

    # Define User model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=True, unique=True)
        ...
        roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))

    # Define Role model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define UserRoles model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

Roles are defined by adding rows to the role table with a specific Role.name value.

::

    # Create 'user007' user with 'secret' and 'agent' roles
    user1 = User(username='user007', email='user007@example.com', is_enabled=True,
                 password=user_manager.hash_password('Password1'))
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

Up Next
-------
:doc:`roles_required_app`



