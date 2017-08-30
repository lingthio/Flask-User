from setuptools import setup

def load_readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='Flask-User',
    version='1.0.0',
    description='Customizable User Authorization and Management: Register, Confirm email, Login, Change username, Change password, Forgot password and more.',
    long_description=load_readme(),
    url='http://github.com/lingthio/Flask-User',
    author='Ling Thio',
    author_email='ling.thio@gmail.com',
    license='BSD License',
    keywords='Flask User Authorization Account Management Registration Username Email Confirmation Forgot Reset Password',

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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=['flask_user'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask>=0.9',
        'Flask-Login>=0.3',
        'Flask-WTF>=0.9',
        'bcrypt>=1.1',
        'cryptography>=2.0',
        'passlib>=1.6',
    ],
    test_suite="flask_user.tests.run_tests",
)
