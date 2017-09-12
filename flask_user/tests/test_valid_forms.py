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
VALID_USERNAME = 'valid1'
VALID_EMAIL = 'valid1@example.com'
VALID_PASSWORD = 'Password1'
INVITE_USER_EMAIL = 'valid2@example.com'
# Using global variable for speed
valid_user = None
valid_user_invitation = None

# ********************************
# ** Automatically called Tests **
# ********************************
# The 'client' and 'app' parameters are set up in conftest.py
# Functions that start with 'test' will be run automatically by the test suite runner (py.test)

def test_with_email(client):
    """
    Test all forms with all enabled features and USER_ENABLE_USERNAME=False
    """
    um = current_app.user_manager
    um.USER_ENABLE_REGISTER = True
    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True          # Login with email
    um.USER_ENABLE_CONFIRM_EMAIL = True
    um.USER_ENABLE_CHANGE_USERNAME = False
    um.USER_ENABLE_CHANGE_PASSWORD = True
    um.USER_ENABLE_FORGOT_PASSWORD = True
    um.USER_ENABLE_MULTIPLE_EMAILS = False
    um.USER_REQUIRE_RETYPE_PASSWORD = True

    check_all_valid_forms(um, client)

def test_with_username(client):
    """
    Test all forms with all enabled features and USER_ENABLE_USERNAME=True
    """
    # Enable all features
    um = current_app.user_manager
    um.USER_ENABLE_REGISTER = True
    um.USER_ENABLE_USERNAME = True       # Login with username
    um.USER_ENABLE_EMAIL = False
    um.USER_ENABLE_CONFIRM_EMAIL = False
    um.USER_ENABLE_CHANGE_USERNAME = True
    um.USER_ENABLE_CHANGE_PASSWORD = True
    um.USER_ENABLE_FORGOT_PASSWORD = False
    um.USER_ENABLE_MULTIPLE_EMAILS = False
    um.USER_REQUIRE_RETYPE_PASSWORD = True

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

    for um.USER_ENABLE_REGISTER in (True, False):
      for um.USER_ENABLE_EMAIL in (True, False):
        for um.USER_REQUIRE_RETYPE_PASSWORD in (True, False):
          for um.USER_ENABLE_CONFIRM_EMAIL in (True, False):
            for um.USER_ENABLE_USERNAME in (True, False):
              for um.USER_ENABLE_CHANGE_PASSWORD in (True, False):
                for um.USER_ENABLE_CHANGE_USERNAME in (True, False):
                  for um.USER_ENABLE_FORGOT_PASSWORD in (True, False):
                    for um.USER_ENABLE_INVITE_USER in (True, False):
                        check_all_valid_forms(um, client, db)

# **************************
# ** Check Form Functions **
# **************************
# Below we check each form by submitting fields depending on the config settings.

def check_all_valid_forms(um, client):
    # ** Skip tests for invalid config combinations
    # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.
    if um.USER_ENABLE_REGISTER and not um.USER_ENABLE_EMAIL and not um.USER_ENABLE_USERNAME: return
    # USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True
    if um.USER_ENABLE_CONFIRM_EMAIL and not um.USER_ENABLE_EMAIL: return
    # USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True
    if um.USER_ENABLE_MULTIPLE_EMAILS and not um.USER_ENABLE_EMAIL: return
    # ENABLE_CHANGE_USERNAME=True must have ENABLE_USERNAME=True.
    if um.USER_ENABLE_CHANGE_USERNAME and not um.USER_ENABLE_USERNAME: return

    check_valid_register_form(um, client, client.db)
    check_valid_confirm_email_page(um, client)
    check_valid_login_form(um, client)
    check_valid_change_password_form(um, client)
    check_valid_change_username_form(um, client)
    check_valid_logout_link(um, client)
    check_valid_resend_email_confirmation_form(um, client)
    check_valid_forgot_password_form(um, client)
    check_valid_reset_password_page(um, client)
    check_valid_invite_email(um, client)
    #check_valid_invite_registration_different_email(um, client)

    delete_valid_user(client.db)
    delete_valid_user_invitation(client.db)

def check_valid_register_form(um, client, db):
    # Using global variable for speed
    global valid_user
    User = um.db_manager.UserClass

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.USER_ENABLE_USERNAME:
        kwargs['username'] = VALID_USERNAME
    if um.USER_ENABLE_EMAIL:
        kwargs['email'] = VALID_EMAIL
    kwargs['password'] = VALID_PASSWORD

    if um.USER_ENABLE_REGISTER:
        print("test_valid_register_form")

        # Create User by submitting a form
        if um.USER_REQUIRE_RETYPE_PASSWORD:
            kwargs['retype_password'] = VALID_PASSWORD

        # Submit form and verify that response has no errors
        client.post_valid_form(url_for('user.register'), **kwargs)

        if um.USER_ENABLE_USERNAME:
            valid_user = um.db_manager.find_user_by_username(VALID_USERNAME)

        else:
            valid_user = um.db_manager.db_adapter.find_first_object(User, email=VALID_EMAIL)
        assert valid_user

    else:
        # Create user record manually

        # hash password
        kwargs['password'] = um.hash_password(VALID_PASSWORD)

        # Create User
        valid_user = User(email_confirmed_at=datetime.datetime.utcnow(), **kwargs)
        db.session.add(valid_user)
        um.db_manager.commit()
        assert valid_user

