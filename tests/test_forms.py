import time

from flask import current_app, url_for
from example_app.models import User
from tests import utils as test_utils

# *************
# ** Defines **
# *************
USERNAME1 = 'user1'
EMAIL1 = 'user1@example.com'
SHORT_USERNAME = 'Aa'
INVALID_EMAIL = 'user1.example.com'
invalid_passwords = (
    'Abcd1',        # too short
    'ABCabc',       # no digits
    'ABC123',       # no lower case letters
    'abc123',       # no upper case letters
)

# ***********************
# ** Utility functions **
# ***********************

# Submits a register form
def post_register_form(client, username=None, email=None, password='Password1', retype_password=None):
    url = url_for('user.register')
    if not retype_password:
        retype_password = password
    return client.post(url, follow_redirects=True, data=dict(
        username=username,
        email=email,
        password=password,
        retype_password=retype_password,
    ))

# Logs a user in using POST /account/login
def post_login(client, username=None, email=None, password='Password1'):
    url = url_for('user.login')
    return client.post(url, data=dict(
        username=username,
        email=email,
        password=password
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

def test_register_form_with_username(client):
    # Set user manager config
    um = current_app.user_manager
    um.feature_register = True
    um.login_with_username = True
    um.login_with_email = False
    um.register_with_retype_password = True

    # ****************
    # ** Valid Form **
    # ****************

    # Submit valid form
    username = USERNAME1
    response = post_register_form(client, username, '')
    assert response.status_code == 200
    assert test_utils.form_has_valid_fields(response)

    # Verify that the user account has been created
    user = User.query.filter(User.username==username).first()
    assert user
    assert user.username == username
    assert not user.active

    # *******************
    # ** Invalid Forms **
    # *******************

    username = 'user2'
    email = None

    # Test empty username
    response = post_register_form(client, '')
    assert test_utils.response_has_string(response, 'Username is required')

    # Test short username
    response = post_register_form(client, SHORT_USERNAME)
    assert test_utils.response_has_string(response, 'Username must be at least 3 characters long')

    # Test existing username
    response = post_register_form(client, USERNAME1)
    assert test_utils.response_has_string(response, 'This Username no longer available. Please try another one.')

    # Test empty password
    response = post_register_form(client, username, email, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test invalid password
    for invalid_password in invalid_passwords:
        response = post_register_form(client, username, email, invalid_password)
        assert test_utils.response_has_string(response, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number')

    # Test non-matching passwords
    response = post_register_form(client, username, email, 'Password1', 'Password9')
    assert test_utils.response_has_string(response, 'Password and Retype Password do not match')


def test_register_form_with_email(client):
    # Set user manager config
    um = current_app.user_manager
    um.feature_register = True
    um.login_with_username = False
    um.login_with_email = True
    um.register_with_retype_password = True

    # ****************
    # ** Valid Form **
    # ****************

    # Submit valid form
    email = EMAIL1
    response = post_register_form(client, '', email)
    assert response.status_code == 200
    assert test_utils.form_has_valid_fields(response)

    # Verify that the user account has been created
    user = User.query.filter(User.email==email).first()
    assert user
    assert user.email == email
    assert not user.active

    # *******************
    # ** Invalid Forms **
    # *******************

    username = None
    email = 'user2@example.com'

    # Test empty email
    response = post_register_form(client, username, '')
    assert test_utils.response_has_string(response, 'Email is required')

    # Test short email
    response = post_register_form(client, username, INVALID_EMAIL)
    assert test_utils.response_has_string(response, 'Invalid Email')

    # Test existing email
    response = post_register_form(client, username, EMAIL1)
    assert test_utils.response_has_string(response, 'This Email no longer available. Please try another one.')

    # Test empty password
    response = post_register_form(client, username, email, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test invalid password
    for invalid_password in invalid_passwords:
        response = post_register_form(client, username, email, invalid_password)
        assert test_utils.response_has_string(response, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number')

    # Test non-matching passwords
    response = post_register_form(client, username, email, 'Password1', 'Password9')
    assert test_utils.response_has_string(response, 'Password and Retype Password do not match')


def test_login_form_with_username(client):
    # Set user manager config
    um = current_app.user_manager
    um.feature_register = True
    um.login_with_username = True
    um.login_with_email = False

    # ****************
    # ** Valid Form **
    # ****************

    test_utils.login(client, USERNAME1, '')
    test_utils.logout(client)

    # ******************
    # ** Invalid Form **
    # ******************

    # Test empty username
    response = post_login(client, '', None)
    assert test_utils.response_has_string(response, 'Username is required')

    # Test incorrect username
    response = post_login(client, 'user9', None, 'Password1')
    assert test_utils.response_has_string(response, 'Incorrect Username and Password')

    # Test empty password
    response = post_login(client, USERNAME1, None, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test incorrect password
    response = post_login(client, USERNAME1, None, 'Password9')
    assert test_utils.response_has_string(response, 'Incorrect Username and Password')

def test_login_form_with_email(client):
    # Set user manager config
    um = current_app.user_manager
    um.feature_register = True
    um.login_with_username = False
    um.login_with_email = True

    # ****************
    # ** Valid Form **
    # ****************

    test_utils.login(client, '', EMAIL1)
    test_utils.logout(client)

    # Test empty email
    response = post_login(client, '', None)
    assert test_utils.response_has_string(response, 'Email is required')

    # Test incorrect email
    response = post_login(client, None, 'email9@example.com', 'Password1')
    assert test_utils.response_has_string(response, 'Incorrect Email and Password')

    # Test empty password
    response = post_login(client, None, EMAIL1, '')
    assert test_utils.response_has_string(response, 'Password is required')

    # Test incorrect password
    response = post_login(client, None, EMAIL1, 'Password9')
    assert test_utils.response_has_string(response, 'Incorrect Email and Password')
