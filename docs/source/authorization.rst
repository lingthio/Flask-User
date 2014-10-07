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
    def profile_page()
        # render the user profile page

| Flask-User relies on Flask-Login to implement and offer the @login_required decorator along with its underlying current_user.is_authenticated() implementation.
| See the `Flask-Login Documentation <https://flask-login.readthedocs.org/en/latest/#flask.ext.login.login_required>`_

@roles_required
---------------
Decorate a view function with @roles_required to ensure that
the user is logged in and has sufficient role-based access rights that particular page:

::

    from flask.ext.user import roles_required

    @roles_required('admin')
    @route('/admin/dashboard')
    def admin_dashboard()
        # render the admin dashboard

| The @roles_required decorator accepts a variable list of arguments.
| Each argument must either be:
| - a role name, or
| - a list of role names (tuples are OK too)

| The argument list represent the AND operation: ``role1, role2, role3``
| A list of role names represents the OR operation: ``[role1, role2, role3]``
| See examples below to make things more clear

::

    @roles_required('manager')
    # Ensures that a user is assigned to the 'manager' role.

::

    @roles_required('tall', 'dark', 'handsome')
    # Ensures that a user must be ALL of these things.
    # This is the AND operation.

::

    @roles_required(['funny', 'witty', 'hilarious'])
    # Notice the usage of square brackets representing a list.
    # Ensures that a user must be ONE of these things.
    # This is the OR operation.

| Why this somewhat confusing syntax?
| Because it allows us to perform powerful AND/OR operations on roles:

::

    @roles_required('starving', ['artist', 'programmer'])
    # Ensures that the user is ('starving' AND (an 'artist' OR a 'programmer'))
    # The nesting level only goes as deep as this example shows.


Note: Comparison of role names is case sensitive, so 'Member' will NOT match 'member'.

Implementation
--------------

The database must contain the following tables:
* The usual 'user' table
* A 'role' table with at least one field called 'name'
* A 'user_roles' pivot table with a 'user_id' field and a 'role_id' field

Roles are defined by adding rows to the 'role' table with a specific Role.name value.

Users are assigned roles by adding a records to the 'user_roles' table,
binding a User to one or more Roles.

Here's a SQLAlchemy example::

    # Define User model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=True, unique=True)
        ...

    # Define Role model
    class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define UserRoles model
    class UserRoles(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    # Create 'user007' user with 'secret' and 'agent' roles
    role1 = Role(name='secret')
    role2 = Role(name='agent')
    user1 = User(username='user007', email='user007@example.com', active=True,
            password=user_manager.hash_password('Password1'))
    user1.roles.append(role1)
    user1.roles.append(role2)
    db.session.add(user1)
    db.session.commit()

See :doc:`recipes_roles_required_app`