def check_valid_resend_email_confirmation_form(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_REGISTER: return
    if not um.USER_ENABLE_EMAIL: return
    if not um.USER_ENABLE_CONFIRM_EMAIL: return

    print("test_valid_resend_email_confirmation_form")

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.resend_email_confirmation'), email=VALID_EMAIL)

def check_valid_confirm_email_page(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_REGISTER: return
    if not um.USER_ENABLE_EMAIL: return
    if not um.USER_ENABLE_CONFIRM_EMAIL: return

    print("test_valid_confirm_email_page")
    global valid_user

    # Generate confirmation token for user 1
    confirmation_token = um.generate_token(valid_user.id)

    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.confirm_email', token=confirmation_token))

    # Verify operations
    valid_user = um.db_manager.db_adapter.get_object(um.db_manager.UserClass, valid_user.id)
    assert valid_user.email_confirmed_at != None

def check_valid_login_form(um, client):
    print("test_valid_login_form")

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.USER_ENABLE_USERNAME:
        kwargs['username'] = VALID_USERNAME
    if um.USER_ENABLE_EMAIL:
        kwargs['email'] = VALID_EMAIL
    kwargs['password'] = VALID_PASSWORD

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.login'), **kwargs)

    # Verify operations
    # TODO:

def check_valid_change_password_form(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_CHANGE_PASSWORD: return

    print("test_valid_change_password_form")
    global valid_user

    # Define defaults
    new_password = 'Password9'
    old_password_hash = valid_user.password

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['old_password'] = VALID_PASSWORD
    kwargs['new_password'] = new_password
    if um.USER_REQUIRE_RETYPE_PASSWORD:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_password'), **kwargs)

    # Verify operations
    valid_user = um.db_manager.db_adapter.get_object(um.db_manager.UserClass, valid_user.id)
    # deliberately test verify_password with deprecated user param (instead of user.password)
    assert um.verify_password(new_password, valid_user)

    # Change password back to old password for subsequent tests
    valid_user.password=old_password_hash
    um.db_manager.save_object(valid_user)
    um.db_manager.commit()

def check_valid_change_username_form(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_CHANGE_USERNAME: return

    print("test_valid_change_username_form")
    global valid_user

    new_username = 'user9'

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_username'), new_username=new_username, old_password=VALID_PASSWORD)

    # Verify operations
    valid_user = um.db_manager.db_adapter.get_object(um.db_manager.UserClass, valid_user.id)
    assert valid_user.username == new_username

    # Change username back to old password for subsequent tests
    valid_user.username = VALID_USERNAME

def check_valid_logout_link(um, client):
    print("test_valid_logout_link")
    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.logout'))

def check_valid_forgot_password_form(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_EMAIL: return
    if not um.USER_ENABLE_FORGOT_PASSWORD: return

    print("test_valid_forgot_password_form")

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.forgot_password'), email=VALID_EMAIL)

def check_valid_reset_password_page(um, client):
    # Skip test for certain config combinations
    if not um.USER_ENABLE_EMAIL: return
    if not um.USER_ENABLE_FORGOT_PASSWORD: return

    print("test_valid_reset_password_page")
    global valid_user

    # Simulate a valid forgot password form
    token = um.generate_token(valid_user.id)

    # Define defaults
    password = 'Password1'
    new_password = 'Password9'
    old_password_hash = valid_user.password
    url = url_for('user.reset_password', token=token)

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['new_password'] = new_password
    if um.USER_REQUIRE_RETYPE_PASSWORD:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url, **kwargs)

    # Verify operations
    valid_user = um.db_manager.db_adapter.get_object(um.db_manager.UserClass, valid_user.id)
    assert um.verify_password(new_password, valid_user.password)

    # Change password back to old password for subsequent tests
    valid_user.password = old_password_hash

def check_valid_invite_email(um, client):
    """ If a valid email is submitted using the invite form,
    then it should generate the proper email and response """
    if not um.USER_ENABLE_INVITE_USER: return
    # Submit form and verify that response has no errors
    global valid_user_invitation
    UserInvitation = um.UserInvitationClass
    client.login(username='member', email='member@example.com', password='Password1')
    client.post_valid_form(url_for('user.invite_user'), email=INVITE_USER_EMAIL)
    valid_user_invitation = um.db_manager.db_adapter.find_first_object(UserInvitation, email=INVITE_USER_EMAIL)
    assert valid_user_invitation

def delete_valid_user(db):
    # Using global variable for speed
    global valid_user

    if valid_user:
        # Delete valid_user
        um = current_app.user_manager
        um.db_manager.delete_object(valid_user)
        um.db_manager.commit()
        valid_user = None

def delete_valid_user_invitation(db):
    # Using global variable for speed
    global valid_user_invitation

    if valid_user_invitation:
        # Delete valid_user_invitation
        um = current_app.user_manager
        um.db_manager.delete_object(valid_user_invitation)
        um.db_manager.commit()
        valid_user_invitation = None
