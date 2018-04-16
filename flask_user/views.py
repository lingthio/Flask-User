""" This file contains view functions for Flask-User forms.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

from datetime import datetime
from flask import current_app, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from .decorators import confirm_email_required, login_required
from . import emails
from . import signals
from .translations import gettext as _

# Python version specific imports
from sys import version_info as py_version
is_py2 = (py_version[0] == 2)     #: Python 2.x?
is_py3 = (py_version[0] == 3)     #: Python 3.x?
if is_py2:
    from urlparse import urlsplit, urlunsplit
    from urllib import quote, unquote
if is_py3:
    from urllib.parse import urlsplit, urlunsplit
    from urllib.parse import quote, unquote


def _call_or_get(function_or_property):
    return function_or_property() if callable(function_or_property) else function_or_property


def render(*args, **kwargs):
    user_manager = current_app.user_manager
    return user_manager.render_function(*args, **kwargs)


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
        return redirect(url_for('user.login'))

    if not is_valid:
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(url_for('user.login'))

    # Confirm email by setting User.confirmed_at=utcnow() or UserEmail.confirmed_at=utcnow()
    user = None
    if db_adapter.UserEmailClass:
        user_email = user_manager.get_user_email_by_id(object_id)
        if user_email:
            user_email.confirmed_at = datetime.utcnow()
            user = user_email.user
    else:
        user_email = None
        user = user_manager.get_user_by_id(object_id)
        if user:
            user.confirmed_at = datetime.utcnow()

    if user:
        user.set_active(True)
        db_adapter.commit()
    else:                                               # pragma: no cover
        flash(_('Invalid confirmation token.'), 'error')
        return redirect(url_for('user.login'))

    # Send email_confirmed signal
    signals.user_confirmed_email.send(current_app._get_current_object(), user=user)

    # Prepare one-time system message
    flash(_('Your email has been confirmed.'), 'success')

    # Auto-login after confirm or redirect to login page
    safe_next = _get_safe_next_param('next', user_manager.after_confirm_endpoint)
    if user_manager.auto_login_after_confirm:
        return _do_login_user(user, safe_next)                       # auto-login
    else:
        return redirect(url_for('user.login')+'?next='+quote(safe_next))    # redirect to login page


@login_required
@confirm_email_required
def change_password():
    """ Prompt for old password and new password and change the user's password."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.change_password_form(request.form)
    safe_next = _get_safe_next_param('next', user_manager.after_change_password_endpoint)
    form.next.data = safe_next

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Hash password
        hashed_password = user_manager.hash_password(form.new_password.data)

        # Change password
        user_manager.update_password(current_user, hashed_password)

        # Send 'password_changed' email
        if user_manager.enable_email and user_manager.send_password_changed_email:
            emails.send_password_changed_email(current_user)

        # Send password_changed signal
        signals.user_changed_password.send(current_app._get_current_object(), user=current_user)

        # Prepare one-time system message
        flash(_('Your password has been changed successfully.'), 'success')

        # Redirect to 'next' URL
        safe_next = user_manager.make_safe_url_function(form.next.data)
        return redirect(safe_next)

    # Process GET or invalid POST
    return render(user_manager.change_password_template, form=form)

