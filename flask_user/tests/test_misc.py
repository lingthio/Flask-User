from .utils import utils_prepare_user

# Make sure that uncovered lines are covered
def test_misc(app):
    um = app.user_manager

    user = utils_prepare_user(app)

    # Generate token with data-item other than int or string
    um.token_manager.generate_token(1.1)

    # Hash password with old API
    um.password_manager.verify_password('password', user)