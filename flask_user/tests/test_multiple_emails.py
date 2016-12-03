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

def test_multiple_emails(app, db, client):
    """
    Test 'multiple emails per user' feature
    """

    # Set Flask-User settings
    um = current_app.user_manager
    um.enable_register = True
    um.enable_username = False
    um.enable_email = True
    um.enable_confirm_email = True
    um.enable_change_username = False
    um.enable_change_password = False
    um.enable_forgot_password = False
    um.enable_multiple_emails = True
    um.enable_retype_password = False

    # Adjust DbAdapter settings
    um.db_adapter.UserEmailClass = app.UserEmailClass

    # Adjust URL routes
    app.add_url_rule(um.email_action_url,  'user.email_action',  um.email_action_view_function)
    app.add_url_rule(um.manage_emails_url, 'user.manage_emails', um.manage_emails_view_function, methods=['GET', 'POST'])

    # constants
    EMAIL1 = 'email1@multi-email.com'
    EMAIL2 = 'email2@multi-email.com'
    PASSWORD = 'Password1'

    # Register user
    response = client.post_valid_form(url_for('user.register'), email=EMAIL1, password=PASSWORD)
    user_email1 = um.db_adapter.UserEmailClass.query.filter(um.db_adapter.UserEmailClass.email==EMAIL1).first()
    assert user_email1 != None

    # Confirm email
    confirmation_token = um.generate_token(user_email1.id)
    client.get_valid_page(url_for('user.confirm_email', token=confirmation_token))

    # Log in using email1
    client.login(email=EMAIL1, password=PASSWORD)

    # Visit manage emails page
    response = client.get_valid_page(url_for('user.manage_emails'))
    assert response.data.find(str.encode(EMAIL1)) >= 0

    # Add an email
    response = client.post_valid_form(url_for('user.manage_emails'), email=EMAIL2)
    assert response.data.find(str.encode(EMAIL1)) >= 0
    assert response.data.find(str.encode(EMAIL2)) >= 0
    user_email2 = um.db_adapter.UserEmailClass.query.filter(um.db_adapter.UserEmailClass.email==EMAIL2).first()
    assert user_email2 != None

    # Confirm email
    confirmation_token = um.generate_token(user_email2.id)
    client.get_valid_page(url_for('user.confirm_email', token=confirmation_token))

    # Logout
    client.logout()

    # Log in using email1
    client.login(email=EMAIL1, password=PASSWORD)

    # Logout
    client.logout()

    # Log in using email2
    client.login(email=EMAIL2, password=PASSWORD)

    # Confirm
    response = client.get_valid_page(url_for('user.email_action', id=user_email2.id, action='confirm'))

    # Make primary
    response = client.get_valid_page(url_for('user.email_action', id=user_email2.id, action='make-primary'))

    # Delete
    response = client.get_valid_page(url_for('user.email_action', id=user_email1.id, action='delete'))

    # Logout
    client.logout()

    # Restore settings
    um.enable_multiple_emails = False
    um.enable_confirm_email = True
    um.enable_retype_password = True
    um.db_adapter.UserEmailClass = None

