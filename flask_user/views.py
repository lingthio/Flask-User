""" This file contains view functions for Flask-User forms.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from datetime import datetime
from flask import current_app, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_user, logout_user
from .decorators import login_required
from . import emails
from . import signals
from .translations import gettext as _

def confirm_email(token):
    """ Verify email confirmation token and activate the user account."""
    # Verify token
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter
    is_valid, has_expired, object_id = user_manager.verify_token(
            token,
            user_manager.confirm_email_expiration)

    if has_expired:
        flash(_('Your confirmation token has expired.'), 'error')
        return redirect(user_manager.login_url)

    if not is_valid:
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(user_manager.login_url)

    # Confirm email by setting User.active=True and User.confirmed_at=utcnow()
    if db_adapter.UserEmailClass:
        user_email = user_manager.find_user_email_by_id(object_id)
        if user_email:
            user_email.confirmed_at = datetime.utcnow()
            user = user_email.user
        else:
            user = None
    else:
        user_email = None
        user = user_manager.find_user_by_id(object_id)
        user.confirmed_at = datetime.utcnow()

    if user:
        user.active = True
        db_adapter.commit()
    else:                                               # pragma: no cover
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(user_manager.login_url)

    # Send email_confirmed signal
    signals.user_confirmed_email.send(current_app._get_current_object(), user=user)

    # Prepare one-time system message
    flash(_('Your email has been confirmed. Please sign in.'), 'success')

    # Retrieve 'next' query parameter
    next = request.args.get('next', '/')

    # Redirect to the login page with the specified 'next' query parameter
    return redirect(user_manager.login_url+'?next='+next)


@login_required
def change_password():
    """ Prompt for old password and new password and change the user's password."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.change_password_form(request.form)
    form.next.data = request.args.get('next', '/')  # Place ?next query param in next form field

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Hash password
        hashed_password = user_manager.hash_password(form.new_password.data)

        # Change password
        db_adapter.update_object(current_user, password=hashed_password)
        db_adapter.commit()

        # Send 'password_changed' email
        if user_manager.enable_email and user_manager.send_password_changed_email:
            emails.send_password_changed_email(current_user)

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
    """ Prompt for new username and old password and change the user's username."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.change_username_form(request.form)
    form.next.data = request.args.get('next', '/')  # Place ?next query param in next form field

    # Process valid POST
    if request.method=='POST' and form.validate():
        new_username = form.new_username.data

        # Change username
        db_adapter.update_object(current_user, username=new_username)
        db_adapter.commit()

        # Send 'username_changed' email
        if user_manager.enable_email and user_manager.send_username_changed_email:
            emails.send_username_changed_email(current_user)

        # Send username_changed signal
        signals.user_changed_username.send(current_app._get_current_object(), user=current_user)

        # Prepare one-time system message
        flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

        # Redirect to 'next' URL
        return redirect(form.next.data)

    # Process GET or invalid POST
    return render_template(user_manager.change_username_template, form=form)

@login_required
def email_action(id, action):
    """ Perform action 'action' on UserEmail object 'id'
    """
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Retrieve UserEmail by id
    user_email = db_adapter.find_object(db_adapter.UserEmailClass, id=id)

    # Users may only change their own UserEmails
    if not user_email or user_email.user_id != current_user.id:
        return unauthorized()

    if action=='delete':
        # Primary UserEmail can not be deleted
        if user_email.is_primary:
            return unauthorized()
        # Delete UserEmail
        db_adapter.delete_object(user_email)
        db_adapter.commit()

    elif action=='make-primary':
        # Disable previously primary emails
        user_emails = db_adapter.find_object_list(db_adapter.UserEmailClass, user_id=current_user.id)
        for ue in user_emails:
            if ue.is_primary:
                ue.is_primary = False
        # Enable current primary email
        user_email.is_primary = True
        # Commit
        db_adapter.commit()

    elif action=='confirm':
        send_confirm_email_or_registered_email(user_email.user, user_email)

    else:
        return unauthorized()

    return redirect(url_for('user.manage_emails'))

def forgot_password():
    """Prompt for email and send reset password email."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.forgot_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        email = form.email.data

        # Find user by email
        user, user_email = user_manager.find_user_by_email(email)
        if user:
            # Generate reset password link
            token = user_manager.generate_token(user.id)
            reset_password_link = url_for('user.reset_password', token=token, _external=True)

            # Send forgot password email
            emails.send_forgot_password_email(user, user_email, reset_password_link)

            # Store token
            if hasattr(user, 'reset_password_token'):
                db_adapter.update_object(user, reset_password_token=token)
                db_adapter.commit()

            # Send forgot_password signal
            signals.user_forgot_password.send(current_app._get_current_object(), user=user)

        # Prepare one-time system message
        flash(_("A reset password email has been sent to '%(email)s'. Open that email and follow the instructions to reset your password.", email=email), 'success')

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.forgot_password_template, form=form)


