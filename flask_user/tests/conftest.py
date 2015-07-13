import os
import pytest

from flask_user.tests.tst_app import app as the_app, init_app
from flask_user.tests.tst_utils import TstClient

@pytest.fixture(scope='session')
def app(request):
    test_config = dict(
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',   # In-memory sqlite DB
        TESTING=True,            # Propagate exceptions (don't show 500 error page)
        WTF_CSRF_ENABLED=False,  # Disable CSRF token in Flask-Wtf
        LOGIN_DISABLED=False,    # Enable @register_required while app.testing=True
        MAIL_SUPPRESS_SEND=True, # Suppress the sending of emails
        SERVER_NAME='localhost'  # Enable url_for() without request context
    )

    # Create app with test settings
    init_app(the_app, test_config)

    # Establish an application context before running the tests.
    ctx = the_app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return the_app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        app.db.drop_all()

    app.db.create_all()

    request.addfinalizer(teardown)
    return app.db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture(scope='session')
def client(app, db, request):
    return TstClient(app.test_client(), db)

