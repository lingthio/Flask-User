from flask import url_for

from .utils import utils_prepare_user

invalid_usernames = (
    'with space',
    'with&symbol',
    "with'symbol",
    )
invalid_passwords = (
    'Abcd1',        # too short
    'ABCabc',       # no digits
    'ABC123',       # no lower case letters
    'abc123',       # no upper case letters
    )

def test_invalid_register(app, client):
    um =  app.user_manager
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True
    um.USER_REQUIRE_RETYPE_PASSWORD = True

    user = utils_prepare_user(app)

    # Set default values
    url = url_for('user.register')
    username = user.username
    email = user.email
    password = 'Password1'

    # Invalid usernames
    # -----------------

    # Test empty username
    client.post_invalid_form(url, 'Username is required',
            username='', email=email, password=password, retype_password=password)

    # Test short username
    client.post_invalid_form(url, 'Username must be at least 3 characters long',
            username='Ab', email=email, password=password, retype_password=password)

    # Test invalid usernames
    for invalid_username in invalid_usernames:
        client.post_invalid_form(url, 'Username may only contain letters, numbers, ',
                username=invalid_username, email=email, password=password, retype_password=password)

    # Test existing username (case INsensitive!)
    client.post_invalid_form(url, 'This Username is already in use. Please try another one.',
            username='TestUser', email=email, password=password, retype_password=password)

    # Invalid emails
    # --------------

    # Test empty email
    client.post_invalid_form(url, 'Email is required',
            email='', password=password, retype_password=password)

    # Test invalid email
    client.post_invalid_form(url, 'Invalid Email',
            email='user.domain.com', password=password, retype_password=password)

    # Test existing email (case INsensitive!)
    client.post_invalid_form(url, 'This Email is already in use. Please try another one.',
           email='TestUser@Example.Com', password=password, retype_password=password)

    # Invalid passwords
    # -----------------

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            username=username, email=email, password='', retype_password='')

    # Test invalid passwords
    for invalid_password in invalid_passwords:
        client.post_invalid_form(url, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number',
                username=username, email=email, password=invalid_password, retype_password=invalid_password)

    # Test non-matching passwords
    client.post_invalid_form(url, 'Password and Retype Password did not match',
            username=username, email=email, password='Password1', retype_password='Password9')



def test_invalid_login(app, client):
    um =  app.user_manager

    user = utils_prepare_user(app)

    # Set default values
    url = url_for('user.login')
    email = user.email
    username = user.username
    password = 'Password1'

    # Incorrect usernames
    # -------------------
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = False

    # Test empty username
    client.post_invalid_form(url, 'Username is required',
            username='', password=password)

    # Test incorrect username
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = False
    client.post_invalid_form(url, 'Incorrect Username and/or Password',
            username='Xuser1', password=password)
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = True
    client.post_invalid_form(url, 'Username does not exist',
            username='Xuser1', password=password)
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = False

    # Incorrect emails
    # ----------------
    um.USER_ENABLE_USERNAME = False
    um.USER_ENABLE_EMAIL = True

    # Test empty email
    client.post_invalid_form(url, 'Email is required',
            email='', password=password)

    # Test incorrect email
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    client.post_invalid_form(url, 'Incorrect Email and/or Password',
            email='Xuser2@example.com', password=password)
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = True
    client.post_invalid_form(url, 'Email does not exist',
            email='Xuser2@example.com', password=password)
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = False

    # Incorrect passwords
    # -------------------
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True

    # Test empty password
    client.post_invalid_form(url, 'Password is required',
            username=username, password='')

    # Test incorrect password
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = False
    client.post_invalid_form(url, 'Incorrect Username/Email and/or Password',
            username=username, password='XPassword1')
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = True
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = True
    client.post_invalid_form(url, 'Incorrect Password',
            username=username, password='XPassword1')
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    um.USER_SHOW_USERNAME_DOES_NOT_EXIST = False


def test_invalid_misc(app, client):
    um = app.user_manager
    um.USER_ENABLE_USERNAME = True
    um.USER_ENABLE_EMAIL = True

    user = utils_prepare_user(app)
    email = user.email
    username = user.username
    password = 'Password1'

    client.login(username=username, password=password)

    # Test change_username with incorrect password
    url = url_for('user.change_username')
    client.post_invalid_form(url, 'Old Password is incorrect',
            new_username=username, old_password='XPassword1')

    # Test change_password with incorrect password
    url = url_for('user.change_password')
    client.post_invalid_form(url, 'Old Password is incorrect',
            old_password='XXX', new_password=password, retype_password=password)

    # Test forgot password with non-existing email
    url = url_for('user.forgot_password')
    um.USER_SHOW_EMAIL_DOES_NOT_EXIST = True
    client.post_invalid_form(url, 'Email does not exist',
            email='nonexisting@nowhere.org')

    client.logout()



