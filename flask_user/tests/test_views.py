import datetime

from flask import url_for

from .utils import utils_prepare_user

# NB: This test MUST be the FIRST function in this file
def test_login_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    db_manager=um.db_manager
    db_adapter = db_manager.db_adapter

    # GET
    url = url_for('user.login')
    client.get_valid_page(url)

    # POST on inactive account
    user.active = False
    db_adapter.commit()
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True
    client.post_invalid_form(url, 'Your account has not been enabled.', username=user.username, password='Password1')
    user.active = True
    db_adapter.commit()

    # POST on unconfirmed email account
    user.email_confirmed_at = None
    db_adapter.commit()
    um.USER_ENABLE_CONFIRM_EMAIL = True
    client.post_invalid_form(url, 'Your email address has not yet been confirmed', username=user.username, password='Password1')
    user.email_confirmed_at = datetime.datetime.utcnow()
    db_adapter.commit()

    # POST with username
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True
    client.post_valid_form(url, username=user.username, password='Password1')
    client.post_valid_form(url_for('user.logout'))

    # POST with email through username field
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True
    client.post_valid_form(url, username=user.email, password='Password1')
    client.post_valid_form(url_for('user.logout'))

    # POST with email through email field
    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True
    client.post_valid_form(url, email=user.email, password='Password1')

def test_change_password_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_CHANGE_PASSWORD = True
    um.USER_REQUIRE_RETYPE_PASSWORD = False

    # GET
    url = url_for('user.change_password')
    client.get_valid_page(url)

    # POST
    old_password_hash = user.password
    client.post_valid_form(
        url,
        old_password='Password1',
        new_password='Password2'
    )

    # Verify operations
    assert user.password != old_password_hash

    # Restore password
    user.password = old_password_hash
    app.db.session.commit()

def test_change_username_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_CHANGE_USERNAME = True

    # GET
    url = url_for('user.change_username')
    client.get_valid_page(url)

    # POST
    old_username = user.username
    client.post_valid_form(
        url,
        old_password='Password1',
        new_username='username2'
    )

    # Verify operations
    assert user.username=='username2'

def test_confirm_email_view(app, client):
    user = utils_prepare_user(app)
    user.email_confirmed_at = None

    um = app.user_manager
    um.USER_ENABLE_REGISTER = True
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_CONFIRM_EMAIL = True


    # Generate confirmation token for user 1
    confirmation_token = um.generate_token(user.id)

    # GET with invalid token
    url = url_for('user.confirm_email', token='INVALID_TOKEN')
    client.get_invalid_page(url, 'Invalid confirmation token.')

    # GET with valid token
    url = url_for('user.confirm_email', token=confirmation_token)
    um.USER_AUTO_LOGIN_AFTER_CONFIRM = True
    client.get_valid_page(url)
    um.USER_AUTO_LOGIN_AFTER_CONFIRM = False
    client.get_valid_page(url)
    um.USER_AUTO_LOGIN_AFTER_CONFIRM = True

    # Verify operations
    assert user.email_confirmed_at

    # Restore
    pass

