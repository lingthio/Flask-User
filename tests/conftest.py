"""
    tests.conftest
    --------------
    py.test config file for automated tests

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

import pytest

from example_apps.basic_app import create_app
from tests.tstutils import TstClient

print("========== tests/conftest.py ==========")

# create app once
print("Creating app")

test_config = dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',   # In-memory sqlite DB
    WTF_CSRF_ENABLED=False,  # Disable CSRF token in Flask-Wtf
    LOGIN_DISABLED=False,    # Enable @register_required while app.testing=True
    MAIL_SUPPRESS_SEND=True, # Suppress the sending of emails
    SERVER_NAME='localhost'  # Enable url_for() without request context
)
_app = create_app(test_config)
_app.testing = True                       # Propagate exceptions (don't show 500 error page)
ctx = _app.app_context()
ctx.push()

_db = _app.db

# print 'urlmap:'
# for rule in _app.url_map.iter_rules():
#         print rule.endpoint, rule

# init db once
print("Creating db")
_db.create_all()

print("Performing tests ...")

@pytest.fixture(scope='module')
def app():
    return _app

@pytest.fixture(scope='module')
def db():
    return _db

@pytest.fixture(scope='module')
def client(app):
    client = TstClient(app.test_client())
    return client


# There is a problem with pytest-cov in that the recommended command:
#    py.test --cov app tests/
# produces inaccurate numbers.
#
# For now, we can use this command:
#    coverage run --source app --omit app/env_settings_example.py tests/conftest.py
# But this requires that we call all the test functions explicitly.
# - Make sure to import all the test files below.
# - Make sure each file's run_all_tests() function calls all test functions in that file.
if __name__ == '__main__':
    from tests import test_valid_forms
    from tests import test_invalid_forms

    test_valid_forms.run_all_tests(client(app()), db())
    test_invalid_forms.run_all_tests(client(app()), db())