# from __future__ import print_function
#
# from datetime import datetime
# import time
#
# from flask import current_app, url_for
#
# from flask_user.tests.tst_utils import response_has_string
#
#
#
# # **********************
# # ** Global Variables **
# # **********************
# # Using global variable for speed
# user1 = None
# user2 = None
# user3 = None
# user4 = None
#
# # *************
# # ** Defines **
# # *************
#
#
# # *********************
# # ** Automated tests **
# # *********************
# # Function names must start with 'test'
# # The 'client' parameter is set up in conftest.py
#
# def test_init(db):
#     """
#     Set up two test users
#     """
#     global user1, user2, user3, user4
#
#     # Enable all features
#     um =  current_app.user_manager
#     um.USER_ENABLE_REGISTER = True
#     um.USER_ENABLE_CHANGE_USERNAME = True
#     um.USER_ENABLE_CHANGE_PASSWORD = True
#     um.USER_ENABLE_CONFIRM_EMAIL = True
#     um.enable_reset_password = True
#     um.USER_ENABLE_EMAIL = True
#     um.USER_REQUIRE_RETYPE_PASSWORD = True
#
#     # Tests have not been written with auto_login in mind
#     um.auto_login = False
#
#     db_manager = um.db_manager
#     password_hash = um.hash_password('Password1')
#
#     # Create user1 with username and email
#     user1 = db_manager.add_user(username='user1', email='user1@example.com', password=password_hash)
#     assert user1
#
#     # Create user1 with email only
#     user2 = db_manager.add_user(email='user2@example.com', password=password_hash)
#     assert user2
#
#     # Create user3 with username and email
#     user3 = db_manager.add_user(username='user3', email='user3@example.com', password=password_hash)
#     assert user3
#
#     # Create user4 with email only
#     user4 = db_manager.add_user(email='user4@example.com', password=password_hash)
#     assert user4
#
#     um.db_manager.commit()
#
#
# def test_invalid_confirm_email_page(client):
#     print("test_invalid_confirm_email_page")
#
#     # Test Invalid token
#     url = url_for('user.confirm_email', token='InvalidToken')
#     client.get_invalid_page(url, 'Invalid confirmation token')
#
#     # Generate valid token
#     um = current_app.user_manager
#     token = um.generate_token(user1.id)
#     url = url_for('user.confirm_email', token=token)
#
#     # Test Expired token
#     orig_expiration = um.USER_CONFIRM_EMAIL_EXPIRATION    # Save old expiration
#     um.USER_CONFIRM_EMAIL_EXPIRATION = -1                 # Make it expire immediately
#     client.get_invalid_page(url, 'Invalid confirmation token')
#     um.USER_CONFIRM_EMAIL_EXPIRATION = orig_expiration    # Restors old expiration
#
#

