"""
===========
Flask-Utils
===========

Customizable User management for Flask

Features
--------
* Register (sign up)
* Confirm email
* Login (Sign in) with email or username
* Logout (Sign out)
* Change username
* Change password
* Forgot password (Reset password)
* Session management through Flask-Login
* Password encryption through passlib and py-bcript
* Internationalization through Flask-Babel

Philosophy
----------
* Reliable (Automated test coverage of over 95%)
* Simple to use
* Easy to configure (by changing files)
* Easy to customize (by adding code)
* Model agnostic (specify your own User model)
* Database abstraction (SQLAlchemyAdapter provided)
* Extensible (See Flask-User-Roles for role based authorization)
"""

from __future__ import print_function
from setuptools import setup

# class run_audit(Command):
#     """Audits source code using PyFlakes for following issues:
#         - Names which are used but not defined or used before they are defined.
#         - Names which are redefined without having been used.
#     """
#     description = "Audit source code with PyFlakes"
#     user_options = []
#
#     def initialize_options(self):
#         pass
#
#     def finalize_options(self):
#         pass
#
#     def run(self):
#         import os, sys
#         try:
#             import pyflakes.scripts.pyflakes as flakes
#         except ImportError:
#             print("Audit requires PyFlakes installed in your system.")
#             sys.exit(-1)
#
#         warns = 0
#         # Define top-level directories
#         dirs = ('flask', 'examples', 'scripts')
#         for dir in dirs:
#             for root, _, files in os.walk(dir):
#                 for file in files:
#                     if file != '__init__.py' and file.endswith('.py') :
#                         warns += flakes.checkPath(os.path.join(root, file))
#         if warns > 0:
#             print("Audit finished with total %d warnings." % warns)
#         else:
#             print("No problems found in sourcecode.")
#
setup(
    name='Flask-User',
    version='0.3',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    url='http://github.com/lingthio/flask-user#flask-user',
    license='Simplified BSD License',
    description='A user management extension for Flask (Register, Confirm, Forgot password, Login, etc.)',
    long_description=__doc__,
    packages=['flask_user'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'SQLAlchemy',
        'WTForms',
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
