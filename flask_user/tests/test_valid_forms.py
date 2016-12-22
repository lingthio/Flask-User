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
valid_user_invite = None

# ********************************
# ** Automatically called Tests **
# ********************************
# The 'client' and 'app' parameters are set up in conftest.py
# Functions that start with 'test' will be run automatically by the test suite runner (py.test)

def test_with_email(client):
    """
    Test all forms with all enabled features and enable_username=False
    """
    print('test_with_email()')

    um = current_app.user_manager
    um.enable_register = True
    um.enable_username = False
    um.enable_email = True          # Login with email
    um.enable_confirm_email = True
    um.enable_change_username = False
    um.enable_change_password = True
    um.enable_forgot_password = True
    um.enable_multiple_emails = False
    um.enable_retype_password = True

    check_all_valid_forms(um, client)

def test_with_username(client):
    """
    Test all forms with all enabled features and enable_username=True
    """
    print('test_with_username()')

    # Enable all features
    um = current_app.user_manager
    um.enable_register = True
    um.enable_username = True       # Login with username
    um.enable_email = False
    um.enable_confirm_email = False
    um.enable_change_username = True
    um.enable_change_password = True
    um.enable_forgot_password = False
    um.enable_multiple_emails = False
    um.enable_retype_password = True

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
            for um.enable_username in (True, False):
              for um.enable_change_password in (True, False):
                for um.enable_change_username in (True, False):
                  for um.enable_forgot_password in (True, False):
                    for um.enable_invitation in (True, False):
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
    check_valid_resend_confirm_email_form(um, client)
    check_valid_confirm_email_page(um, client)
    check_valid_login_form(um, client)
    check_valid_change_password_form(um, client)
    check_valid_change_username_form(um, client)
    check_valid_logout_link(um, client)
    check_valid_forgot_password_form(um, client)
    check_valid_reset_password_page(um, client)
    check_valid_invite_email(um, client)
    #check_valid_invite_registration_different_email(um, client)

    delete_valid_user(client.db)
    delete_valid_user_invite(client.db)

def check_valid_register_form(um, client, db):
    # Using global variable for speed
    global valid_user
    User = um.db_adapter.UserClass

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.enable_username:
        kwargs['username'] = VALID_USERNAME
    if um.enable_email:
        kwargs['email'] = VALID_EMAIL
    kwargs['password'] = VALID_PASSWORD

    if um.enable_register:
        print("test_valid_register_form")

        # Create User by submitting a form
        if um.enable_retype_password:
            kwargs['retype_password'] = VALID_PASSWORD

        # Submit form and verify that response has no errors
        client.post_valid_form(url_for('user.register'), **kwargs)

        if um.enable_username:
            valid_user = User.query.filter(User.username==VALID_USERNAME).first()
        else:
            valid_user = User.query.filter(User.email==VALID_EMAIL).first()
        assert valid_user

        # Verify operations
        assert valid_user.active

    else:
        # Create user record manually

        # hash password
        kwargs['password'] = um.hash_password(VALID_PASSWORD)

        # Create User
        valid_user = User(active=True, confirmed_at=datetime.datetime.utcnow(), **kwargs)
        db.session.add(valid_user)
        db.session.commit()
        assert valid_user

def check_valid_resend_confirm_email_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_register: return
    if not um.enable_email: return
    if not um.enable_confirm_email: return

    print("test_valid_resend_confirm_email_form")

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.resend_confirm_email'), email=VALID_EMAIL)

def check_valid_confirm_email_page(um, client):
    # Skip test for certain config combinations
    if not um.enable_register: return
    if not um.enable_email: return
    if not um.enable_confirm_email: return

    print("test_valid_confirm_email_page")

    # Generate confirmation token for user 1
    confirmation_token = um.generate_token(valid_user.id)

    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.confirm_email', token=confirmation_token))

    # Verify operations
    assert valid_user.active
    assert valid_user.confirmed_at != None

def check_valid_login_form(um, client):
    print("test_valid_login_form")

    # Build variable argument list depending on config settings
    kwargs = {}
    if um.enable_username:
        kwargs['username'] = VALID_USERNAME
    if um.enable_email:
        kwargs['email'] = VALID_EMAIL
    kwargs['password'] = VALID_PASSWORD

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.login'), **kwargs)

    # Verify operations
    # TODO:

def check_valid_change_password_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_change_password: return

    print("test_valid_change_password_form")

    # Define defaults
    new_password = 'Password9'
    old_hashed_password = valid_user.password

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['old_password'] = VALID_PASSWORD
    kwargs['new_password'] = new_password
    if um.enable_retype_password:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_password'), **kwargs)

    # Verify operations
    assert um.verify_password(new_password, valid_user)

    # Change password back to old password for subsequent tests
    valid_user.password = old_hashed_password

def check_valid_change_username_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_change_username: return

    print("test_valid_change_username_form")

    new_username = 'user9'

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.change_username'), new_username=new_username, old_password=VALID_PASSWORD)

    # Verify operations
    assert valid_user.username == new_username

    # Change username back to old password for subsequent tests
    valid_user.username = VALID_USERNAME

def check_valid_logout_link(um, client):
    print("test_valid_logout_link")
    # Retrieve page and verify that response has no errors
    client.get_valid_page(url_for('user.logout'))

def check_valid_forgot_password_form(um, client):
    # Skip test for certain config combinations
    if not um.enable_email: return
    if not um.enable_forgot_password: return

    print("test_valid_forgot_password_form")

    # Submit form and verify that response has no errors
    client.post_valid_form(url_for('user.forgot_password'), email=VALID_EMAIL)

def check_valid_reset_password_page(um, client):
    # Skip test for certain config combinations
    if not um.enable_email: return
    if not um.enable_forgot_password: return

    print("test_valid_reset_password_page")

    # Simulate a valid forgot password form
    token = um.generate_token(valid_user.id)

    # Define defaults
    password = 'Password1'
    new_password = 'Password9'
    old_hashed_password = valid_user.password
    url = url_for('user.reset_password', token=token)

    # Build variable argument list depending on config settings
    kwargs = {}
    kwargs['new_password'] = new_password
    if um.enable_retype_password:
        kwargs['retype_password'] = new_password

    # Submit form and verify that response has no errors
    client.post_valid_form(url, **kwargs)

    # Verify operations
    assert um.verify_password(new_password, valid_user)

    # Change password back to old password for subsequent tests
    valid_user.password = old_hashed_password

def check_valid_invite_email(um, client):
    """ If a valid email is submitted using the invite form,
    then it should generate the proper email and response """
    if not um.enable_invitation: return
    # Submit form and verify that response has no errors
    global valid_user_invite
    UserInvite = um.db_adapter.UserInvitationClass
    client.login(username='member', email='member@example.com', password='Password1')
    client.post_valid_form(url_for('user.invite'), email=INVITE_USER_EMAIL)
    valid_user_invite = UserInvite.query.filter(UserInvite.email==INVITE_USER_EMAIL).first()
    assert valid_user_invite

def delete_valid_user(db):
    # Using global variable for speed
    global valid_user

    # Delete valid_user
    db.session.delete(valid_user)
    db.session.commit()
    valid_user = None

def delete_valid_user_invite(db):
    global valid_user_invite

    db.session.delete(valid_user_invite)
    db.session.commit()
    valid_user_invite = None
