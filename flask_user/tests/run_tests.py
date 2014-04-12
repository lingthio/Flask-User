"""
    flask_user.tests
    ----------------
    Automated tests for Flask-User

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from __future__ import print_function
import unittest

# Configure app
from flask_user.tests import test_valid_forms, test_authorization, tst_app, test_invalid_forms, tstutils

test_config = dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',   # In-memory sqlite DB
    WTF_CSRF_ENABLED=False,  # Disable CSRF token in Flask-Wtf
    LOGIN_DISABLED=False,    # Enable @register_required while app.testing=True
    MAIL_SUPPRESS_SEND=True, # Suppress the sending of emails
    SERVER_NAME='localhost'  # Enable url_for() without request context
)

# Create app
app = tst_app.create_app(test_config)
app.testing = True           # Propagate exceptions (don't show 500 error page)
db = app.user_manager.db_adapter.db

# create client
client = tstutils.TstClient(app.test_client(), db)

# Create test case
class TestFlaskUserForms(unittest.TestCase):
    """
    Automated tests for Flask-User forms
    """
    def test_authorization(self):
        with app.app_context():
            test_authorization.test_authorization(client)

    def test_valid_forms_with_email_login(self):
        with app.app_context():
            test_valid_forms.test_with_email(client)

    def test_valid_forms_with_username_login(self):
        with app.app_context():
            test_valid_forms.test_with_username(client)

    def test_invalid_forms(self):
        with app.app_context():
            test_invalid_forms.run_all_tests(client)

if __name__=='__main__':
    unittest.main()