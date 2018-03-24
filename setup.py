from setuptools import setup
import sys

__version__ = '0.6.20'

# Load pytest and pytest-runner only when needed:
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


# Read long description from README.rst file
def load_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='Flask-User',
    version=__version__,
    url='http://github.com/lingthio/Flask-User',
    license='BSD License',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    description='Customizable User Authentication and Management, and more.',
    long_description=load_readme(),
    keywords='Flask User Registration Email Username Confirmation Password Reset',

    platforms='any',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=['flask_user'],
    include_package_data=True,    # Tells setup to use MANIFEST.in
    zip_safe=False,    # Do not zip as it will make debugging harder

    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',   # Python 2.6, 2.7, 3.3+
    setup_requires=pytest_runner,
    install_requires=[
        'bcrypt',
        'Flask',
        'Flask-Login',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'passlib',
        'pycryptodome',
    ],
    tests_require=['pytest'],
)