def login():
    """ Prompt for username/email and password and sign the user in."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    next = request.args.get('next', '/')                  # Get the ?next=... query param

    # Immediately redirect already logged in users
    if user_manager.auto_login:
        if current_user.is_authenticated():
            return redirect(next)

    # Initialize form
    login_form = user_manager.login_form(request.form)
    login_form.next.data = next                           # set hidden form field 'next'
    register_form = user_manager.register_form()          # for login_or_register.html

    # Process valid POST
    if request.method=='POST' and login_form.validate():
        # Retrieve User
        user_email = None
        if user_manager.enable_username:
            # Find user by username or email address
            user = user_manager.find_user_by_username(login_form.username.data)
            user_email = None
            if user and db_adapter.UserEmailClass:
                user_email = db_adapter.find_object(db_adapter.UserEmailClass,
                        user_id=user.id,
                        is_primary=True,
                        )
            if not user and user_manager.enable_email:
                user, user_email = user_manager.find_user_by_email(login_form.username.data)
        else:
            # Find user by email address
            user, user_email = user_manager.find_user_by_email(login_form.email.data)

        if user:
            if user.active:
                # Use Flask-Login to sign in user
                login_user(user)

                # Send user_logged_in signal
                signals.user_logged_in.send(current_app._get_current_object(), user=user)

                # Prepare one-time system message
                flash(_('You have signed in successfully.'), 'success')

                # Redirect to 'next' URL
                return redirect(login_form.next.data)
            else:
                confirmed_at = user_email.confirmed_at if db_adapter.UserEmailClass else user.confirmed_at
                if user_manager.enable_confirm_email and not confirmed_at:
                    flash(_('Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email or <a href="'+url_for('user.resend_confirm_email')+'">Re-send confirmation email</a>.'), 'error')
                else:
                    flash(_('Your account has been disabled.'), 'error')

    # Process GET or invalid POST
    return render_template(user_manager.login_template,
            form=login_form,
            login_form=login_form,
            register_form=register_form)

def logout():
    """ Sign the user out."""
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


@login_required
def manage_emails():
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    user_emails = db_adapter.find_object_list(db_adapter.UserEmailClass, user_id=current_user.id)
    form = user_manager.add_email_form()

    # Process valid POST request
    if request.method=="POST" and form.validate():
        user_emails = db_adapter.add_object(db_adapter.UserEmailClass,
                user_id=current_user.id,
                email=form.email.data)
        db_adapter.commit()
        return redirect(url_for('user.manage_emails'))

    # Process GET or invalid POST request
    return render_template(user_manager.manage_emails_template,
            user_emails=user_emails,
            form=form,
            )

def register():
    """ Display registration form and create new User."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    register_form = user_manager.register_form(request.form)
    login_form = user_manager.login_form()          # for login_or_register.html

    # Process valid POST
    if request.method=='POST' and register_form.validate():

        # Create a User object using Form fields that have a corresponding User field
        User = user_manager.db_adapter.UserClass
        user_class_fields = User.__dict__
        user_fields = {}

        # Create a UserEmail object using Form fields that have a corresponding UserEmail field
        if user_manager.db_adapter.UserEmailClass:
            UserEmail = user_manager.db_adapter.UserEmailClass
            user_email_class_fields = UserEmail.__dict__
            user_email_fields = {}

        # Create a UserProfile object using Form fields that have a corresponding UserProfile field
        if user_manager.db_adapter.UserProfileClass:
            UserProfile = user_manager.db_adapter.UserProfileClass
            user_profile_class_fields = UserProfile.__dict__
            user_profile_fields = {}

        # User.active is True if not USER_ENABLE_CONFIRM_EMAIL and False otherwise
        user_fields['active'] = not user_manager.enable_confirm_email

        # For all form fields
        for field_name, field_value in register_form.data.items():
            # Hash password field
            if field_name=='password':
                user_fields['password'] = user_manager.hash_password(register_form.password.data)
            # Store corresponding Form fields into the User object and/or UserProfile object
            else:
                if field_name in user_class_fields:
                    user_fields[field_name] = field_value
                if user_manager.db_adapter.UserEmailClass:
                    if field_name in user_email_class_fields:
                        user_email_fields[field_name] = field_value
                if user_manager.db_adapter.UserProfileClass:
                    if field_name in user_profile_class_fields:
                        user_profile_fields[field_name] = field_value

        # Add User record using named arguments 'user_fields'
        user = db_adapter.add_object(User, **user_fields)

        # Add UserEmail record using named arguments 'user_email_fields'
        if user_manager.db_adapter.UserEmailClass:
            user_email = db_adapter.add_object(UserEmail,
                    user=user,
                    is_primary=True,
                    **user_email_fields)
        else:
            user_email = None

        # Add UserProfile record using named arguments 'user_profile_fields'
        if user_manager.db_adapter.UserProfileClass:
            user.user_profile = db_adapter.add_object(UserProfile, **user_profile_fields)

        db_adapter.commit()

        send_confirm_email_or_registered_email(user, user_email)

        # Send user_registered signal
        signals.user_registered.send(current_app._get_current_object(), user=user)

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.register_template,
            form=register_form,
            login_form=login_form,
            register_form=register_form)

