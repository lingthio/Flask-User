import sys
from setuptools import setup

__title__       = 'Flask-User'
__description__ = 'Customizable User Authentication,User Management, and more.'
__version__     = '1.0.1.1'
__url__         = 'https://github.com/lingthio/Flask-User'
__author__      = 'Ling Thio'
__author_email__= 'ling.thio@gmail.com'
__maintainer__  = 'Ling Thio'
__license__     = 'MIT'
__copyright__   = '(c) 2013 Ling Thio'


# Load pytest and pytest-runner only when needed:
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


# Read long description from README.rst file
def load_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=load_readme(),
    keywords='Flask User Authorization Account Management Registration Username Email Confirmation Forgot Reset Password Invitation',
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,

    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: German',
        'Natural Language :: Spanish',
        'Natural Language :: Finnish',
        'Natural Language :: French',
        'Natural Language :: Italian',
        'Natural Language :: Persian',
        'Natural Language :: Russian',
        'Natural Language :: Swedish',
        'Natural Language :: Turkish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=['flask_user'],
    include_package_data=True,    # Tells setup to use MANIFEST.in
    zip_safe=False,    # Do not zip as it will make debugging harder

    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',   # Python 2.6, 2.7, 3.3+
    setup_requires=['Flask-Login',] + pytest_runner,
    install_requires=[
        'bcrypt>=2.0',
        'cryptography>=1.6',
        'Flask>=0.9',
        'Flask-Login>=0.2',
        'Flask-Mail>=0.9',
        'Flask-SQLAlchemy>=1.0',
        'Flask-WTF>=0.9',
        'passlib>=1.6',
    ],
    tests_require=['pytest'],
)
