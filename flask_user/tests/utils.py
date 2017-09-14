import datetime

from flask_login import login_user, current_user

def utils_prepare_user(app):
    um = app.user_manager
    db_manager=um.db_manager
    db_adapter = db_manager.db_adapter
    User = db_manager.UserClass
    UserEmail = db_manager.UserEmailClass

    # Get or create test user
    test_user = User.query.filter(User.email=='testuser@example.com').first()
    if not test_user:
        password_hash = um.password_manager.hash_password('Password1')
        test_user = User(password=password_hash)
        db_adapter.add_object(test_user)

    # NB: password_manager.hash_password() seems to mess up the request context
    test_user.active = True
    test_user.username = 'testuser'
    test_user.email = 'testuser@example.com'
    test_user.email_confirmed_at = datetime.datetime.utcnow()
    test_user.first_name = 'Firstname'
    test_user.last_name = 'Lastname'
    db_adapter.save_object(test_user)
    db_adapter.commit()

    return test_user