def resend_confirm_email():
    """Prompt for email and re-send email conformation email."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.resend_confirm_email_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        email = form.email.data

        # Find user by email
        user, user_email = user_manager.find_user_by_email(email)
        if user:
            send_confirm_email_or_registered_email(user, user_email)

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.resend_confirm_email_template, form=form)


def reset_password(token):
    """ Verify the password reset token, Prompt for new password, and set the user's password."""
    # Verify token
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    is_valid, has_expired, user_id = user_manager.verify_token(
            token,
            user_manager.reset_password_expiration)

    if has_expired:
        flash(_('Your reset password token has expired.'), 'error')
        return redirect(user_manager.login_url)

    if not is_valid:
        flash(_('Your reset password token is invalid.'), 'error')
        return redirect(user_manager.login_url)

    user = user_manager.find_user_by_id(user_id)
    if user:
        # Avoid re-using old tokens
        if hasattr(user, 'reset_password_token'):
            verified = user.reset_password_token == token
        else:
            verified = True
    if not user or not verified:
        flash(_('Your reset password token is invalid.'), 'error')
        return redirect(user_manager.login_url)

    # Initialize form
    form = user_manager.reset_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Invalidate the token by clearing the stored token
        if hasattr(user, 'reset_password_token'):
            db_adapter.update_object(user, reset_password_token='')

        # Change password
        hashed_password = user_manager.hash_password(form.new_password.data)
        db_adapter.update_object(user, password=hashed_password)
        db_adapter.commit()

        # Send 'password_changed' email
        if user_manager.enable_email and user_manager.send_password_changed_email:
            emails.send_password_changed_email(user)

        # Prepare one-time system message
        flash(_("Your password has been reset successfully. Please sign in with your new password"), 'success')

        # Redirect to the login page
        return redirect(url_for('user.login'))

    # Process GET or invalid POST
    return render_template(user_manager.reset_password_template, form=form)

def _get_email_address(user):
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter
    if db_adapter.UserEmailClass:
        user_email = db_adapter.find_object(db_adapter.UserEmailClass,
                user_id=user.id,
                is_primary=True,
                )
        return user_email.email if user_email else None
    else:
        return user.email

def send_confirm_email_or_registered_email(user, user_email):
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Send 'confirm_email' or 'registered' email
    if user_manager.enable_email:
        email_address = user_email.email if user_email else user.email

        try:
            if user_manager.enable_confirm_email:
                # Send 'confirm_email' email

                # Generate confirm email link
                object_id = user_email.id if user_email else user.id
                token = user_manager.generate_token(object_id)
                confirm_email_link = url_for('user.confirm_email', token=token, _external=True)

                # Send email
                emails.send_confirm_email_email(user, user_email, confirm_email_link)
            else:
                if user_manager.send_registered_email:
                    # Send 'registered' email
                    emails.send_registered_email(user, user_email)

        except Exception as e:
            # delete newly registered user if send email fails
            db_adapter.delete_object(user)
            db_adapter.commit()
            raise e

    # Prepare one-time system message
    if user_manager.enable_confirm_email:
        flash(_('A confirmation email has been sent to %(email)s with instructions to complete your registration.', email=email_address), 'success')
    else:
        flash(_('You have registered successfully. Please sign in.'), 'success')


def unauthenticated():
    """ Prepare a Flash message and redirect to USER_UNAUTHENTICATED_URL"""
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_("You must be signed in to access '%(url)s'.", url=url), 'error')

    # Redirect to USER_UNAUTHENTICATED_URL
    user_manager = current_app.user_manager
    return redirect(user_manager.unauthenticated_url+'?next='+url)

def unauthorized():
    """ Prepare a Flash message and redirect to USER_UNAUTHORIZED_URL"""
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_("You do not have permission to access '%(url)s'.", url=url), 'error')

    # Redirect to USER_UNAUTHORIZED_URL
    user_manager = current_app.user_manager
    return redirect(user_manager.unauthorized_url)
