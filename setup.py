"""

Customizable User Login for Flask
---------------------------------
**Register, Confirm email, Login, Forgot password and more**

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

| Many websites require that their users can **Register**, **Confirm email**, **Login**, **Change password** and handle **Forgot passwords**.
| Some websites require **Role-based Authorization**.
| *Each website often requires different and precise customization of this process*.

Flask-User aims to provide a ready to use **and** fully customizable package that is:

* **Reliable** (Automated tests cover over 95% of the code base)
* **Secure** (``bcrypt`` for passwords, ``AES`` and ``itsdangerous`` for tokens)
* **Ready to use**
* **Fully customizable** (Emails, Templates, Validators, Views and more)
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Documentation
-------------

`Flask-User Documentation <https://pythonhosted.org/Flask-User/>`_

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Alternative Packages
--------------------
I've successfully used `Flask-Security <https://pythonhosted.org/Flask-Security/>`_ in the past.

Revision History
----------------
* v0.3.7 Added role based authorization with @roles_required.
* v0.3.6 Provides @login_required. Handles multiple apps.
* v0.3.5 Added: Signals. Refactored automated tests.
* v0.3.4 Added: Support for Python 3.3 (while retaining support for 2.7 and 2.6)
* v0.3.3 Added: Minimal-app and basic-app examples to docs
* v0.3.2 Bug fix: Confirm email did not send confirmation emails
* v0.3.1 Alpha release
* v0.3 Added: Confirm email, Forgot password, Reset password
* v0.2 Added: Change username, Change password
* v0.1 Initial version: Register, Login, Logout

Contact
-------
Ling Thio - ling.thio [at] gmail.com
"""

from __future__ import print_function
from setuptools import setup

setup(
    name='Flask-User',
    version='0.3.7',
    url='http://github.com/lingthio/flask-user',
    license='BSD License',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    description='Customizable User Login for Flask: Register, Confirm email, Login, Forgot password and more',
    long_description=__doc__,
    keywords='Flask User Registration Email Username Confirmation Password Reset',
    packages=['flask_user'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'passlib',
        'py-bcrypt',
        'pycrypto',
        'Flask',
        'Flask-Babel',
        'Flask-Login',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
    ],
    test_suite="flask_user.tests.run_tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
