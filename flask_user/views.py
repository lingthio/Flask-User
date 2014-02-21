from itsdangerous import SignatureExpired

from flask import current_app, flash, redirect, render_template, request, url_for
from flask.ext.babel import gettext as _
from flask.ext.login import current_user, login_required, login_user, logout_user

from flask_user.email_manager import send_confirmation_email

def confirm_email(token):
    """
    Verify email confirmation token and activate the user account.
    """
    # Verify token
    user_manager =  current_app.user_manager
    is_valid, has_expired, user_id = user_manager.token_manager.verify_token(token, max_age=1000)

    if has_expired:
        flash(_('Your confirmation token has expired.'), 'error')
        return redirect(user_manager.login_url)

    if not is_valid:
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(user_manager.login_url)

    user_manager.db_adapter.confirm_user(user_id)
    flash(_('Your email has been confirmed.'), 'success')

    return redirect(user_manager.login_url)


@login_required
def change_password():
    """
    Prompt for old password and new password and change the user's password.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.change_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Hash password
        hashed_password = user_manager.password_crypt_context.encrypt(form.new_password.data)

        # Change password
        user_manager.db_adapter.set_password(current_user, hashed_password)

        # Prepare one-time system message
        flash(_('Your password has been changed successfully.'), 'success')

        # Redirect to 'next' URL or '/'
        next = form.next.data
        if not next:
            return redirect('/')
        return redirect(next)

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

    # Process valid POST
    if request.method=='POST' and form.validate():
        new_username = form.new_username.data

        # Change username
        user_manager.db_adapter.set_username(current_user, new_username)

        # Prepare one-time system message
        flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

        # Redirect to 'next' URL or '/'
        next = form.next.data
        if not next:
            return redirect('/')
        return redirect(next)

    # Process GET or invalid POST
    return render_template(user_manager.change_username_template, form=form)


# TODO:
def forgot_password():
    pass


def login():
    """
    Prompt for username/email and password and sign the user in.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.login_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Retrieve User
        if user_manager.login_with_username:
            user = user_manager.db_adapter.find_user_by_username(form.username.data)
        else:
            user = user_manager.db_adapter.find_user_by_email(form.email.data)

        if user:
            if user.active:
                # Use Flask-Login to sign in user
                login_user(user)

                # Prepare one-time system message
                flash(_('You have signed in successfully.'), 'success')

                # Redirect to 'next' URL or '/'
                next = form.next.data
                if not next:
                    return redirect('/')
                return redirect(next)
            else:
                if not user.email_confirmed_at:
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

    # Use Flask-Login to sign out user
    logout_user()

    # Prepare one-time system message
    flash(_('You have signed out successfully.'), 'success')

    # Redirect to logout_next endpoint or '/'
    if user_manager.logout_next:
        return redirect(url_for(user_manager.logout_next))
    else:
        return redirect('/')


def register():
    """
    Prompt for username/email and password, send confirmation email, and create an inactive user account.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Encrypt password
        email = None
        hashed_password = user_manager.password_crypt_context.encrypt(form.password.data)

        # Construct named arguments (**kwargs)
        kwargs = {}
        # Always set password
        kwargs['password']=hashed_password
        # Set username if USER_LOGIN_WITH_USERNAME is True
        if user_manager.login_with_username:
            kwargs['username'] = form.username.data
        # Set username if USER_REGISTER_WITH_USER_NAME is True or USER_LOGIN_WITH_USERNAME is False
        if user_manager.register_with_email or not user_manager.login_with_username:
            email = form.email.data
            kwargs['email'] = email
        # Set active=False if USER_REQUIRE_EMAIL_CONFIRMATION is True
        if user_manager.require_email_confirmation:
            kwargs['active'] = False
        else:
            kwargs['active'] = True

        # Add User record with named arguments (**kwargs)
        user = user_manager.db_adapter.add_user(**kwargs)

        if email:
            # Prepare one-time system message
            flash(_("A confirmation email has been sent to %(email)s. Open this email and follow the instructions to activate your account.", email=email), 'success')
            # Send confirmation email
            send_confirmation_email(email, user)

        return redirect(user_manager.login_url)

    # Process GET or invalid POST
    return render_template(user_manager.register_template, form=form)


# TODO:
def resend_confirmation_email():
    """
    Prompt for email and re-send the confirmation email.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Encrypt password
        email = None
        hashed_password = user_manager.password_crypt_context.encrypt(form.password.data)

        # Construct named arguments (**kwargs)
        kwargs = {}
        # Always set password
        kwargs['password']=hashed_password
        # Set username if USER_LOGIN_WITH_USERNAME is True
        if user_manager.login_with_username:
            kwargs['username'] = form.username.data
        # Set username if USER_REGISTER_WITH_USER_NAME is True or USER_LOGIN_WITH_USERNAME is False
        if user_manager.register_with_email or not user_manager.login_with_username:
            email = form.email.data
            kwargs['email'] = email
        # Set active=False if USER_REQUIRE_EMAIL_CONFIRMATION is True
        if user_manager.require_email_confirmation:
            kwargs['active'] = False
        else:
            kwargs['active'] = True

        # Add User record with named arguments (**kwargs)
        user = user_manager.db_adapter.add_user(**kwargs)

        if email:
            # Prepare one-time system message
            flash(_("A confirmation email has been sent to %(email)s. Open this email and follow the instructions to activate your account.", email=email), 'success')
            # Send confirmation email
            send_confirmation_email(email, user)

        return redirect(user_manager.login_url)

    # Process GET or invalid POST
    return render_template(user_manager.resend_confirmation_email_template, form=form)


# TODO:
def reset_password():
    """
    Verify the password reset token, Prompt for new password, and set the user's password.
    """
    user_manager =  current_app.user_manager

    # Initialize form
    form = user_manager.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Encrypt password
        email = None
        hashed_password = user_manager.password_crypt_context.encrypt(form.password.data)

        # Construct named arguments (**kwargs)
        kwargs = {}
        # Always set password
        kwargs['password']=hashed_password
        # Set username if USER_LOGIN_WITH_USERNAME is True
        if user_manager.login_with_username:
            kwargs['username'] = form.username.data
        # Set username if USER_REGISTER_WITH_USER_NAME is True or USER_LOGIN_WITH_USERNAME is False
        if user_manager.register_with_email or not user_manager.login_with_username:
            email = form.email.data
            kwargs['email'] = email
        # Set active=False if USER_REQUIRE_EMAIL_CONFIRMATION is True
        if user_manager.require_email_confirmation:
            kwargs['active'] = False
        else:
            kwargs['active'] = True

        # Add User record with named arguments (**kwargs)
        user = user_manager.db_adapter.add_user(**kwargs)

        if email:
            # Prepare one-time system message
            flash(_("A confirmation email has been sent to %(email)s. Open this email and follow the instructions to activate your account.", email=email), 'success')
            # Send confirmation email
            send_confirmation_email(email, user)

        return redirect(user_manager.login_url)

    # Process GET or invalid POST
    return render_template(user_manager.reset_password_template, form=form)

