import time

from flask import current_app, url_for
from example_app.models import User
from tests import utils as test_utils

# *************
# ** Defines **
# *************
USERNAME1 = 'user1'
EMAIL1 = 'user1@example.com'
PASSWORD1 = 'Password1'
SHORT_USERNAME = 'Aa'
INVALID_EMAIL = 'user1.example.com'
invalid_usernames = (
    'with space',
    'with_symbol',
    'with&symbol',
    "with'symbol",
    )
invalid_passwords = (
    'Abcd1',        # too short
    'ABCabc',       # no digits
    'ABC123',       # no lower case letters
    'abc123',       # no upper case letters
    )

# ***********************
# ** Utility functions **
# ***********************

def post_register_form(client, username=None, email=None, password=PASSWORD1, retype_password=None):
    """
    POST a Register form
    """
    url = url_for('user.register')
    if not retype_password:
        retype_password = password
    return client.post(url, follow_redirects=True, data=dict(
        username=username,
        email=email,
        password=password,
        retype_password=retype_password,
    ))

def post_login_form(client, username=None, email=None, password=PASSWORD1):
    """
    POST a Login form
    """
    url = url_for('user.login')
    return client.post(url, data=dict(
        username=username,
        email=email,
        password=password
    ), follow_redirects=True)

def post_change_username_form(client, new_username=None, old_password=PASSWORD1):
    """
    POST a Change User form
    """
    url = url_for('user.change_username')
    return client.post(url, data=dict(
        new_username=new_username,
        old_password=old_password
    ), follow_redirects=True)

def post_change_password_form(client, old_password=PASSWORD1, new_password=PASSWORD1, retype_password=None):
    """
    POST a Change Password form
    """
    url = url_for('user.change_password')
    if not retype_password:
        retype_password = new_password
    return client.post(url, data=dict(
        old_password=old_password,
        new_password=new_password,
        retype_password=retype_password,
    ), follow_redirects=True)

# *********************
# ** Automated tests **
# *********************
# Function names must start with 'test'
# The 'client' parameter is set up in conftest.py

# Workaround for py.test coverage issue
def run_all_tests(client):
    test_register_form_with_username(client)
    test_register_form_with_email(client)
    test_login_form_with_username(client)
    test_login_form_with_email(client)
    test_change_username_form(client)
    test_change_password_form(client)

