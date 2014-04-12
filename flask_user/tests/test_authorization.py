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
    client.get_invalid_page(url_for('profile_page'), "You must be signed in to access ")
    client.get_invalid_page(url_for('special_page'), "You must be signed in to access ")

    # Register and Log in as user1 without any roles
    client.post_valid_form(url_for('user.register'),
            username='userX', password='Password1')
    client.login(username='userX', password='Password1')

    client.get_valid_page(url_for('home_page'))
    client.get_valid_page(url_for('profile_page'))
    client.get_invalid_page(url_for('special_page'), "You do not have permission to access ")

    # Delete userX
    User = um.db_adapter.UserClass
    user = User.query.filter(User.username=='userX').first()
    assert(user)
    client.db.session.delete(user)
    client.db.session.commit()

    # Log in as user007 without roles 'special' and 'agent'
    client.login(username='user007', password='Password1')

    client.get_valid_page(url_for('home_page'))
    client.get_valid_page(url_for('profile_page'))
    client.get_valid_page(url_for('special_page'))

    # Test translations.ngettext
    from flask_user.translations import ngettext
    count = 1
    text = ngettext('I have %(count)s apple', 'I have %(count)s apples', count, count=count)
    assert(text=='I have 1 apple')
    count = 2
    text = ngettext('I have %(count)s apple', 'I have %(count)s apples', count, count=count)
    assert(text=='I have 2 apples')


# Workaround for py.test coverage issue
def run_all_tests(client, db):
    test_authorization(client)