# def test_invalid_change_username_form(client):
#     print("test_invalid_change_username_form")
#
#     # Set user manager config
#     um =  current_app.user_manager
#     um.USER_ENABLE_EMAIL = False
#     um.USER_ENABLE_USERNAME = True
#     um.USER_ENABLE_CHANGE_USERNAME = True
#
#     # Set default values
#     username = 'user1'
#     password = 'Password1'
#     new_username = 'user4'
#     url = url_for('user.change_username')
#
#     # Log in as 'user1'
#     client.login(username=username, password=password)
#
#     # Test empty username
#     client.post_invalid_form(url, 'Username is required',
#             new_username='', old_password=password)
#
#     # Test short username
#     client.post_invalid_form(url, 'Username must be at least 3 characters long',
#             new_username=SHORT_USERNAME, old_password=password)
#
#     # Test existing username
#     client.post_invalid_form(url, 'This Username is already in use. Please try another one.',
#             new_username='user3', old_password=password)
#
#     # Test empty password
#     client.post_invalid_form(url, 'Old Password is required',
#             new_username=username, old_password='')
#
#     # Test incorrect password
#     client.post_invalid_form(url, 'Old Password is incorrect',
#             new_username=username, old_password='XPassword1')
#
#     client.logout()
#
# def test_invalid_change_password_form(client):
#     print("test_invalid_change_password_form")
#
#     # Set user manager config
#     um =  current_app.user_manager
#     um.USER_ENABLE_USERNAME = False
#
#     # Set default values
#     email = 'user2@example.com'
#     old_password = 'Password1'
#     new_password = 'Password5'
#     url = url_for('user.change_password')
#
#     # Log in as 'user1'
#     client.login(email=email, password=old_password)
#
#     # Test empty old password
#     client.post_invalid_form(url, 'Old Password is required',
#             old_password='', new_password=new_password, retype_password=new_password)
#
#     # Test incorrect old password
#     client.post_invalid_form(url, 'Old Password is incorrect',
#             old_password='XPassword1', new_password=new_password, retype_password=new_password)
#
#     # Test empty password
#     client.post_invalid_form(url, 'New Password is required',
#             old_password=old_password, new_password='', retype_password=new_password)
#
#     # Test invalid passwords
#     for invalid_password in invalid_passwords:
#         client.post_invalid_form(url, 'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number',
#             old_password=old_password, new_password=invalid_password, retype_password=new_password)
#
#     # Test non-matching passwords
#     client.post_invalid_form(url, 'New Password and Retype Password did not match',
#             old_password=old_password, new_password=new_password, retype_password='Xpassword5')
#
#     client.logout()
#
#
# def test_invalid_forgot_password_form(client):
#     print("test_invalid_forgot_password_form")
#
#     url = url_for('user.forgot_password')
#
#     # Test invalid email
#     client.post_invalid_form(url, 'Invalid Email',
#             email=INVALID_EMAIL)
#
#
# def test_invalid_reset_password(client):
#     print("test_invalid_reset_password")
#
#     # Set user manager config
#     um =  current_app.user_manager
#
#     # Set default values
#     new_password = 'Password5'
#     # Simulate a valid forgot password form
#     token = um.generate_token(user1.id)
#
#     # Test invalid token
#     url = url_for('user.reset_password', token='InvalidToken')
#     client.post_invalid_form(url, 'Your reset password token is invalid',
#             new_password=new_password, retype_password=new_password)
#
#     # Expired Token
#     url = url_for('user.reset_password', token=token)
#     orig_expiration = um.USER_RESET_PASSWORD_EXPIRATION    # Save old expiration
#     um.USER_RESET_PASSWORD_EXPIRATION = -1                 # Make it expire immediately
#     client.post_invalid_form(url, 'Your reset password token is invalid',
#             new_password=new_password, retype_password=new_password)
#     um.USER_RESET_PASSWORD_EXPIRATION = orig_expiration    # Restore old expiration
#
#     # Invalid retype password
#     client.post_invalid_form(url, 'New Password and Retype Password did not match',
#             new_password = new_password, retype_password='XPassword5')
#
# def test_valid_roles(client):
#     um =  current_app.user_manager
#     User = um.db_manager.UserClass
#
#     # Perform only for roles_required_app
#     user007 = um.db_manager.find_user_by_username('user007')
#     if not user007: return
#
#     print("test_valid_roles")
#     um.USER_ENABLE_USERNAME = True
#
#     client.login(username='user007', password='Password1')
#     url = url_for('admin_page')
#     response = client.get_valid_page(url)
#     assert not response_has_string(response, 'You must be signed in to access')
#     client.logout()
#
# def test_invalid_roles(client):
#     um =  current_app.user_manager
#     User = um.db_manager.UserClass
#
#     # Perform only for roles_required_app
#     user007 = um.db_manager.find_user_by_username('user007')
#     if not user007: return
#
#     print("test_invalid_roles")
#     um.USER_ENABLE_USERNAME = True
#
#     client.login(username='user1', password='Password1')
#     url = url_for('admin_page')
#     response = client.get_invalid_page(url, 'You do not have permission to access')
#     client.logout()
#
# def test_login_without_confirm_email(client):
#     print("test_login_without_confirm_email")
#
#     um = current_app.user_manager
#     um.USER_ENABLE_USERNAME = False
#     um.USER_ENABLE_EMAIL = True
#     um.USER_ENABLE_CONFIRM_EMAIL = True
#     um.USER_REQUIRE_RETYPE_PASSWORD = False
#
#     email = 'notconfirmed@example.com'
#     password = 'Password1'
#
#     # register user
#     client.post_valid_form(url_for('user.register'),
#             email=email,
#             password=password)
#
#     # Try logging in without confirming email
#     client.post_invalid_form(url_for('user.login'),
#             'Your email address has not yet been confirmed',
#             email=email,
#             password=password)
#
#     # TODO
#     # # Confirm email manually, but disable account
#     # User = um.db_manager.UserClass
#     # user = User.query.filter(User.email==email).first()
#     # assert(user)
#     # user.active = False
#     # user.email_confirmed_at = datetime.utcnow()
#     #
#     # # Try logging in into  disabled account
#     # client.post_invalid_form(url_for('user.login'),
#     #         'Your account has not been enabled',
#     #         email=email,
#     #         password=password)
#
# def test_cleanup(db):
#     """
#     Delete user1 and user2
#     """
#     global user1, user2, user3, user4
#     um = current_app.user_manager
#     um.db_manager.delete_object(user1)
#     um.db_manager.delete_object(user2)
#     um.db_manager.delete_object(user3)
#     um.db_manager.delete_object(user4)
#     um.db_manager.commit()
#     user1 = None
#     user2 = None
#     user3 = None
#     user4 = None
#
#
# # TODO:
# # Register without confirming email and try to log in
# # 'Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email and follow the instructions to activate your account.'
# #
# # Disable account and try to login
# # 'Your account has been disabled.'
# #
# # Logout with user_manager.logout_next set
# #
# # Reset password with custom user_manager.password_validator
# #
# # Change password with custom user_manager.password_validator:
# #
# # Custom db_adapter.EmailClass