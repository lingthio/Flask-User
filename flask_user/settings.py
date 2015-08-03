""" This file handles default application config settings for Flask-User.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

def set_default_settings(user_manager, app_config):
    """ Set default app.config settings, but only if they have not been set before """
    # define short names
    um = user_manager
    sd = app_config.setdefault

    # Retrieve obsoleted settings
    # These plural settings have been replaced by singular settings
    obsoleted_enable_emails            = sd('USER_ENABLE_EMAILS',              True)
    obsoleted_enable_retype_passwords  = sd('USER_ENABLE_RETYPE_PASSWORDS',    True)
    obsoleted_enable_usernames         = sd('USER_ENABLE_USERNAMES',           True)
    obsoleted_enable_registration      = sd('USER_ENABLE_REGISTRATION',        True)

    # General settings
    um.app_name                     = sd('USER_APP_NAME', 'AppName')

    # Set default features
    um.enable_change_password       = sd('USER_ENABLE_CHANGE_PASSWORD',       True)
    um.enable_change_username       = sd('USER_ENABLE_CHANGE_USERNAME',       True)
    um.enable_email                 = sd('USER_ENABLE_EMAIL',                 obsoleted_enable_emails)
    um.enable_confirm_email         = sd('USER_ENABLE_CONFIRM_EMAIL',         um.enable_email)
    um.enable_forgot_password       = sd('USER_ENABLE_FORGOT_PASSWORD',       um.enable_email)
    um.enable_login_without_confirm_email = sd('USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL', False)
    um.enable_multiple_emails       = sd('USER_ENABLE_MULTIPLE_EMAILS',       False)
    um.enable_register              = sd('USER_ENABLE_REGISTER',              obsoleted_enable_registration)
    um.enable_remember_me           = sd('USER_ENABLE_REMEMBER_ME',           True)
    um.enable_retype_password       = sd('USER_ENABLE_RETYPE_PASSWORD',       obsoleted_enable_retype_passwords)
    um.enable_username              = sd('USER_ENABLE_USERNAME',              obsoleted_enable_usernames)

    # Set default settings
    um.auto_login                  = sd('USER_AUTO_LOGIN',                 True)
    um.auto_login_after_confirm    = sd('USER_AUTO_LOGIN_AFTER_CONFIRM',   um.auto_login)
    um.auto_login_after_register   = sd('USER_AUTO_LOGIN_AFTER_REGISTER',  um.auto_login)
    um.auto_login_after_reset_password   = sd('USER_AUTO_LOGIN_AFTER_RESET_PASSWORD',  um.auto_login)
    um.auto_login_at_login         = sd('USER_AUTO_LOGIN_AT_LOGIN',        um.auto_login)
    um.confirm_email_expiration    = sd('USER_CONFIRM_EMAIL_EXPIRATION',   2*24*3600)   # 2 days
    um.invite_expiration           = sd('USER_INVITE_EXPIRATION',          90*24*3600)  # 90 days
    um.password_hash_mode          = sd('USER_PASSWORD_HASH_MODE',         'passlib')
    um.password_hash               = sd('USER_PASSWORD_HASH',              'bcrypt')
    um.password_salt               = sd('USER_PASSWORD_SALT',              app_config['SECRET_KEY'])
    um.reset_password_expiration   = sd('USER_RESET_PASSWORD_EXPIRATION',  2*24*3600)   # 2 days
    um.enable_invitation           = sd('USER_ENABLE_INVITATION',          False)
    um.require_invitation          = sd('USER_REQUIRE_INVITATION',         False)
    um.send_password_changed_email = sd('USER_SEND_PASSWORD_CHANGED_EMAIL',um.enable_email)
    um.send_registered_email       = sd('USER_SEND_REGISTERED_EMAIL',      um.enable_email)
    um.send_username_changed_email = sd('USER_SEND_USERNAME_CHANGED_EMAIL',um.enable_email)
    um.show_username_email_does_not_exist = sd('USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST', um.enable_register)

    # Set default URLs
    um.change_password_url       = sd('USER_CHANGE_PASSWORD_URL',        '/user/change-password')
    um.change_username_url       = sd('USER_CHANGE_USERNAME_URL',        '/user/change-username')
    um.confirm_email_url         = sd('USER_CONFIRM_EMAIL_URL',          '/user/confirm-email/<token>')
    um.email_action_url          = sd('USER_EMAIL_ACTION_URL',           '/user/email/<id>/<action>')
    um.forgot_password_url       = sd('USER_FORGOT_PASSWORD_URL',        '/user/forgot-password')
    um.login_url                 = sd('USER_LOGIN_URL',                  '/user/sign-in')
    um.logout_url                = sd('USER_LOGOUT_URL',                 '/user/sign-out')
    um.manage_emails_url         = sd('USER_MANAGE_EMAILS_URL',          '/user/manage-emails')
    um.register_url              = sd('USER_REGISTER_URL',               '/user/register')
    um.resend_confirm_email_url  = sd('USER_RESEND_CONFIRM_EMAIL_URL',   '/user/resend-confirm-email')
    um.reset_password_url        = sd('USER_RESET_PASSWORD_URL',         '/user/reset-password/<token>')
    um.user_profile_url          = sd('USER_PROFILE_URL',                '/user/profile')
    um.invite_url                = sd('USER_INVITE_URL',                 '/user/invite')

    # Set default ENDPOINTs
    home_endpoint = ''
    login_endpoint = um.login_endpoint = 'user.login'
    um.after_change_password_endpoint      = sd('USER_AFTER_CHANGE_PASSWORD_ENDPOINT',      home_endpoint)
    um.after_change_username_endpoint      = sd('USER_AFTER_CHANGE_USERNAME_ENDPOINT',      home_endpoint)
    um.after_confirm_endpoint              = sd('USER_AFTER_CONFIRM_ENDPOINT',              home_endpoint)
    um.after_forgot_password_endpoint      = sd('USER_AFTER_FORGOT_PASSWORD_ENDPOINT',      home_endpoint)
    um.after_login_endpoint                = sd('USER_AFTER_LOGIN_ENDPOINT',                home_endpoint)
    um.after_logout_endpoint               = sd('USER_AFTER_LOGOUT_ENDPOINT',               login_endpoint)
    um.after_register_endpoint             = sd('USER_AFTER_REGISTER_ENDPOINT',             home_endpoint)
    um.after_resend_confirm_email_endpoint = sd('USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT', home_endpoint)
    um.after_reset_password_endpoint       = sd('USER_AFTER_RESET_PASSWORD_ENDPOINT',       home_endpoint)
    um.after_invite_endpoint               = sd('USER_INVITE_ENDPOINT',                     home_endpoint)
    um.unconfirmed_email_endpoint          = sd('USER_UNCONFIRMED_EMAIL_ENDPOINT',          home_endpoint)
    um.unauthenticated_endpoint            = sd('USER_UNAUTHENTICATED_ENDPOINT',            login_endpoint)
    um.unauthorized_endpoint               = sd('USER_UNAUTHORIZED_ENDPOINT',               home_endpoint)

    # Set default template files
    um.change_password_template      = sd('USER_CHANGE_PASSWORD_TEMPLATE',  'flask_user/change_password.html')
    um.change_username_template      = sd('USER_CHANGE_USERNAME_TEMPLATE',  'flask_user/change_username.html')
    um.forgot_password_template      = sd('USER_FORGOT_PASSWORD_TEMPLATE',  'flask_user/forgot_password.html')
    um.login_template                = sd('USER_LOGIN_TEMPLATE',            'flask_user/login.html')
    um.manage_emails_template        = sd('USER_MANAGE_EMAILS_TEMPLATE',    'flask_user/manage_emails.html')
    um.register_template             = sd('USER_REGISTER_TEMPLATE',         'flask_user/register.html')
    um.resend_confirm_email_template = sd('USER_RESEND_CONFIRM_EMAIL_TEMPLATE', 'flask_user/resend_confirm_email.html')
    um.reset_password_template       = sd('USER_RESET_PASSWORD_TEMPLATE',   'flask_user/reset_password.html')
    um.user_profile_template         = sd('USER_PROFILE_TEMPLATE',          'flask_user/user_profile.html')
    um.invite_template               = sd('USER_INVITE_TEMPLATE',           'flask_user/invite.html')
    um.invite_accept_template        = sd('USER_INVITE_ACCEPT_TEMPLATE',    'flask_user/register.html')

    # Set default email template files
    um.confirm_email_email_template    = sd('USER_CONFIRM_EMAIL_EMAIL_TEMPLATE',    'flask_user/emails/confirm_email')
    um.forgot_password_email_template  = sd('USER_FORGOT_PASSWORD_EMAIL_TEMPLATE',  'flask_user/emails/forgot_password')
    um.password_changed_email_template = sd('USER_PASSWORD_CHANGED_EMAIL_TEMPLATE', 'flask_user/emails/password_changed')
    um.registered_email_template       = sd('USER_REGISTERED_EMAIL_TEMPLATE',       'flask_user/emails/registered')
    um.username_changed_email_template = sd('USER_USERNAME_CHANGED_EMAIL_TEMPLATE', 'flask_user/emails/username_changed')
    um.invite_email_template           = sd('USER_INVITE_EMAIL_TEMPLATE',           'flask_user/emails/invite')


def check_settings(user_manager):
    """ Verify config combinations. Produce a helpful error messages for inconsistent combinations."""
    # Define custom Exception
    class ConfigurationError(Exception):
        pass
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
    # USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.
    if um.enable_change_username and not um.enable_username:
        raise ConfigurationError('USER_ENABLE_CHANGE_USERNAME=True must have USER_ENABLE_USERNAME=True.')
    # USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True
    if um.send_registered_email and not um.enable_email:
        raise ConfigurationError('USER_SEND_REGISTERED_EMAIL=True must have USER_ENABLE_EMAIL=True.')
    if um.require_invitation and not um.enable_invitation:
        raise ConfigurationError('USER_REQUIRE_INVITATION=True must have USER_ENABLE_INVITATION=True.')
    if um.enable_invitation and not um.db_adapter.UserInvitationClass:
        raise ConfigurationError('USER_ENABLE_INVITATION=True must pass UserInvitationClass to SQLAlchemyAdapter().')