def test_edit_user_profile(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager

    # GET
    url = url_for('user.edit_user_profile')
    client.get_valid_page(url)

    # POST
    client.post_valid_form(
        url,
        first_name='Firstname2',
        last_name='Lastname2')

    # Verify operations
    assert user.first_name == 'Firstname2'
    assert user.last_name == 'Lastname2'

def test_email_action_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_MULTIPLE_EMAILS = True

    UserEmail = app.UserEmailClass
    db_manager=um.db_manager
    db_manager.UserEmailClass = UserEmail
    db_adapter = db_manager.db_adapter

    user_email1 = UserEmail(
        user=user,
        email='testuser1@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        is_primary=True,
    )
    app.db.session.add(user_email1)
    app.db.session.commit()

    # Add
    url = url_for('user.manage_emails')
    client.post_valid_form(url, email='testuser2@example.com')
    user_email2 = db_adapter.find_first_object(UserEmail, email='testuser2@example.com')
    assert user_email2

    # Confirm
    url = url_for('user.email_action', id=user_email2.id, action='confirm')
    client.get_valid_page(url)

    # Make primary
    url = url_for('user.email_action', id=user_email2.id, action='make-primary')
    client.get_valid_page(url)
    assert user_email2.is_primary
    user_email2.is_primary = False
    user_email1.is_primary = True
    app.db.session.commit()

    # Delete
    url = url_for('user.email_action', id=user_email2.id, action='delete')
    client.get_valid_page(url)
    user_email2 = db_adapter.find_first_object(UserEmail, email='testuser2@example.com')
    assert user_email2 is None

    # Restore UserManager settings
    um.USER_ENABLE_MULTIPLE_EMAILS = False
    db_manager.UserEmailClass = None

def test_forgot_password_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_FORGOT_PASSWORD = True

    # GET
    url = url_for('user.forgot_password')
    client.get_valid_page(url)

    # POST
    client.post_valid_form(url, email=user.email)

def test_invite_user_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_INVITE_USER = True
    db_adapter = um.db_manager.db_adapter

    # GET
    url = url_for('user.invite_user')
    client.get_valid_page(url)

    # POST existing email
    client.post_invalid_form(url, 'User with that email has already registered', email='testuser@example.com')

    # POST new email
    client.post_valid_form(url, email='inviteduser@example.com')

    db_manager = um.db_manager
    UserInvitation = db_manager.UserInvitationClass
    user_invitation = db_adapter.find_first_object(UserInvitation, email='inviteduser@example.com')
    assert user_invitation

def test_register_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    db_manager = um.db_manager
    db_adapter = db_manager.db_adapter

    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_INVITE_USER = True
    um.USER_SEND_REGISTERED_EMAIL = True
    um.USER_REQUIRE_RETYPE_PASSWORD = False
    um.USER_REQUIRE_INVITATION = True

    UserInvitation = db_manager.UserInvitationClass
    user_invitation = UserInvitation(email='inviteduser@example.com', invited_by_user=user)
    db_adapter.add_object(user_invitation)
    db_adapter.commit()

    # GET with USER_REQUIRE_INVITATION without a token
    url = url_for('user.register')
    client.get_invalid_page(url, 'Registration is invite only')

    # GET with USER_REQUIRE_INVITATION and an invalid token
    url = url_for('user.register', token='INVALID_TOKEN')
    client.get_invalid_page(url, 'Invalid invitation token')

    # GET with USER_REQUIRE_INVITATION and a valid token
    token = um.token_manager.generate_token(user_invitation.id)
    url = url_for('user.register', token=token)
    client.get_valid_page(url)

    # POST with USER_REQUIRE_INVITATION and a valid token
    url = url_for('user.register', token=token)
    client.post_valid_form(url, email=user_invitation.email, password='Password1')

    # POST with USER_ENABLE_CONFIRM_EMAIL=True
    um.USER_REQUIRE_INVITATION = False
    um.USER_ENABLE_CONFIRM_EMAIL = True
    url = url_for('user.register')
    client.post_valid_form(url, email='register1@example.com', password='Password1')

    # POST with USER_AUTO_LOGIN_AFTER_REGISTER=False and no reg_next
    um.USER_ENABLE_CONFIRM_EMAIL = False
    um.USER_AUTO_LOGIN_AFTER_REGISTER=False
    url = url_for('user.register')
    client.post_valid_form(url, email='register2@example.com', password='Password1')

    # POST with USER_AUTO_LOGIN_AFTER_REGISTER=True and reg_next
    um.USER_AUTO_LOGIN_AFTER_REGISTER = True
    url = url_for('user.register', reg_next='/')
    client.post_valid_form(url, email='register3@example.com', password='Password1')

def test_resend_email_confirmation_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_CONFIRM_EMAIL = True

    # GET
    url = url_for('user.resend_email_confirmation')
    client.get_valid_page(url)

    # POST
    client.post_valid_form(url, email=user.email)

def test_reset_password_view(app, client):
    user = utils_prepare_user(app)

    um = app.user_manager
    db_manager = um.db_manager
    db_adapter = db_manager.db_adapter

    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True
    um.USER_ENABLE_FORGOT_PASSWORD = True

    old_password_hash = user.password
    token = um.generate_token(user.id)

    # GET with invalid token
    url = url_for('user.reset_password', token='INVALID_TOKEN')
    client.get_invalid_page(url, 'Your reset password token is invalid')

    # GET with valid token
    url = url_for('user.reset_password', token=token)
    token = um.generate_token(user.id)
    client.get_valid_page(url)

    # POST with USER_AUTO_LOGIN_AFTER_RESET_PASSWORD=False
    url = url_for('user.reset_password', token=token)
    um.USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = False
    token = um.generate_token(user.id)
    client.post_valid_form(url, new_password='Password9')

    # POST with USER_AUTO_LOGIN_AFTER_RESET_PASSWORD=True
    um.USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True
    token = um.generate_token(user.id)
    client.post_valid_form(url, new_password='Password9')

    # Verify operations
    assert user.password!=old_password_hash

    # Restore password
    user.password = old_password_hash
    db_adapter.commit()


# NB: This test MUST be the LAST function in this file
def test_logout_view(app, client):
    # Submit form and verify that response has no errors
    url = url_for('user.logout')
    client.post_valid_form(url)