@login_required
@confirm_email_required
def change_username():
    """ Prompt for new username and old password and change the user's username."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Initialize form
    form = user_manager.change_username_form(request.form)
    safe_next = _get_safe_next_param('next', user_manager.after_change_username_endpoint)
    form.next.data = safe_next

    # Process valid POST
    if request.method=='POST' and form.validate():
        new_username = form.new_username.data

        # Change username
        user_auth = current_user.user_auth if db_adapter.UserAuthClass and hasattr(current_user, 'user_auth') else current_user
        db_adapter.update_object(user_auth, username=new_username)
        db_adapter.commit()

        # Send 'username_changed' email
        if user_manager.enable_email and user_manager.send_username_changed_email:
            emails.send_username_changed_email(current_user)

        # Send username_changed signal
        signals.user_changed_username.send(current_app._get_current_object(), user=current_user)

        # Prepare one-time system message
        flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

        # Redirect to 'next' URL
        safe_next = user_manager.make_safe_url_function(form.next.data)
        return redirect(safe_next)

    # Process GET or invalid POST
    return render(user_manager.change_username_template, form=form)

@login_required
@confirm_email_required
def email_action(id, action):
    """ Perform action 'action' on UserEmail object 'id'
    """
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Retrieve UserEmail by id
    user_email = db_adapter.find_first_object(db_adapter.UserEmailClass, id=id)

    # Users may only change their own UserEmails
    if not user_email or user_email.user_id != int(current_user.get_id()):
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
        user_emails = db_adapter.find_all_objects(db_adapter.UserEmailClass, user_id=int(current_user.get_id()))
        for ue in user_emails:
            if ue.is_primary:
                ue.is_primary = False
        # Enable current primary email
        user_email.is_primary = True
        # Commit
        db_adapter.commit()

    elif action=='confirm':
        _send_confirm_email(user_email.user, user_email)

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
        user, user_email = user_manager.find_user_by_email(email)

        if user:
            user_manager.send_reset_password_email(email)

        # Prepare one-time system message
        flash(_("A reset password email has been sent to '%(email)s'. Open that email and follow the instructions to reset your password.", email=email), 'success')

        # Redirect to the login page
        return redirect(_endpoint_url(user_manager.after_forgot_password_endpoint))

    # Process GET or invalid POST
    return render(user_manager.forgot_password_template, form=form)


def login():
    """ Prompt for username/email and password and sign the user in."""
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    safe_next = _get_safe_next_param('next', user_manager.after_login_endpoint)
    safe_reg_next = _get_safe_next_param('reg_next', user_manager.after_register_endpoint)

    # Immediately redirect already logged in users
    if _call_or_get(current_user.is_authenticated) and user_manager.auto_login_at_login:
        return redirect(safe_next)

    # Initialize form
    login_form = user_manager.login_form(request.form)          # for login.html
    register_form = user_manager.register_form()                # for login_or_register.html
    if request.method!='POST':
        login_form.next.data     = register_form.next.data     = safe_next
        login_form.reg_next.data = register_form.reg_next.data = safe_reg_next

    # Process valid POST
    if request.method=='POST' and login_form.validate():
        # Retrieve User
        user = None
        user_email = None
        if user_manager.enable_username:
            # Find user record by username
            user = user_manager.find_user_by_username(login_form.username.data)
            user_email = None
            # Find primary user_email record
            if user and db_adapter.UserEmailClass:
                user_email = db_adapter.find_first_object(db_adapter.UserEmailClass,
                        user_id=int(user.get_id()),
                        is_primary=True,
                        )
            # Find user record by email (with form.username)
            if not user and user_manager.enable_email:
                user, user_email = user_manager.find_user_by_email(login_form.username.data)
        else:
            # Find user by email (with form.email)
            user, user_email = user_manager.find_user_by_email(login_form.email.data)

        if user:
            # Log user in
            safe_next = user_manager.make_safe_url_function(login_form.next.data)
            return _do_login_user(user, safe_next, login_form.remember_me.data)

    # Process GET or invalid POST
    return render(user_manager.login_template,
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
    safe_next = _get_safe_next_param('next', user_manager.after_logout_endpoint)
    return redirect(safe_next)


@login_required
@confirm_email_required
def manage_emails():
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    user_emails = db_adapter.find_all_objects(db_adapter.UserEmailClass, user_id=int(current_user.get_id()))
    form = user_manager.add_email_form()

    # Process valid POST request
    if request.method=="POST" and form.validate():
        user_emails = db_adapter.add_object(db_adapter.UserEmailClass,
                user_id=int(current_user.get_id()),
                email=form.email.data)
        db_adapter.commit()
        return redirect(url_for('user.manage_emails'))

    # Process GET or invalid POST request
    return render(user_manager.manage_emails_template,
            user_emails=user_emails,
            form=form,
            )

def register():
    """ Display registration form and create new User."""

    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    safe_next = _get_safe_next_param('next', user_manager.after_login_endpoint)
    safe_reg_next = _get_safe_next_param('reg_next', user_manager.after_register_endpoint)

    # Initialize form
    login_form = user_manager.login_form()                      # for login_or_register.html
    register_form = user_manager.register_form(request.form)    # for register.html

    # invite token used to determine validity of registeree
    invite_token = request.values.get("token")

    # require invite without a token should disallow the user from registering
    if user_manager.require_invitation and not invite_token:
        flash("Registration is invite only", "error")
        return redirect(url_for('user.login'))

    user_invite = None
    if invite_token and db_adapter.UserInvitationClass:
        user_invite = db_adapter.find_first_object(db_adapter.UserInvitationClass, token=invite_token)
        if user_invite:
            register_form.invite_token.data = invite_token
        else:
            flash("Invalid invitation token", "error")
            return redirect(url_for('user.login'))

    if request.method!='POST':
        login_form.next.data     = register_form.next.data     = safe_next
        login_form.reg_next.data = register_form.reg_next.data = safe_reg_next
        if user_invite:
            register_form.email.data = user_invite.email

    # Process valid POST
    if request.method=='POST' and register_form.validate():
        # Create a User object using Form fields that have a corresponding User field
        User = db_adapter.UserClass
        user_class_fields = User.__dict__
        user_fields = {}

        # Create a UserEmail object using Form fields that have a corresponding UserEmail field
        if db_adapter.UserEmailClass:
            UserEmail = db_adapter.UserEmailClass
            user_email_class_fields = UserEmail.__dict__
            user_email_fields = {}

        # Create a UserAuth object using Form fields that have a corresponding UserAuth field
        if db_adapter.UserAuthClass:
            UserAuth = db_adapter.UserAuthClass
            user_auth_class_fields = UserAuth.__dict__
            user_auth_fields = {}

        # Enable user account
        if db_adapter.UserProfileClass:
            if hasattr(db_adapter.UserProfileClass, 'active'):
                user_auth_fields['active'] = True
            elif hasattr(db_adapter.UserProfileClass, 'is_enabled'):
                user_auth_fields['is_enabled'] = True
            else:
                user_auth_fields['is_active'] = True
        else:
            if hasattr(db_adapter.UserClass, 'active'):
                user_fields['active'] = True
            elif hasattr(db_adapter.UserClass, 'is_enabled'):
                user_fields['is_enabled'] = True
            else:
                user_fields['is_active'] = True

        # For all form fields
        for field_name, field_value in register_form.data.items():
            # Hash password field
            if field_name=='password':
                hashed_password = user_manager.hash_password(field_value)
                if db_adapter.UserAuthClass:
                    user_auth_fields['password'] = hashed_password
                else:
                    user_fields['password'] = hashed_password
            # Store corresponding Form fields into the User object and/or UserProfile object
            else:
                if field_name in user_class_fields:
                    user_fields[field_name] = field_value
                if db_adapter.UserEmailClass:
                    if field_name in user_email_class_fields:
                        user_email_fields[field_name] = field_value
                if db_adapter.UserAuthClass:
                    if field_name in user_auth_class_fields:
                        user_auth_fields[field_name] = field_value

        # Add User record using named arguments 'user_fields'
        user = db_adapter.add_object(User, **user_fields)
        if db_adapter.UserProfileClass:
            user_profile = user

        # Add UserEmail record using named arguments 'user_email_fields'
        if db_adapter.UserEmailClass:
            user_email = db_adapter.add_object(UserEmail,
                    user=user,
                    is_primary=True,
                    **user_email_fields)
        else:
            user_email = None

        # Add UserAuth record using named arguments 'user_auth_fields'
        if db_adapter.UserAuthClass:
            user_auth = db_adapter.add_object(UserAuth, **user_auth_fields)
            if db_adapter.UserProfileClass:
                user = user_auth
            else:
                user.user_auth = user_auth

        require_email_confirmation = True
        if user_invite:
            if user_invite.email == register_form.email.data:
                require_email_confirmation = False
                db_adapter.update_object(user, confirmed_at=datetime.utcnow())

        db_adapter.commit()

        # Send 'registered' email and delete new User object if send fails
        if user_manager.send_registered_email:
            try:
                # Send 'registered' email
                _send_registered_email(user, user_email, require_email_confirmation)
            except Exception as e:
                # delete new User object if send  fails
                db_adapter.delete_object(user)
                db_adapter.commit()
                raise

        # Send user_registered signal
        signals.user_registered.send(current_app._get_current_object(),
                                     user=user,
                                     user_invite=user_invite)

        # Redirect if USER_ENABLE_CONFIRM_EMAIL is set
        if user_manager.enable_confirm_email and require_email_confirmation:
            safe_reg_next = user_manager.make_safe_url_function(register_form.reg_next.data)
            return redirect(safe_reg_next)

        # Auto-login after register or redirect to login page
        if 'reg_next' in request.args:
            safe_reg_next = user_manager.make_safe_url_function(register_form.reg_next.data)
        else:
            safe_reg_next = _endpoint_url(user_manager.after_confirm_endpoint)
        if user_manager.auto_login_after_register:
            return _do_login_user(user, safe_reg_next)                     # auto-login
        else:
            return redirect(url_for('user.login')+'?next='+quote(safe_reg_next))  # redirect to login page

    # Process GET or invalid POST
    return render(user_manager.register_template,
            form=register_form,
            login_form=login_form,
            register_form=register_form)

@login_required
def invite():
    """ Allows users to send invitations to register an account """
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    invite_form = user_manager.invite_form(request.form)

    if request.method=='POST' and invite_form.validate():
        email = invite_form.email.data

        User = db_adapter.UserClass
        user_class_fields = User.__dict__
        user_fields = {
            "email": email
        }

        user, user_email = user_manager.find_user_by_email(email)
        if user:
            flash("User with that email has already registered", "error")
            return redirect(url_for('user.invite'))
        else:
            user_invite = db_adapter \
                            .add_object(db_adapter.UserInvitationClass, **{
                                "email": email,
                                "invited_by_user_id": current_user.id
                            })
        db_adapter.commit()

        token = user_manager.generate_token(user_invite.id)
        accept_invite_link = url_for('user.register',
                                     token=token,
                                     _external=True)

        # Store token
        if hasattr(db_adapter.UserInvitationClass, 'token'):
            user_invite.token = token
            db_adapter.commit()

        try:
            # Send 'invite' email
            emails.send_invite_email(user_invite, accept_invite_link)
        except Exception as e:
            # delete new User object if send fails
            db_adapter.delete_object(user_invite)
            db_adapter.commit()
            raise

        signals \
            .user_sent_invitation \
            .send(current_app._get_current_object(), user_invite=user_invite,
                  form=invite_form)

        flash(_('Invitation has been sent.'), 'success')
        safe_next = _get_safe_next_param('next', user_manager.after_invite_endpoint)
        return redirect(safe_next)

    return render(user_manager.invite_template, form=invite_form)

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
            _send_confirm_email(user, user_email)

        # Redirect to the login page
        return redirect(_endpoint_url(user_manager.after_resend_confirm_email_endpoint))

    # Process GET or invalid POST
    return render(user_manager.resend_confirm_email_template, form=form)


def reset_password(token):
    """ Verify the password reset token, Prompt for new password, and set the user's password."""
    # Verify token
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    if _call_or_get(current_user.is_authenticated):
        logout_user()

    is_valid, has_expired, user_id = user_manager.verify_token(
            token,
            user_manager.reset_password_expiration)

    if has_expired:
        flash(_('Your reset password token has expired.'), 'error')
        return redirect(_endpoint_url(user_manager.login_endpoint))

    if not is_valid:
        flash(_('Your reset password token is invalid.'), 'error')
        return redirect(_endpoint_url(user_manager.login_endpoint))

    user = user_manager.get_user_by_id(user_id)

    # Mark email as confirmed
    user_email = emails.get_primary_user_email(user)
    user_email.confirmed_at = datetime.utcnow()
    db_adapter.commit()

    # Initialize form
    form = user_manager.reset_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():

        # Change password
        hashed_password = user_manager.hash_password(form.new_password.data)
        user_auth = user.user_auth if db_adapter.UserAuthClass and hasattr(user, 'user_auth') else user
        db_adapter.update_object(user_auth, password=hashed_password)
        db_adapter.commit()

        # Send 'password_changed' email
        if user_manager.enable_email and user_manager.send_password_changed_email:
            emails.send_password_changed_email(user)

        # Send user_reset_password signal
        signals.user_reset_password.send(current_app._get_current_object(), user=user)

        # Prepare one-time system message
        flash(_("Your password has been reset successfully."), 'success')

        # Auto-login after reset password or redirect to login page
        safe_next = _get_safe_next_param('next', user_manager.after_reset_password_endpoint)
        if user_manager.auto_login_after_reset_password:
            return _do_login_user(user, safe_next)                       # auto-login
        else:
            return redirect(url_for('user.login')+'?next='+quote(safe_next))    # redirect to login page

    # Process GET or invalid POST
    return render(user_manager.reset_password_template, form=form)