def test_register_form_with_username(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.require_email_confirmation=False
    user_manager.login_with_username = True
    user_manager.register_with_email = False

    # ****************
    # ** Valid Form **
    # ****************

    # Submit valid form with retype password
    user_manager.retype_password = True
    username = USERNAME1
    email = EMAIL1
    response = post_register_form(client, username, email)
    assert response.status_code == 200
    assert test_utils.response_has_no_errors(response)

    # Verify that the user account has been created
    user = User.query.filter(User.username==username).first()
    assert user
    assert user.username == username
    assert user.active

    # Submit valid form without retype password
    user_manager.retype_password = True
    username = 'user2'
    response = post_register_form(client, username, email)
    assert response.status_code == 200
    assert test_utils.response_has_no_errors(response)

    # Verify that the user account has been created
    user = User.query.filter(User.username==username).first()
    assert user
    assert user.username == username
    assert user.active

    # *******************
    # ** Invalid Forms **
    # *******************
    # Assumes that 'user1' and 'user2' exist

    user_manager.retype_password = True
    username = 'user3'
    email = None

    # Test empty username
    response = post_register_form(client, '', email)
    assert test_utils.response_has_string(response, 'Username is required')

    # Test short username
    response = post_register_form(client, SHORT_USERNAME, email)
    assert test_utils.response_has_string(response, 'Username must be at least 3 characters long')

    # Test invalid usernames
    for invalid_username in invalid_usernames:
        response = post_register_form(client, invalid_username, email)
        assert test_utils.response_has_string(response, 'Username may only contain letters and numbers')

    # Test existing username (case INsensitive!)
    response = post_register_form(client, 'UsEr2', email)
    assert test_utils.response_has_string(response, 'This Username is no longer available. Please try another one.')

    # Test empty password
    response = post_register_form(client, username, email, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        response = post_register_form(client, username, email, invalid_password)
        assert test_utils.response_has_string(response, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number')

    # Test non-matching passwords
    response = post_register_form(client, username, email, 'Password1', 'Password9')
    assert test_utils.response_has_string(response, 'Password and Retype Password did not match')


def test_register_form_with_email(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.require_email_confirmation=False
    user_manager.login_with_username = False
    user_manager.register_with_email = True

    # ****************
    # ** Valid Form **
    # ****************

    # Submit valid form with retype password
    user_manager.retype_password = True
    email = EMAIL1
    response = post_register_form(client, '', email)
    assert response.status_code == 200
    assert test_utils.response_has_no_errors(response)

    # Verify that the user account has been created
    user = User.query.filter(User.email==email).first()
    assert user
    assert user.email == email
    assert user.active

    # Submit valid form without retype password
    user_manager.retype_password = False
    email = 'user2@example.com'
    response = post_register_form(client, '', email)
    assert response.status_code == 200
    assert test_utils.response_has_no_errors(response)

    # Verify that the user account has been created
    user = User.query.filter(User.email==email).first()
    assert user
    assert user.email == email
    assert user.active

    # *******************
    # ** Invalid Forms **
    # *******************
    # Assumes 'user1@xample.com' and 'user2@example.com' exists

    user_manager.retype_password = True
    username = None
    email = 'user3@example.com'

    # Test empty email
    response = post_register_form(client, username, '')
    assert test_utils.response_has_string(response, 'Email is required')

    # Test short email
    response = post_register_form(client, username, INVALID_EMAIL)
    assert test_utils.response_has_string(response, 'Invalid Email')

    # Test existing email (case INsensitive!)
    response = post_register_form(client, username, 'UsEr2@ExAmPlE.cOm')
    assert test_utils.response_has_string(response, 'This Email is no longer available. Please try another one.')

    # Test empty password
    response = post_register_form(client, username, email, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test invalid password
    for invalid_password in invalid_passwords:
        response = post_register_form(client, username, email, invalid_password)
        assert test_utils.response_has_string(response, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number')

    # Test non-matching passwords
    response = post_register_form(client, username, email, 'Password1', 'Password9')
    assert test_utils.response_has_string(response, 'Password and Retype Password did not match')


def test_login_form_with_username(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.login_with_username = True

    # ****************
    # ** Valid Form **
    # ****************

    test_utils.login(client, USERNAME1, '')
    test_utils.logout(client)

    # ******************
    # ** Invalid Form **
    # ******************

    # Test empty username
    response = post_login_form(client, '', None)
    assert test_utils.response_has_string(response, 'Username is required')

    # Test incorrect username
    response = post_login_form(client, 'user9', None, 'Password1')
    assert test_utils.response_has_string(response, 'Incorrect Username and Password')

    # Test empty password
    response = post_login_form(client, USERNAME1, None, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test incorrect password
    response = post_login_form(client, USERNAME1, None, 'Password9')
    assert test_utils.response_has_string(response, 'Incorrect Username and Password')

def test_login_form_with_email(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.login_with_username = False

    # ****************
    # ** Valid Form **
    # ****************

    test_utils.login(client, '', EMAIL1)
    test_utils.logout(client)

    # Test empty email
    response = post_login_form(client, '', None)
    assert test_utils.response_has_string(response, 'Email is required')

    # Test incorrect email
    response = post_login_form(client, None, 'email9@example.com', 'Password1')
    assert test_utils.response_has_string(response, 'Incorrect Email and Password')

    # Test empty password
    response = post_login_form(client, None, EMAIL1, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test incorrect password
    response = post_login_form(client, None, EMAIL1, 'Password9')
    assert test_utils.response_has_string(response, 'Incorrect Email and Password')


def test_change_username_form(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.login_with_username = True

    # Log in as 'user1'
    test_utils.login(client, 'user1')

    # ****************
    # ** Valid Form **
    # ****************

    # Change username to 'user3'
    response = post_change_username_form(client, 'user3')
    assert test_utils.response_has_no_errors(response)
    
    # Log out and login with new username
    test_utils.logout(client)
    test_utils.login(client, 'user3')

    # Change username back to 'user1'
    response = post_change_username_form(client, 'user1')
    assert test_utils.response_has_no_errors(response)

    # *******************
    # ** Invalid Forms **
    # *******************

    new_username = 'user4'

    # Test empty username
    response = post_change_username_form(client, '')
    assert test_utils.response_has_string(response, 'Username is required')

    # Test short username
    response = post_change_username_form(client, SHORT_USERNAME)
    assert test_utils.response_has_string(response, 'Username must be at least 3 characters long')

    # Test existing username
    response = post_change_username_form(client, 'user2')
    assert test_utils.response_has_string(response, 'This Username is no longer available. Please try another one.')

    # Test empty password
    response = post_change_username_form(client, new_username, '')
    assert test_utils.response_has_string(response, 'Old Password is required')

    # Test incorrect password
    response = post_change_username_form(client, new_username, 'ABde12')
    assert test_utils.response_has_string(response, 'Old Password is incorrect')

    test_utils.logout(client)

def test_change_password_form(client):
    # Set user manager config
    user_manager =  current_app.user_manager
    user_manager.enable_registration = True
    user_manager.login_with_username = True

    # ****************
    # ** Valid Form **
    # ****************

    # Log in as 'user1'
    test_utils.login(client, 'user1', '', PASSWORD1)

    # Change password to 'Password9' with retype_password
    user_manager.retype_password = True
    response = post_change_password_form(client, PASSWORD1, 'Password9')
    assert test_utils.response_has_no_errors(response)
    
    # Log out and login with new password
    test_utils.logout(client)
    test_utils.login(client, 'user1', '', 'Password9')

    # Change password back to 'Password1' without retype_password
    user_manager.retype_password = False
    response = post_change_password_form(client, 'Password9', PASSWORD1)
    assert test_utils.response_has_no_errors(response)

    test_utils.logout(client)

    # *******************
    # ** Invalid Forms **
    # *******************

    # Log in as 'user1'
    test_utils.login(client, 'user1')
    user_manager.retype_password = True

    # Test empty old password
    response = post_change_password_form(client, '', 'Password2')
    assert test_utils.response_has_string(response, 'Old Password is required')

    # Test incorrect old password
    response = post_change_password_form(client, 'ABde12', 'Password2')
    assert test_utils.response_has_string(response, 'Old Password is incorrect')

    # Test empty password
    response = post_change_password_form(client, PASSWORD1, '')
    assert test_utils.response_has_string(response, 'New Password is required')

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        response = post_change_password_form(client, PASSWORD1, invalid_password)
        assert test_utils.response_has_string(response, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number')

    # Test non-matching passwords
    response = post_change_password_form(client, PASSWORD1, 'Password2', 'Password9')
    assert test_utils.response_has_string(response, 'New Password and Retype Password did not match')

    test_utils.logout(client)

# TODO: register with require_email_confirmation=True/False
# TODO: add tests for post_confirm_email()
