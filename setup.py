"""
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
* **Well documentated**

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

Revision History
----------------
* v0.3.4 Added support for Python 3.3 (while retaining support for 2.7 and 2.6)
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
    version='0.3.4',
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