def unconfirmed():
    """ Prepare a Flash message and redirect to USER_UNCONFIRMED_ENDPOINT"""
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_("You must confirm your email to access '%(url)s'.", url=url), 'error')

    # Redirect to USER_UNCONFIRMED_EMAIL_ENDPOINT
    user_manager = current_app.user_manager
    return redirect(_endpoint_url(user_manager.unconfirmed_email_endpoint))


def unauthenticated():
    """ Prepare a Flash message and redirect to USER_UNAUTHENTICATED_ENDPOINT"""
    user_manager = current_app.user_manager
    # Prepare Flash message
    url = request.url
    flash(_("You must be signed in to access '%(url)s'.", url=url), 'error')

    # Redirect to USER_UNAUTHENTICATED_ENDPOINT
    safe_next = user_manager.make_safe_url_function(url)
    return redirect(_endpoint_url(user_manager.unauthenticated_endpoint)+'?next='+quote(safe_next))


def unauthorized():
    """ Prepare a Flash message and redirect to USER_UNAUTHORIZED_ENDPOINT"""
    # Prepare Flash message
    url = request.script_root + request.path
    flash(_("You do not have permission to access '%(url)s'.", url=url), 'error')

    # Redirect to USER_UNAUTHORIZED_ENDPOINT
    user_manager = current_app.user_manager
    return redirect(_endpoint_url(user_manager.unauthorized_endpoint))


