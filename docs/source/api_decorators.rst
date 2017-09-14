.. _ViewDecorators:

View decorators
===============
Flask-User view decorators serve as the gatekeepers to prevent
unauthenticated or unauthorized users from accessing certain views.

.. important::

    The @route decorator must always be
    the **first** view decorator in a list of view decorators
    (because it's used to map the function *below itself* to a URL).

.. autofunction:: flask_user.decorators.login_required
.. autofunction:: flask_user.decorators.roles_accepted
.. autofunction:: flask_user.decorators.roles_required
.. autofunction:: flask_user.decorators.allow_unconfirmed_email
