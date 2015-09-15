"""
Flask-User
==========

.. image:: https://img.shields.io/pypi/v/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://img.shields.io/travis/lingthio/Flask-User.svg
    :target: https://travis-ci.org/lingthio/Flask-User

.. image:: https://img.shields.io/pypi/dm/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User

.. image:: https://img.shields.io/pypi/l/Flask-User.svg
    :target: https://pypi.python.org/pypi/Flask-User

Customizable User Account Management for Flask
----------------------------------------------

| So you're writing a Flask web application and would like to authenticate your users.
| You start with a simple **Login** page, but soon enough you need to handle:

* **Registrations** and **Email Confirmations**
* **Change Usernames**, **Change Passwords**, and **Forgotten Passwords**

And wouldn't it be nice to also offer:

* **Role-based Authorization**
* **Remember-me cookies**
* **Multiple emails per user**
* **Internationalization**

| Flask-User offers these user features (and more) out-of-the-box
| while also honoring the following developer needs:

* **Reliable** (Code coverage of over 95%)
* **Secure** (Built on top of widely deployed Flask-Login)
* **Ready to use** (Through sensible defaults)
* **Largely configurable** (Through configuration settings)
* **Fully customizable** (Through customizable functions and email templates)
* **Well documented**
* **Tested on Python 2.6, 2.7, 3.3 and 3.4**

Status
------

| Flask-User v0.5 and v0.6 are quite stable and are used in production environments.
| It is marked as a Beta release because the API is subject to small changes.
| We appreciate it if you would enter issues and
  enhancement requests into the `Flask-User Issue Tracker <https://github.com/lingthio/flask-user/issues>`_.


Demo
----
The `Flask-User Demo <https://flask-user-demo.herokuapp.com/>`_ showcases Flask-User.
To protect against spam mis-use, all email features have been disabled.
(If you're the first visitor in the last hour, it may take a few seconds for Heroku to start this service)

Documentation
-------------
`Flask-User Documentation <https://pythonhosted.org/Flask-User/>`_

Revision History
----------------
`Flask-User Revision History <http://pythonhosted.org//Flask-User/index.html#revision-history>`_

Contact Information
-------------------
Ling Thio - ling.thio [at] gmail.com

Acknowledgements
----------------
This project would not be possible without the use of the following amazing offerings:

* `Flask <http://flask.pocoo.org/>`_
* `Flask-Babel <http://babel.pocoo.org/>`_
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Mail <http://pythonhosted.org/flask-mail/>`_
* `SQLAlchemy <http://www.sqlalchemy.org/>`_ and `Flask-SQLAlchemy <http://pythonhosted.org/Flask-SQLAlchemy/>`_
* `WTForms <http://wtforms.readthedocs.org/en/latest/>`_ and `Flask-WTF <https://flask-wtf.readthedocs.org/en/latest/>`_

Alternative Flask extensions
----------------------------
* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
* `Flask-Security <https://pythonhosted.org/Flask-Security/>`_
"""

from __future__ import print_function
from setuptools import setup

setup(
    name='Flask-User',
    version='0.6.8',
    url='http://github.com/lingthio/Flask-User',
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
        'bcrypt',
        'pycrypto',
        'Flask',
        'Flask-Login',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
    ],
    test_suite="flask_user.tests.run_tests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