@login_required
@confirm_email_required
def user_profile():
    user_manager = current_app.user_manager
    return render(user_manager.user_profile_template)


def _send_registered_email(user, user_email, require_email_confirmation=True):
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Send 'confirm_email' or 'registered' email
    if user_manager.enable_email and user_manager.enable_confirm_email:
        # Generate confirm email link
        object_id = user_email.id if user_email else int(user.get_id())
        token = user_manager.generate_token(object_id)
        confirm_email_link = url_for('user.confirm_email', token=token, _external=True)

        # Send email
        emails.send_registered_email(user, user_email, confirm_email_link)

        # Prepare one-time system message
        if user_manager.enable_confirm_email and require_email_confirmation:
            email = user_email.email if user_email else user.email
            flash(_('A confirmation email has been sent to %(email)s with instructions to complete your registration.', email=email), 'success')
        else:
            flash(_('You have registered successfully.'), 'success')


def _send_confirm_email(user, user_email):
    user_manager =  current_app.user_manager
    db_adapter = user_manager.db_adapter

    # Send 'confirm_email' or 'registered' email
    if user_manager.enable_email and user_manager.enable_confirm_email:
        # Generate confirm email link
        object_id = user_email.id if user_email else int(user.get_id())
        token = user_manager.generate_token(object_id)
        confirm_email_link = url_for('user.confirm_email', token=token, _external=True)

        # Send email
        emails.send_confirm_email_email(user, user_email, confirm_email_link)

        # Prepare one-time system message
        email = user_email.email if user_email else user.email
        flash(_('A confirmation email has been sent to %(email)s with instructions to complete your registration.', email=email), 'success')


