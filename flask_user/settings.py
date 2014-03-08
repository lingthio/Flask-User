def set_default_settings(user_manager, app_config):
    """
    Set default app.config settings, but only if they have not been set before
    """
    # define short names
    um = user_manager
    sd = app_config.setdefault

    # Retrieve obsoleted settings
    # These plural settings have been replaced by singular settings
    obsoleted_enable_emails            = sd('USER_ENABLE_EMAILS',              True)
    obsoleted_enable_retype_passwords  = sd('USER_ENABLE_RETYPE_PASSWORDS',    False)
    obsoleted_enable_usernames         = sd('USER_ENABLE_USERNAMES',           False)

    # Set default features
    um.enable_change_password   = sd('USER_ENABLE_CHANGE_PASSWORD',     True)
    um.enable_change_username   = sd('USER_ENABLE_CHANGE_USERNAME',     False)
    um.enable_confirm_email     = sd('USER_ENABLE_CONFIRM_EMAIL',       False)
    um.enable_email             = sd('USER_ENABLE_EMAIL',               obsoleted_enable_emails)
    um.enable_forgot_password   = sd('USER_ENABLE_FORGOT_PASSWORD',     False)
    um.enable_register          = sd('USER_ENABLE_REGISTRATION',        True)
    um.enable_require_invitation= sd('USER_ENABLE_REQUIRE_INVITATION',  False)
    um.enable_retype_password   = sd('USER_ENABLE_RETYPE_PASSWORD',     obsoleted_enable_retype_passwords)
    um.enable_username          = sd('USER_ENABLE_USERNAME',            obsoleted_enable_usernames)
    um.enable_multiple_emails   = sd('USER_ENABLE_MULTIPLE_EMAILS',     False)

    # Set default settings
    um.confirm_email_expiration = sd('USER_CONFIRM_EMAIL_EXPIRATION',   2*24*3600) # 2 days
    um.reset_password_expiration= sd('USER_RESET_PASSWORD_EXPIRATION',  2*24*3600) # 2 days

    # Set default URLs
    um.change_password_url      = sd('USER_CHANGE_PASSWORD_URL',        '/user/change-password')
    um.change_username_url      = sd('USER_CHANGE_USERNAME_URL',        '/user/change-username')
    um.confirm_email_url        = sd('USER_CONFIRM_EMAIL_URL',          '/user/confirm-email/<token>')
    um.forgot_password_url      = sd('USER_FORGOT_PASSWORD_URL',        '/user/forgot-password')
    um.login_url                = sd('USER_LOGIN_URL',                  '/user/sign-in')
    um.logout_url               = sd('USER_LOGOUT_URL',                 '/user/sign-out')
    um.register_url             = sd('USER_REGISTER_URL',               '/user/register')
    um.resend_confirmation_email_url = sd('USER_RESEND_CONFIRMATION_EMAIL_URL', '/user/resend-confirmation-email')
    um.reset_password_url       = sd('USER_RESET_PASSWORD_URL',         '/user/reset-password/<token>')
    um.unauthenticated_url      = sd('USER_UNAUTHENTICATED_URL',        um.login_url)
    um.unauthorized_url         = sd('USER_UNAUTHORIZED_URL',           '/')

    # Set default template files
    um.change_password_template = sd('USER_CHANGE_PASSWORD_TEMPLATE',  'flask_user/change_password.html')
    um.change_username_template = sd('USER_CHANGE_USERNAME_TEMPLATE',  'flask_user/change_username.html')
    um.forgot_password_template = sd('USER_FORGOT_PASSWORD_TEMPLATE',  'flask_user/forgot_password.html')
    um.login_template           = sd('USER_LOGIN_TEMPLATE',            'flask_user/login.html')
    um.register_template        = sd('USER_REGISTER_TEMPLATE',         'flask_user/register.html')
    um.resend_confirmation_email_template = sd('USER_RESEND_CONFIRMATION_EMAIL_TEMPLATE', 'flask_user/resend_confirmation_email.html')
    um.reset_password_template  = sd('USER_RESET_PASSWORD_TEMPLATE',    'flask_user/reset_password.html')

def check_settings(user_manager):
    """
    Verify config combinations. Produce a helpful error messages for inconsistent combinations.
    """
    # Define custom Exception
    class ConfigurationError(Exception):
        pass

    # define short names
    um = user_manager

    # USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.
    if um.enable_register and not(um.enable_username or um.enable_email):
        raise ConfigurationError('USER_ENABLE_REGISTER=True must have USER_ENABLE_USERNAME=True or USER_ENABLE_EMAIL=True or both.')

    # USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True
    if um.enable_confirm_email and not um.enable_email:
        raise ConfigurationError('USER_ENABLE_CONFIRM_EMAIL=True must have USER_ENABLE_EMAIL=True.')

    # USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True
    if um.enable_multiple_emails and not um.enable_email:
        raise ConfigurationError('USER_ENABLE_MULTIPLE_EMAILS=True must have USER_ENABLE_EMAIL=True.')

    # ENABLE_CHANGE_USERNAME=True must have ENABLE_USERNAME=True.
    if um.enable_change_username and not um.enable_username:
        raise ConfigurationError('ENABLE_CHANGE_USERNAME=True must have ENABLE_USERNAME=True.')

