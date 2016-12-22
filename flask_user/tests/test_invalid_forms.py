"""
    tests.test_invalid_forms.py
    ---------------------------
    Flask-User automated tests:
    Tests all forms with as many invalid field values as possible

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from __future__ import print_function

from datetime import datetime
import time

from flask import current_app, url_for

from flask_user.tests.tst_utils import response_has_string



# **********************
# ** Global Variables **
# **********************
# Using global variable for speed
user1 = None
user2 = None
user3 = None
user4 = None

# *************
# ** Defines **
# *************
SHORT_USERNAME = 'Aa'
INVALID_EMAIL = 'user1.example.com'
invalid_usernames = (
    'with space',
    'with&symbol',
    "with'symbol",
    )
invalid_passwords = (
    'Abcd1',        # too short
    'ABCabc',       # no digits
    'ABC123',       # no lower case letters
    'abc123',       # no upper case letters
    )


# *********************
# ** Automated tests **
# *********************
# Function names must start with 'test'
# The 'client' parameter is set up in conftest.py

def test_init(db):
    """
    Set up two test users
    """
    global user1, user2, user3, user4

    # Enable all features
    um =  current_app.user_manager
    um.enable_register = True
    um.enable_change_username = True
    um.enable_change_password = True
    um.enable_confirm_email = True
    um.enable_reset_password = True
    um.enable_email = True
    um.enable_retype_password = True

    # Tests have not been written with auto_login in mind
    um.auto_login = False

    hashed_password = um.hash_password('Password1')
    User = um.db_adapter.UserClass

    # Create user1 with username and email
    user1 = User(username='user1', email='user1@example.com', password=hashed_password, active=True)
    assert user1
    db.session.add(user1)

    # Create user1 with email only
    user2 = User(email='user2@example.com', password=hashed_password, active=True)
    assert user2
    db.session.add(user2)

    # Create user3 with username and email
    user3 = User(username='user3', email='user3@example.com', password=hashed_password, active=True)
    assert user3
    db.session.add(user3)

    # Create user4 with email only
    user4 = User(email='user4@example.com', password=hashed_password, active=True)
    assert user4
    db.session.add(user4)

    db.session.commit()


def test_invalid_register_with_username_form(client):
    print("test_invalid_register_with_username_form")

    # Choose config
    um =  current_app.user_manager
    um.enable_username = True
    User = um.db_adapter.UserClass

    # Set default values
    url = url_for('user.register')
    username = 'user3'
    email = 'user3@example.com'
    password = 'Password1'

    # Test empty username
    client.post_invalid_form(url, 'Username is required',
            username='', email=email, password=password, retype_password=password)

    # Test short username
    client.post_invalid_form(url, 'Username must be at least 3 characters long',
            username=SHORT_USERNAME, email=email, password=password, retype_password=password)

    # Test invalid usernames
    for invalid_username in invalid_usernames:
        client.post_invalid_form(url, 'Username may only contain letters, numbers, ',
                username=invalid_username, email=email, password=password, retype_password=password)

    # Test existing username (case INsensitive!)
    client.post_invalid_form(url, 'This Username is already in use. Please try another one.',
            username='UsEr1', email=email, password=password, retype_password=password)

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            username=username, email=email, password='', retype_password='')

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        client.post_invalid_form(url, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number',
                username=username, email=email, password=invalid_password, retype_password=invalid_password)

    # Test non-matching passwords
    client.post_invalid_form(url, 'Password and Retype Password did not match',
            username=username, email=email, password='Password1', retype_password='Password9')

def test_invalid_register_with_email_form(client):
    print("test_invalid_register_with_email_form")

    # Choose config
    um =  current_app.user_manager
    um.enable_username = False
    User = um.db_adapter.UserClass

    # Set default values
    url = url_for('user.register')
    email = 'user3@example.com'
    password = 'Password1'

    # Test empty email
    client.post_invalid_form(url, 'Email is required',
            email='', password=password, retype_password=password)

    # Test invalid email
    client.post_invalid_form(url, 'Invalid Email',
            email=INVALID_EMAIL, password=password, retype_password=password)

    # Test existing email (case INsensitive!)
    # TODO: Debug
    #client.post_invalid_form(url, 'This Email is already in use. Please try another one.',
    #        email='UsEr1@ExAmPlE.CoM', password=password, retype_password=password)

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            email=email, password='', retype_password='')

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        client.post_invalid_form(url, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number',
                email=email, password=invalid_password, retype_password=invalid_password)

    # Test non-matching passwords
    client.post_invalid_form(url, 'Password and Retype Password did not match',
            email=email, password='Password1', retype_password='Password9')

def test_invalid_confirm_email_page(client):
    print("test_invalid_confirm_email_page")

    # Test Invalid token
    url = url_for('user.confirm_email', token='InvalidToken')
    client.get_invalid_page(url, 'Invalid confirmation token')

    # Generate valid token
    um = current_app.user_manager
    token = um.generate_token(user1.id)
    url = url_for('user.confirm_email', token=token)

    # Test Expired token
    um.confirm_email_expiration = 1   # set 1 second expiration
    time.sleep(2)                     # wait for 2 seconds
    client.get_invalid_page(url, 'Your confirmation token has expired')


def test_invalid_login_with_username_form(client):
    print("test_invalid_login_with_username_form")

    # Choose config
    um = current_app.user_manager
    um.enable_email = True
    um.enable_username = True

    # Set default values
    url = url_for('user.login')
    username = 'user1'
    password = 'Password1'

    # Test empty username
    client.post_invalid_form(url, 'Username is required',
            username='', password=password)

    # Test incorrect username
    um.show_username_email_does_not_exist = False
    client.post_invalid_form(url, 'Incorrect Username/Email and/or Password',
            username='Xuser1', password=password)
    um.show_username_email_does_not_exist = True
    client.post_invalid_form(url, 'Username/Email does not exist',
            username='Xuser1', password=password)
    um.show_username_email_does_not_exist = False

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            username=username, password='')

    # Test incorrect password
    um.show_username_email_does_not_exist = False
    client.post_invalid_form(url, 'Incorrect Username/Email and/or Password',
            username=username, password='XPassword1')
    um.show_username_email_does_not_exist = True
    client.post_invalid_form(url, 'Incorrect Password',
            username=username, password='XPassword1')
    um.show_username_email_does_not_exist = False

def test_invalid_login_with_email_form(client):
    print("test_invalid_login_with_email_form")

    # Choose config
    um = current_app.user_manager
    um.enable_email = True
    um.enable_username = False

    # Set default values
    url = url_for('user.login')
    email = 'user2@example.com'
    password = 'Password1'

    # Test empty email
    client.post_invalid_form(url, 'Email is required',
            email='', password=password)

    # Test incorrect email
    um.show_username_email_does_not_exist = False
    client.post_invalid_form(url, 'Incorrect Email and/or Password',
            email='Xuser2@example.com', password=password)
    um.show_username_email_does_not_exist = True
    client.post_invalid_form(url, 'Email does not exist',
            email='Xuser2@example.com', password=password)
    um.show_username_email_does_not_exist = False

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            email=email, password='')

    # Test incorrect password
    um.show_username_email_does_not_exist = False
    client.post_invalid_form(url, 'Incorrect Email and/or Password',
            email=email, password='XPassword1')
    um.show_username_email_does_not_exist = True
    client.post_invalid_form(url, 'Incorrect Password',
            email=email, password='XPassword1')
    um.show_username_email_does_not_exist = False

def test_invalid_change_username_form(client):
    print("test_invalid_change_username_form")

    # Set user manager config
    um =  current_app.user_manager
    um.enable_username = True
    um.enable_email = False

    # Set default values
    username = 'user1'
    password = 'Password1'
    new_username = 'user4'
    url = url_for('user.change_username')

    # Log in as 'user1'
    client.login(username=username, password=password)

    # Test empty username
    client.post_invalid_form(url, 'Username is required',
            new_username='', old_password=password)

    # Test short username
    client.post_invalid_form(url, 'Username must be at least 3 characters long',
            new_username=SHORT_USERNAME, old_password=password)

    # Test existing username
    client.post_invalid_form(url, 'This Username is already in use. Please try another one.',
            new_username='user3', old_password=password)

    # Test empty password
    client.post_invalid_form(url, 'Old Password is required',
            new_username=username, old_password='')

    # Test incorrect password
    client.post_invalid_form(url, 'Old Password is incorrect',
            new_username=username, old_password='XPassword1')

    client.logout()

def test_invalid_change_password_form(client):
    print("test_invalid_change_password_form")

    # Set user manager config
    um =  current_app.user_manager
    um.enable_username = False

    # Set default values
    email = 'user2@example.com'
    old_password = 'Password1'
    new_password = 'Password5'
    url = url_for('user.change_password')

    # Log in as 'user1'
    client.login(email=email, password=old_password)

    # Test empty old password
    client.post_invalid_form(url, 'Old Password is required',
            old_password='', new_password=new_password, retype_password=new_password)

    # Test incorrect old password
    client.post_invalid_form(url, 'Old Password is incorrect',
            old_password='XPassword1', new_password=new_password, retype_password=new_password)

    # Test empty password
    client.post_invalid_form(url, 'New Password is required',
            old_password=old_password, new_password='', retype_password=new_password)

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        client.post_invalid_form(url, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number',
            old_password=old_password, new_password=invalid_password, retype_password=new_password)

    # Test non-matching passwords
    client.post_invalid_form(url, 'New Password and Retype Password did not match',
            old_password=old_password, new_password=new_password, retype_password='Xpassword5')

    client.logout()


def test_invalid_forgot_password_form(client):
    print("test_invalid_forgot_password_form")

    url = url_for('user.forgot_password')

    # Test invalid email
    client.post_invalid_form(url, 'Invalid Email',
            email=INVALID_EMAIL)


def test_invalid_reset_password(client):
    print("test_invalid_reset_password")

    # Set user manager config
    um =  current_app.user_manager

    # Set default values
    new_password = 'Password5'
    # Simulate a valid forgot password form
    token = um.generate_token(user1.id)

    # Test invalid token
    url = url_for('user.reset_password', token='InvalidToken')
    client.post_invalid_form(url, 'Your reset password token is invalid',
            new_password=new_password, retype_password=new_password)

    # Expired Token
    url = url_for('user.reset_password', token=token)
    um.reset_password_expiration = 1    # set 1 second expiration
    time.sleep(2)                       # wait for 2 seconds
    client.post_invalid_form(url, 'Your reset password token has expired',
            new_password=new_password, retype_password=new_password)
    um.reset_password_expiration = 2*24*3600  # 2 days

    # Invalid retype password
    client.post_invalid_form(url, 'New Password and Retype Password did not match',
            new_password = new_password, retype_password='XPassword5')

def test_valid_roles(client):
    um =  current_app.user_manager
    User = um.db_adapter.UserClass

    # Perform only for roles_required_app
    user007 = User.query.filter(User.username=='user007').first()
    if not user007: return

    print("test_valid_roles")
    um.enable_username = True

    client.login(username='user007', password='Password1')
    url = url_for('special_page')
    response = client.get_valid_page(url)
    assert not response_has_string(response, 'You must be signed in to access')
    client.logout()

def test_invalid_roles(client):
    um =  current_app.user_manager
    User = um.db_adapter.UserClass

    # Perform only for roles_required_app
    user007 = User.query.filter(User.username=='user007').first()
    if not user007: return

    print("test_invalid_roles")
    um.enable_username = True

    client.login(username='user1', password='Password1')
    url = url_for('special_page')
    response = client.get_invalid_page(url, 'You do not have permission to access')
    client.logout()

def test_login_without_confirm_email(client):
    print("test_login_without_confirm_email")

    um = current_app.user_manager
    um.enable_username = False
    um.enable_email = True
    um.enable_confirm_email = True
    um.enable_retype_password = False

    email = 'notconfirmed@example.com'
    password = 'Password1'

    # register user
    client.post_valid_form(url_for('user.register'),
            email=email,
            password=password)

    # Try logging in without confirming email
    client.post_invalid_form(url_for('user.login'),
            'Your email address has not yet been confirmed',
            email=email,
            password=password)

    # Confirm email manually, but disable account
    User = um.db_adapter.UserClass
    user = User.query.filter(User.email==email).first()
    assert(user)
    user.active = False
    user.confirmed_at = datetime.utcnow()

    # Try logging in into  disabled account
    client.post_invalid_form(url_for('user.login'),
            'Your account has not been enabled',
            email=email,
            password=password)

def test_cleanup(db):
    """
    Delete user1 and user2
    """
    global user1, user2, user3, user4
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.delete(user3)
    db.session.delete(user4)
    db.session.commit()
    user1 = None
    user2 = None
    user3 = None
    user4 = None


# TODO:
# Register without confirming email and try to log in
# 'Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email and follow the instructions to activate your account.'
#
# Disable account and try to login
# 'Your account has been disabled.'
#
# Logout with user_manager.logout_next set
#
# Reset password with custom user_manager.password_validator
#
# Change password with custom user_manager.password_validator:
#
# Custom db_adapter.EmailClass