===============
Install & Setup
===============

Requirements
------------
- Python 2.6 or 2.7
- Flask
- Flask-Babel
- Flask-Login
- Flask-WTF
- crypto, passlib and py-bcript

Additional requirements when selecting the SQLAlchemyAdapter():

- SQL-Python
- Flask-SQLAlchemy

Installation Instructions
-------------------------

We recommend making use of virtualenv and virtualenvwrapper
::

    mkvirtualenv my_env
    workon my_env
    pip install flask-user

Using Flask-User with a new application
---------------------------------------
Checkout the example_app dir of the `Flask-User github repository <https://github.com/solidbuilds/flask-user/tree/master/example_app>`_

Setting up Flask-User with an existing application
--------------------------------------------------
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


