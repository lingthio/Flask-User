"""

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

Customizable User Account Management for Flask
----------------------------------------------

Many web applications require User Account Management features such as **Register**, **Confirm email**,
**Login**, **Change username**, **Change password** and **Forgot password**.

Some also require **Role-based Authorization** and **Internationalization**.

Wouldn't it be nice to have a package that would offer these features **out-of-the-box**
while retaining **full control over the workflow and presentation** of this process?

Flask-User aims to provide such a ready-to-use **AND** fully customizable solution:

* **Reliable**
* **Secure**
* **Fully customizable**
* **Ready to use**
* **Role-based Authorization**
* **Internationalization**
* **Well documented**
* Tested on Python 2.6, 2.7 and 3.3

Documentation
-------------

`Flask-User Documentation <https://pythonhosted.org/Flask-User/>`_

Revision History
----------------
`Flask-User Revision History <http://pythonhosted.org//Flask-User/index.html#revision-history>`_

Extension Packages
------------------
We plan to offer the following Flask-User extensions in the future:

* Flask-User-Profiles: View profile, Edit profile, Upload profile picture
* Flask-User-Social: Login via Google, Facebook and Twitter authentication

Alternative Packages
--------------------
`Flask-Security <https://pythonhosted.org/Flask-Security/>`_

Contact
-------
Ling Thio - ling.thio [at] gmail.com
"""

from __future__ import print_function
from setuptools import setup

setup(
    name='Flask-User',
    version='0.4.1',
    url='http://github.com/lingthio/flask-user',
    license='BSD License',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    description='Customizable User Account Management for Flask: Register, Confirm email, Login, Change username, Change password, Forgot password and more.',
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
        'Development Status :: 4 - Beta',
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
