from setuptools import setup

# Import version number from source code
from flask_user import __version__ as flask_user_version


# Read long description from README.rst file
def load_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='Flask-User',
    version=flask_user_version,
    description='Customizable User Authorization and Management: Register, Confirm email, Login, Change username, Change password, Forgot password and more.',
    long_description=load_readme(),
    keywords='Flask User Authorization Account Management Registration Username Email Confirmation Forgot Reset Password Invitation',
    url='http://github.com/lingthio/Flask-User',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    license='BSD License',

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
    install_requires=[
        'Flask>=0.9',
        'Flask-Login>=0.3',
        'Flask-Mail>=0.9',
        'Flask-SQLAlchemy>=1.0',
        'Flask-WTF>=0.9',
        'bcrypt>=1.1',
        'cryptography>=2.0',
        'passlib>=1.6',
    ],
)
