"""
==========
Flask-User
==========

!!News Flash: In v0.3.1 and v0.3.2 confirmation emails were not working.
Please upgrade to v0.3.3. Thank you!!

Overview
--------

| Many Flask websites require that their users can Register, Confirm email,
| Login, Logout, Change password and Reset forgotten passwords.
| Each website often requires different and precise customization of this process.

Flask-User aims to provide a ready to use **and** fully customizable package that is:

* **Reliable** user management functionality,
* **Secure** password hashing and token encryption and signing,
* **Ready to use** after an easy install and setup,
* **Fully customizable** through well documented config settings and attributes, and
* **Good documentation**.

Status
------

This package is relatively new. We are looking for alpha testers to give us feedback
on how it behaves in different usage scenarios. If something doesn't work the way
you expect it to work, please take the time to email ling [at] gmail.com and help us
reach outstanding quality quickly. Thanks!

We're also welcoming feature requests. In particular, we would like to know if there's
a need out there for database adapters other than the SQLAlchemyAdapter.

Documentation
-------------
* `View documentation here <https://pythonhosted.org/Flask-User/>`_

Revision History
----------------
* v0.3.3 Added minimal-app and basic-app examples
* v0.3.2 Bug fix for Confirm email
* v0.3.1 Alpha release
* v0.3 Confirm email, Forgot password, Reset password
* v0.2 Change username, Change password
* v0.1 Register, Login, Logout

Contact
-------
Ling Thio - ling.thio [at] gmail.com
"""

from __future__ import print_function
from setuptools import setup

setup(
    name='Flask-User',
    version='0.3.3',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    url='http://github.com/lingthio/flask-user',
    description='Customizable User Login for Flask: Register, Confirm, Forgot password and more',
    keywords='Flask User Registration Email Confirmation Reset',
    long_description=__doc__,
    packages=['flask_user'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'passlib',
        'py-bcrypt',
        'pycrypto',
        'Flask',                # Includes itsdangerous
        'Flask-Babel',
        'Flask-Login',
        'Flask-Mail',           # Includes blinker
        'Flask-SQLAlchemy',     # Includes SQLAlchemy
        'Flask-WTF',            # Includes WTForms
    ],
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
    #cmdclass={'audit': run_audit},
    #test_suite='flask.testsuite.suite'
)
