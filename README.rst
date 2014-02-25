Flask-User
==========

.. image:: https://pypip.in/v/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://travis-ci.org/lingthio/flask-user.png?branch=master
    :target: https://travis-ci.org/lingthio/flask-user

.. image:: https://coveralls.io/repos/lingthio/flask-user/badge.png?branch=master
    :target: https://coveralls.io/r/lingthio/flask-user?branch=master

.. image:: https://pypip.in/d/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://pypip.in/license/Flask-User/badge.png
    :target: https://pypi.python.org/pypi/Flask-User

::

    !! Newsflash: In v0.3.1 and v0.3.2 confirmation emails were not working !!
       Please upgrade to v0.3.4. Thank you.

User Login for Flask
--------------------
**Register, Confirm email, Login, Forgot password and more**

| Many Flask websites require that their users can Register, Confirm email, Login, Logout, Change password and Reset forgotten passwords.
| Each website often requires different and precise customization of this process.

Flask-User aims to provide a ready to use **and** fully customizable package that is:

* **Reliable** (Automated tests cover 97% of the code base)
* **Secure** (``bcrypt`` password hashing, ``AES`` ID encryption, ``itsdangerous`` token signing)
* **Ready to use**
* **Fully customizable** (Email, Field labels, Flash messages, Form templates, URLs, and more)
* **Well documented**

Documentation
-------------

`Flask-User Documentation <https://pythonhosted.org/Flask-User/>`_

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Roles: Role based authentication
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Alternative Packages
--------------------
I've successfully used `Flask-Security <https://pythonhosted.org/Flask-Security/>`_ in the past.
Flask-Security offers additional role based authentication.

Contact
-------
Ling Thio - ling.thio [at] gmail.com