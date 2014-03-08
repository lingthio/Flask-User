"""
    flask_user.views
    ----------------
    This module contains default Flask-User view functions.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from flask import current_app, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user

from .emails import send_confirmation_email, send_reset_password_email
from . import signals
from .translations import gettext as _

def confirm_email(token):
    """
    Verify email confirmation token and activate the user account.
    """
    # Verify token
    user_manager = current_app.user_manager
    is_valid, has_expired, object_id = user_manager.token_manager.verify_token(
            token,
            user_manager.confirm_email_expiration)

    if has_expired:
        flash(_('Your confirmation token has expired.'), 'error')
        return redirect(user_manager.login_url)

    if not is_valid:
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(user_manager.login_url)

    # Confirm email
    user, email = user_manager.db_adapter.confirm_email(object_id)

    # Send email_confirmed signal
    signals.user_confirmed_email.send(current_app._get_current_object(), user=user, email=email)

    # Prepare one-time system message
    flash(_('Your email has been confirmed. Please sign in.'), 'success')

    return redirect(user_manager.login_url)


@login_required
def change_password():
    """
    Prompt for old password and new password and change the user's password.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.change_password_form(request.form)
    form.next.data = request.args.get('next', '/')  # Place ?next query param in next form field

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Hash password
        hashed_password = user_manager.password_crypt_context.encrypt(form.new_password.data)

        # Change password
        user_manager.db_adapter.set_password(current_user, hashed_password)

        # Send password_changed signal
        signals.user_changed_password.send(current_app._get_current_object(), user=current_user)

        # Prepare one-time system message
        flash(_('Your password has been changed successfully.'), 'success')

        # Redirect to 'next' URL
        return redirect(form.next.data)

    # Process GET or invalid POST
    return render_template(user_manager.change_password_template, form=form)


@login_required
def change_username():
    """
    Prompt for new username and old password and change the user's username.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.change_username_form(request.form)
    form.next.data = request.args.get('next', '/')  # Place ?next query param in next form field

    # Process valid POST
    if request.method=='POST' and form.validate():
        new_username = form.new_username.data

        # Change username
        user_manager.db_adapter.set_username(current_user, new_username)

        # Send username_changed signal
        signals.user_changed_username.send(current_app._get_current_object(), user=current_user)

        # Prepare one-time system message
        flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

        # Redirect to 'next' URL
        return redirect(form.next.data)

    # Process GET or invalid POST
    return render_template(user_manager.change_username_template, form=form)


def forgot_password():
    """
    Prompt for email and send reset password email.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.forgot_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        email = form.email.data

        # Find user by email
        user = user_manager.db_adapter.find_user_by_email(email)
        if user:
            # Generate password reset token
            token = user_manager.token_manager.generate_token(user.id)

            # Store token
            user_manager.db_adapter.set_reset_password_token(user, token)

            # Send confirmation email
            send_reset_password_email(email, user, token)

            # Send reset_password_email_sent signal
            signals.reset_password_email_sent.send(current_app._get_current_object(), user=user)

        # Prepare one-time system message
        flash(_("A reset password email has been sent to '%(email)s'. Open that email and follow the instructions to reset your password.", email=email), 'success')

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.forgot_password_template, form=form)


