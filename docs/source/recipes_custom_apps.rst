===========
Custom Apps
===========

Github contains the following additional example apps:

**Custom Register Form with User model**

This application:

* Defines a User model with extra 'first_name' and 'last_name' fields
* Defines a MyRegisterForm with extra fields
* Defines a templates/flask_user/register.html template with extra fields

Flask-User will automatically save any Register form field with a matching User model field in the User record.

`See Github repository <https://github.com/lingthio/Flask-User/tree/master/example_apps/custom_register_app>`_

**Custom Register Form with User and UserProfile model**

This application behaves similarly to the example app above,
except that it stores 'first_name' and 'last_name' in a separate UserProfile object.

Note that the User model has 'user_profile_id' and 'user_profile'.

Note that SQLAlchemy() is called with both the User class and the UserProfile class.

Flask-User will automatically save any Register form field with a matching UserProfile model field in the UserProfile record.

`See Github repository <https://github.com/lingthio/Flask-User/tree/master/example_apps/user_profile_app>`_
