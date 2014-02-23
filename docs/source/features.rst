========
Features
========

+-----------------------------------+---------------------------------------+
| * Reliable and Feature Rich       | * Register with email address         |
| * Easy to Install and Setup       | * Register with username              |
| * Fully Customizable              | * Confirm email address               |
| * Data model agnostic             | * Login and Logout                    |
|   (provide your own User model)   | * Change username                     |
| * Database ORM abstraction        | * Change password                     |
|   (SQLAlchemyAdapter provided)    | * Forgot password and Reset password  |
| * Internationalization Ready      |                                       |
+-----------------------------------+---------------------------------------+

Reliable
--------
We understand that you are looking for an easy yet reliable way to manage your users.
We've run our code automated tests from the very beginning and we're proud
to consistently achieve automated code coverage of over 95% without fudging.

Here is our Feb 2014 code coverage report::

    > coverage report
    Name                                                            Stmts   Miss  Cover
    -----------------------------------------------------------------------------------
    flask_user/__init__                                                93      0   100%
    flask_user/db_interfaces                                           51      0   100%
    flask_user/emails                                                  28      0   100%
    flask_user/forms                                                  149      3    98%
    flask_user/passwords                                                4      0   100%
    flask_user/tokens                                                  37      0   100%
    flask_user/views                                                  128     13    90%
    -----------------------------------------------------------------------------------
    TOTAL                                                             490     16    97%


Fully Customizable
------------------

| - **URLs** and
| - **workflow** can be configured through your application config.

| - **Form templates** and
| - **Email messages** can be customized by creating copies in your application's ``templates`` directory.

| - **Form field labels**,
| - **Validation messages**, and
| - **Flash messages** can be customized and through Babel translation files.

| - **Forms**,
| - **View functions**,
| - the **Password validator**, and
| - the **Username validator** can be customized by setting a Flask-User attribute.

| - Many **Password hasing methods** available through passlib and py-bcrypt.


Easy to Install
---------------
::

    pip install flask-user

Easy to Setup
-------------
Here's the minimal code needed to get an existing Flash application up and running with Flask-User::

        ...
    from flask.ext.user import SQLAlchemyAdapter, UserManager
        ...
    def create_app():
        app = Flask(__name__)                                   # Initialize Flask App
        db.init_app(app)                                        # Bind Flask-SQLAlchemy to app
        db_adapter = flask_user.SQLAlchemyAdapter(db, User)     # Choose a database Adapter
        user_manager = flask_user.UserManager(db_adapter)       # Initialize Flask-User
        user_manager.init_app(app)                              # Bind Flask-User to app
        return app


Planned Features
----------------
* Registration by invitation only
* Profile editing with pictures and thumbnails
* Role based authorization