def _do_login_user(user, safe_next, remember_me=False):
    # User must have been authenticated
    if not user: return unauthenticated()

    # Check if user account has been disabled
    if not _call_or_get(user.is_active):
        flash(_('Your account has not been enabled.'), 'error')
        return redirect(url_for('user.login'))

    # Check if user has a confirmed email address
    user_manager = current_app.user_manager
    if user_manager.enable_email and user_manager.enable_confirm_email \
            and not current_app.user_manager.enable_login_without_confirm_email \
            and not user.has_confirmed_email():
        url = url_for('user.resend_confirm_email')
        flash(_('Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email or <a href="%(url)s">Re-send confirmation email</a>.', url=url), 'error')
        return redirect(url_for('user.login'))

    # Use Flask-Login to sign in user
    #print('login_user: remember_me=', remember_me)
    login_user(user, remember=remember_me)

    # Send user_logged_in signal
    signals.user_logged_in.send(current_app._get_current_object(), user=user)

    # Prepare one-time system message
    flash(_('You have signed in successfully.'), 'success')

    # Redirect to 'safe_next' URL
    return redirect(safe_next)


def make_safe_url(url):
    """Makes a URL safe by removing optional hostname and port.

    Example:

        | ``make_safe_url('https://hostname:80/path1/path2?q1=v1&q2=v2#fragment')``
        | returns ``'/path1/path2?q1=v1&q2=v2#fragment'``

    Override this method if you need to allow a list of safe hostnames.
    """

    # Split the URL into scheme, netloc, path, query and fragment
    parts = list(urlsplit(url))

    # Clear scheme and netloc and rebuild URL
    parts[0] = ''  # Empty scheme
    parts[1] = ''  # Empty netloc (hostname:port)
    safe_url = urlunsplit(parts)
    return safe_url


# 'next' and 'reg_next' query parameters contain quoted (URL-encoded) URLs
# that may contain unsafe hostnames.
# Return the query parameter as a safe, unquoted URL
def _get_safe_next_param(param_name, default_endpoint):
    if param_name in request.args:
        # return safe unquoted query parameter value
        safe_next = current_app.user_manager.make_safe_url_function(unquote(request.args[param_name]))
    else:
        # return URL of default endpoint
        safe_next = _endpoint_url(default_endpoint)
    return safe_next


def _endpoint_url(endpoint):
    url = '/'
    if endpoint:
        url = url_for(endpoint)
    return url


