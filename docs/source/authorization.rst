Role-based Authorization
========================
Authorization is the process of specifying and enforcing access rights of users to resources.

Flask-User offers role-based authorization through the use of the ``@roles_required`` decorator.

@roles_required
---------------
If a view function is decorated with the ``@roles_required`` decorator, the user:

- must be logged in, and
- must be associated with the specified role names.

If any of these conditions is not met, an 'Unauthorized access' error message will be shown
and the user will be redirected to the ``USER_UNAUTHORIZED_ENDPOINT``.

In the example below the current user is required to be logged in and to be associated with the role named 'Admin'::

    from flask_user import roles_required

    @route('/admin/dashboard')    # @route() must always be the outer-most decorator
    @roles_required('Admin')
    def admin_dashboard():
        # render the admin dashboard

Note: Comparison of role names is case sensitive, so ``'Admin'`` will NOT match ``'admin'``.

Simple AND/OR operations
~~~~~~~~~~~~~~~~~~~~~~~~

The @roles_required decorator accepts one or more role names.
At the decorator level, if multiple role names are specified here,
the user must have **all** the specified roles.
This is the AND operation.

At the argument level, each item may be a role name or a list or role names.
If a list of role names is specified here,
the user mast have **any one** of the specified roles to gain access.
This is the OR operation.

In the example below, the user must always have the ``'Starving'`` role,
AND either the ``'Artist'`` role OR the ``'Programmer'`` role::

    # Ensures that the user is ('Starving' AND (an 'Artist' OR a 'Programmer'))
    @roles_required('Starving', ['Artist', 'Programmer'])

Note: The nesting level only goes as deep as this example shows.


Required Role and UserRoles data-models
---------------------------------------
The @roles_required decorator depends the ``Role`` and ``UserRoles`` data-models
(in addition to the ``User`` data-model).

See the docs on :ref:`Role and UserRoles data-models<RoleAndUserRoleDataModels>`.

Example App
-----------
The :doc:`basic_app` demonstrates the use of the ``@roles_required`` decorator.