def login():
    """
    Prompt for username/email and password and sign the user in.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.login_form(request.form)
    form.next.data = request.args.get('next', '/')  # Place ?next query param in next form field

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Retrieve User
        if user_manager.enable_username:
            user = user_manager.db_adapter.find_user_by_username(form.username.data)
        else:
            user = user_manager.db_adapter.find_user_by_email(form.email.data)

        if user:
            if user.active:
                # Use Flask-Login to sign in user
                login_user(user)

                # Send user_logged_in signal
                signals.user_logged_in.send(current_app._get_current_object(), user=user)

                # Prepare one-time system message
                flash(_('You have signed in successfully.'), 'success')

                # Redirect to 'next' URL
                return redirect(form.next.data)
            else:
                if user_manager.enable_confirm_email and not user.email_confirmed_at:
                    flash(_('Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email and follow the instructions to activate your account.'), 'error')
                else:
                    flash(_('Your account has been disabled.'), 'error')


    # Process GET or invalid POST
    return render_template(user_manager.login_template, form=form)


def logout():
    """
    Sign the user out.
    """
    user_manager =  current_app.user_manager

    # Send user_logged_out signal
    signals.user_logged_out.send(current_app._get_current_object(), user=current_user)

    # Use Flask-Login to sign out user
    logout_user()

    # Prepare one-time system message
    flash(_('You have signed out successfully.'), 'success')

    # Redirect to logout_next endpoint or '/'
    next = request.args.get('next', '/')  # Get 'next' query param
    return redirect(next)


def register():
    """
    Prompt for username/email and password, send confirmation email, and create an inactive user account.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():

        # We are about to store user information. The fields to save vary
        # depending on the application config settings.
        # In addition, the email address may be stored in a different
        # table when multiple email addresses are allowed per user.

        # We address these variations by constructing two variable argument dictionaries:
        # - user_kwargs for the User object
        # - email_kwargs for the UserEmail object
        # The UserEmail object may be the same as the User object
        user_kwargs = {}
        if user_manager.db_adapter.EmailClass:
            email_kwargs = {}
        else:
            email_kwargs = user_kwargs

        # Always store hashed password
        user_kwargs['password'] = user_manager.password_crypt_context.encrypt(form.password.data)

        # Store email address depending on config
        if user_manager.enable_email:
            email_address = form.email.data
            email_kwargs['email'] = email_address
        else:
            email_address = None

        # Store username depending on config
        if user_manager.enable_username:
            user_kwargs['username'] = form.username.data

        # If USER_ENABLE_CONFIRM_EMAIL==True: active=False otherwise: active=True
        if user_manager.enable_confirm_email:
            user_kwargs['active'] = False
        else:
            user_kwargs['active'] = True

        # Add User record with named arguments
        user = user_manager.db_adapter.add_user(**user_kwargs)

        # For multiple emails per user, add Email object
        if user_manager.db_adapter.EmailClass:
            raise NotImplementedError()
            # TODO: multiple_emails_per_user
            # email_kwargs['user_id'] = user.id
            # email = user_manager.db_adapter.add_email(**email_kwargs)
            # object_id = email.id
        else:
            object_id = user.id

        # Send user_registered signal
        signals.user_registered.send(current_app._get_current_object(), user=user)

        if user_manager.enable_confirm_email:

            # Generate password reset token
            token = user_manager.token_manager.generate_token(object_id)

            # Send confirmation email
            send_confirmation_email(email_address, user, token)

            # Send confirmation_email_sent signal
            signals.confirmation_email_sent.send(current_app._get_current_object(), user=user)

            # Prepare one-time system message
            flash(_('A confirmation email has been sent to %(email)s. Open that email and follow the instructions to complete your registration.', email=email_address), 'success')

        else:
            # Prepare one-time system message
            flash(_('You have registered successfully. Please sign in.'), 'success')

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.register_template, form=form)


# TODO:
def resend_confirmation_email():
    pass
    # """
    # Prompt for email and re-send the confirmation email.
    # """
    # user_manager =  current_app.user_manager
    #
    # # Initialize form
    # form = user_manager.resend_confirmation_email_form(request.form)
    #
    # # Process valid POST
    # if request.method=='POST' and form.validate():
    #     email = form.email.data
    #
    #     # Find user by email
    #     user = user_manage.db_adapter.find_user_by_email(email)
    #     if user:
    #
    #         # Send confirmation email
    #         send_confirmation_email(email, user)
    #
    #     # Prepare one-time system message
    #     flash(_("A confirmation email has been sent to %(email)s. Open that email and follow the instructions to complete your registration.", email=email), 'success')
    #
    #     # Redirect to 'next' URL or '/'
    #     next = form.next.data
    #     if not next:
    #         return redirect('/')
    #     return redirect(next)
    #
    # # Process GET or invalid POST
    # return render_template(user_manager.resend_confirmation_email_template, form=form)


def reset_password(token):
    """
    Verify the password reset token, Prompt for new password, and set the user's password.
    """
    # Verify token
    user_manager = current_app.user_manager
    is_valid, has_expired, user_id = user_manager.token_manager.verify_token(
            token,
            user_manager.reset_password_expiration)

    if has_expired:
        flash(_('Your reset password token has expired.'), 'error')
        return redirect(user_manager.login_url)

    if not is_valid:
        flash(_('Your reset password token is invalid.'), 'error')
        return redirect(user_manager.login_url)

    user = user_manager.db_adapter.find_user_by_id(user_id)
    if not user or not user_manager.db_adapter.verify_reset_password_token(user, token):
        flash(_('Your reset password token is invalid.'), 'error')
        return redirect(user_manager.login_url)

    # Initialize form
    form = user_manager.reset_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Invalidate the token by clearing the stored token
        user_manager.db_adapter.set_reset_password_token(user, '')

        # Change password
        hashed_password = user_manager.password_crypt_context.encrypt(form.new_password.data)
        user_manager.db_adapter.set_password(user, hashed_password)

        # Prepare one-time system message
        flash(_("Your password has been reset successfully. Please sign in with your new password"), 'success')

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.reset_password_template, form=form)

def unauthenticated():
    """
    Prepare a Flash message and redirect to USER_UNAUTHENTICATED_URL
    """
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_('You must be signed in to access %(url)s.', url=url), 'error')

    # Redirect to USER_UNAUTHENTICATED_URL
    user_manager = current_app.user_manager
    return redirect(user_manager.unauthenticated_url)

def unauthorized():
    """
    Prepare a Flash message and redirect to USER_UNAUTHORIZED_URL
    """
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_('You do not have permission to access %(url)s.', url=url), 'error')

    # Redirect to USER_UNAUTHORIZED_URL
    user_manager = current_app.user_manager
    return redirect(user_manager.unauthorized_url)
