"""
    tests.test_all_forms.py
    ---------------------------
    Flask-User automated tests:
    Tests posting a sequence of valid forms for all possible config combinations

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from __future__ import print_function

import datetime

from flask import current_app, url_for

# **********************
# ** Global Variables **
# **********************
# Using global variable for speed
user1 = None

# ********************************
# ** Automatically called Tests **
# ********************************
# The 'client' and 'app' parameters are set up in conftest.py
# Functions that start with 'test' will be run automatically by the test suite runner (py.test)

def test_with_email(client):
    """
    Test all forms with all enabled features and enable_username=False
    """
    print()

    um = current_app.user_manager
    um.enable_register = True
    um.enable_confirm_email = True
    um.enable_username = False
    um.enable_change_username = False
    um.enable_change_password = True
    um.enable_forgot_password = True

    um.enable_username = False      # Login with email
    check_all_valid_forms(um, client)

def test_with_username(client):
    """
    Test all forms with all enabled features and enable_username=True
    """
    print()

    # Enable all features
    um = current_app.user_manager
    um.enable_register = True
    um.enable_email = False
    um.enable_confirm_email = False
    um.enable_change_username = True
    um.enable_change_password = True
    um.enable_forgot_password = True

    # Login with username
    um.enable_username = True       # Login with username
    check_all_valid_forms(um, client)

# *****************************
# ** Explicitly called Tests **
# *****************************
# These function names may not start with 'test'

def do_test_all_possible_config_combinations(client, db):
    """
    Test all forms with all possible config combinations
    """
    print()
    print("Testing all forms for all possible config combinations")
    um =  current_app.user_manager
    
    for um.enable_register in (True, False):
      for um.enable_email in (True, False):
        for um.enable_retype_password in (True, False):
          for um.enable_confirm_email in (True, False):
            print("Config:", um.enable_register, um.enable_email, um.enable_retype_password, um.enable_confirm_email, "...")
            for um.enable_username in (True, False):
              for um.enable_change_password in (True, False):
                for um.enable_change_username in (True, False):
                  for um.enable_forgot_password in (True, False):
                    check_all_valid_forms(um, client, db)

# **************************
# ** Check Form Functions **
# **************************
# Below we check each form by submitting fields depending on the config settings.

def check_all_valid_forms(um, client):
    # ** Skip tests for invalid config combinations
    # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.
    if um.enable_register and not um.enable_email and not um.enable_username: return
    # USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True
    if um.enable_confirm_email and not um.enable_email: return
    # USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True
    if um.enable_multiple_emails and not um.enable_email: return
    # ENABLE_CHANGE_USERNAME=True must have ENABLE_USERNAME=True.
    if um.enable_change_username and not um.enable_username: return

    check_valid_register_form(um, client, client.db)
    check_valid_confirm_email_page(um, client)
    check_valid_login_form(um, client)
    check_valid_change_password_form(um, client)
    check_valid_change_username_form(um, client)
    check_valid_logout_link(um, client)
    check_valid_forgot_password_form(um, client)
    check_valid_reset_password_page(um, client)

    delete_user1(client.db)

def check_valid_register_form(um, client, db):
    # Using global variable for speed
    global user1
    User = um.db_adapter.UserClass

    # Define defaults
    username = 'user1'
    email = username+'@example.com'
    password = 'Password1'

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.enable_username:
        kwargs['username'] = username
    if um.enable_email:
        kwargs['email'] = email
    kwargs['password'] = password

    if um.enable_register:
        print("test_valid_register_form")

        # Create User by submitting a form
        if um.enable_retype_password:
            kwargs['retype_password'] = password

        # Submit form and verify that response has no errors
        client.post_valid_form(url_for('user.register'), **kwargs)

        if um.enable_username:
            user1 = User.query.filter(User.username==username).first()
        else:
            user1 = User.query.filter(User.email==email).first()
        assert user1

        # Verify operations
        if um.enable_confirm_email:
            assert not user1.active
        else:
            assert user1.active

    else:
        # Create user record manually

        # hash password
        kwargs['password'] = um.hash_password(password)

        # Create User
        user1 = User(active=True, confirmed_at=datetime.datetime.utcnow(), **kwargs)
        db.session.add(user1)
        db.session.commit()
        assert user1

def check_valid_confirm_email_page(um, client):
    # Skip test for certain config combinations
    if not um.enable_register: return
    if not um.enable_email: return
    if not um.enable_confirm_email: return

    print("test_valid_confirm_email_page")

    # Generate confirmation token for user 1
    confirmation_token = um.generate_token(user1.id)

    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.confirm_email', token=confirmation_token))

    # Verify operations
    assert user1.active
    assert user1.confirmed_at != None

def check_valid_login_form(um, client):
    print("test_valid_login_form")

    # Define defaults
    username = 'user1'
    email = username+'@example.com'
    password = 'Password1'

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.enable_username:
        kwargs['username'] = username
    if um.enable_email:
        kwargs['email'] = email
    kwargs['password'] = password

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.login'), **kwargs)

    # Verify operations
    # TODO:

def check_valid_change_password_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_change_password: return

    print("test_valid_change_password_form")

    # Define defaults
    password = 'Password1'
    new_password = 'Password9'
    old_hashed_password = user1.password

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['old_password'] = password
    kwargs['new_password'] = new_password
    if um.enable_retype_password:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_password'), **kwargs)

    # Verify operations
    assert um.verify_password(new_password, user1.password)

    # Change password back to old password for subsequent tests
    user1.password = old_hashed_password

def check_valid_change_username_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_change_username: return

    print("test_valid_change_username_form")

    # Define defaults
    username = 'user1'
    password = 'Password1'
    new_username = 'user9'

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_username'), new_username=new_username, old_password=password)

    # Verify operations
    assert user1.username == new_username

    # Change username back to old password for subsequent tests
    user1.username = username

def check_valid_logout_link(um, client):
    print("test_valid_logout_link")
    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.logout'))

def check_valid_forgot_password_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_email: return
    if not um.enable_forgot_password: return

    print("test_valid_forgot_password_form")

    # Define defaults
    email = 'user1@example.com'

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.forgot_password'), email=email)

def check_valid_reset_password_page(um, client):
    # Skip test for certain config combinations
    if not um.enable_email: return
    if not um.enable_forgot_password: return

    print("test_valid_reset_password_page")

    # Simulate a valid forgot password form
    user1.reset_password_token = um.generate_token(user1.id)
    token = user1.reset_password_token

    # Define defaults
    password = 'Password1'
    new_password = 'Password9'
    old_hashed_password = user1.password
    url = url_for('user.reset_password', token=token)

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['new_password'] = new_password
    if um.enable_retype_password:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url, **kwargs)

    # Verify operations
    assert um.verify_password(new_password, user1.password)

    # Change password back to old password for subsequent tests
    user1.password = old_hashed_password


def delete_user1(db):
    # Using global variable for speed
    global user1

    # Delete user1
    db.session.delete(user1)
    db.session.commit()
    user1 = None

# Workaround for py.test coverage issue
def run_all_tests(client, db):
    test_with_username(client, db)
    test_with_email(client, db)
