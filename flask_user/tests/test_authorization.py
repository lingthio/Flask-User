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

def test_authorization(client):
    """
    Test various authorization scenarios
    """
    um = current_app.user_manager
    um.enable_register = True
    um.enable_username = True
    um.enable_email = False
    um.enable_confirm_email = False
    um.enable_retype_password = False

    # Test as anonymous user
    client.get_valid_page(url_for('home_page'))
    client.get_invalid_page(url_for('user_profile_page'), "You must be signed in to access ")
    client.get_invalid_page(url_for('special_page'), "You must be signed in to access ")

    # Test as regular 'member' user
    client.login(username='member', password='Password1')
    client.get_valid_page(url_for('home_page'))
    client.get_valid_page(url_for('user_profile_page'))
    client.get_invalid_page(url_for('special_page'), "You do not have permission to access ")
    client.logout()

    # Test as special 'user007' user
    client.login(username='user007', password='Password1')
    client.get_valid_page(url_for('home_page'))
    client.get_valid_page(url_for('user_profile_page'))
    client.get_valid_page(url_for('special_page'))
    client.logout()

