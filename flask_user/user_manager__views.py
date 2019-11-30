"""This module implements UserManager view methods.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio

from datetime import datetime
try:
    from urllib.parse import quote, unquote    # Python 3
except ImportError:
    from urllib import quote, unquote          # Python 2

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from .decorators import login_required
from . import signals
from .translation_utils import gettext as _    # map _() to gettext()


# This class mixes into the UserManager class.
# Mixins allow for maintaining code and docs across several files.
class UserManager__Views(object):
    """Flask-User views."""

    # # This callback view is called by Auth0's Lock Widget after a user logs in successfully
    # def auth0_callback_view(self):  # pragma: no cover
    #     """This callback is called after a successful Auth0 login.
    #
    #     Args:
    #         code(str): Auth0's authentication code.
    #     """
    #
    #     # Check for errors
    #     error = request.args.get('error')
    #     if error:
    #         error_code = request.args.get('error_description')
    #         return redirect(url_for('regular.unauthorized', error_code=error_code))
    #
    #     from auth0.v3.authentication import GetToken
    #     from auth0.v3.authentication import Users
    #     import json
    #
    #     # Retrieve AUTH0 settings from the local settings file
    #     AUTH0_DOMAIN = current_app.config.get('AUTH0_DOMAIN', '')
    #     AUTH0_CLIENT_ID = current_app.config.get('AUTH0_CLIENT_ID', '')
    #     AUTH0_CLIENT_SECRET = current_app.config.get('AUTH0_CLIENT_SECRET', '')
    #     AUTH0_CALLBACK_URL = url_for('user.auth0_callback', _external=True)
    #
    #     auth0_users = Users(AUTH0_DOMAIN)
    #
    #     # Retrieve Auth0 code from the URL query parameters
    #     code = request.args.get('code')
    #
    #     # Decode Auth0 code and extract the Auth0 Token
    #     get_token = GetToken(AUTH0_DOMAIN)
    #     token = get_token.authorization_code(AUTH0_CLIENT_ID,
    #                                          AUTH0_CLIENT_SECRET,
    #                                          code,
    #                                          AUTH0_CALLBACK_URL)
    #
    #     # Retrieve user_info from AUTH0 token
    #     user_info_str = auth0_users.userinfo(token['access_token'])
    #     user_info = json.loads(user_info_str)
    #     email = user_info['email']
    #     email_verified = user_info['email_verified']
    #
    #     # Retrieve User record by email
    #     user, user_email = self.db_manager.get_user_and_user_email_by_email(email)
    #     if not user:
    #         # Create new user if needed
    #         user = self.db_manager.add_user(
    #             email=email,
    #             active=True,
    #             first_name=user_info.get('given_name', ''),
    #             last_name=user_info.get('family_name', ''),
    #         )
    #         self.db_manager.commit()
    #
    #     # Retrieve next URL from 'state' query param
    #     state = request.args.get('state', '/')
    #     safe_next_url = self.make_safe_url(state)
    #
    #     # Log user in
    #     return self._do_login_user(user, safe_next_url)

    @login_required
    def change_password_view(self):
        """ Prompt for old password and new password and change the user's password."""

        # Initialize form
        form = self.ChangePasswordFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Hash password
            new_password = form.new_password.data
            password_hash = self.hash_password(new_password)

            # Update user.password
            current_user.password = password_hash
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            # Send password_changed email
            if self.USER_ENABLE_EMAIL and self.USER_SEND_PASSWORD_CHANGED_EMAIL:
                self.email_manager.send_password_changed_email(current_user)

            # Send changed_password signal
            signals.user_changed_password.send(current_app._get_current_object(), user=current_user)

            # Flash a system message
            flash(_('Your password has been changed successfully.'), 'success')

            # Redirect to 'next' URL
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CHANGE_PASSWORD_ENDPOINT)
            return redirect(safe_next_url)

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_CHANGE_PASSWORD_TEMPLATE, form=form)


    @login_required
    def change_username_view(self):
        """ Prompt for new username and old password and change the user's username."""

        # Initialize form
        form = self.ChangeUsernameFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():

            # Change username
            new_username = form.new_username.data
            current_user.username=new_username
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            # Send username_changed email
            if self.USER_ENABLE_EMAIL and self.USER_SEND_USERNAME_CHANGED_EMAIL:
                self.email_manager.send_username_changed_email(current_user)

            # Send changed_username signal
            signals.user_changed_username.send(current_app._get_current_object(), user=current_user)

            # Flash a system message
            flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

            # Redirect to 'next' URL
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CHANGE_USERNAME_ENDPOINT)
            return redirect(safe_next_url)

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_CHANGE_USERNAME_TEMPLATE, form=form)


    def confirm_email_view(self, token):
        """ Verify email confirmation token and activate the user account."""
        # Verify token
        data_items = self.token_manager.verify_token(
            token,
            self.USER_CONFIRM_EMAIL_EXPIRATION)

        # Retrieve user, user_email by ID
        user = None
        user_email = None
        if data_items:
            user, user_email = self.db_manager.get_user_and_user_email_by_id(data_items[0])

        if not user or not user_email:
            flash(_('Invalid confirmation token.'), 'error')
            return redirect(url_for('user.login'))

        # Set UserEmail.email_confirmed_at
        user_email.email_confirmed_at=datetime.utcnow()
        self.db_manager.save_user_and_user_email(user, user_email)
        self.db_manager.commit()

        # Send confirmed_email signal
        signals.user_confirmed_email.send(current_app._get_current_object(), user=user)

        # Flash a system message
        flash(_('Your email has been confirmed.'), 'success')

        # Auto-login after confirm or redirect to login page
        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CONFIRM_ENDPOINT)
        if self.USER_AUTO_LOGIN_AFTER_CONFIRM:
            return self._do_login_user(user, safe_next_url)  # auto-login
        else:
            return redirect(url_for('user.login') + '?next=' + quote(safe_next_url))  # redirect to login page


    @login_required
    def edit_user_profile_view(self):
        # Initialize form
        form = self.EditUserProfileFormClass(request.form, obj=current_user)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Update fields
            form.populate_obj(current_user)

            # Save object
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            return redirect(self._endpoint_url(self.USER_AFTER_EDIT_USER_PROFILE_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_EDIT_USER_PROFILE_TEMPLATE, form=form)

    @login_required
    def email_action_view(self, id, action):
        """ Perform action 'action' on UserEmail object 'id'
        """

        # Retrieve UserEmail by id
        user_email = self.db_manager.get_user_email_by_id(id=id)

        # Users may only change their own UserEmails
        if not user_email or user_email.user_id != current_user.id:
            return self.unauthorized_view()

        # Delete UserEmail
        if action == 'delete':
            # Primary UserEmail can not be deleted
            if user_email.is_primary:
                return self.unauthorized_view()
            # Delete UserEmail
            self.db_manager.delete_object(user_email)
            self.db_manager.commit()

        # Set UserEmail.is_primary
        elif action == 'make-primary':
            # Disable previously primary emails
            user_emails = self.db_manager.find_user_emails(current_user)
            for other_user_email in user_emails:
                if other_user_email.is_primary:
                    other_user_email.is_primary=False
                    self.db_manager.save_object(other_user_email)
            # Enable current primary email
            user_email.is_primary=True
            self.db_manager.save_object(user_email)
            self.db_manager.commit()

        # Send confirm email
        elif action == 'confirm':
            self._send_confirm_email_email(user_email.user, user_email)
        else:
            return self.unauthorized_view()

        return redirect(url_for('user.manage_emails'))


    def forgot_password_view(self):
        """Prompt for email and send reset password email."""

        # Initialize form
        form = self.ForgotPasswordFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Get User and UserEmail by email
            email = form.email.data
            user, user_email = self.db_manager.get_user_and_user_email_by_email(email)

            if user and user_email:
                # Send reset_password email
                self.email_manager.send_reset_password_email(user, user_email)

                # Send forgot_password signal
                signals.user_forgot_password.send(current_app._get_current_object(), user=user)

            # Flash a system message
            flash(_(
                "A reset password email has been sent to '%(email)s'. Open that email and follow the instructions to reset your password.",
                email=email), 'success')

            # Redirect to the login page
            return redirect(self._endpoint_url(self.USER_AFTER_FORGOT_PASSWORD_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_FORGOT_PASSWORD_TEMPLATE, form=form)

    @login_required
    def manage_emails_view(self):

        # Retrieve a user's UserEmails
        user_emails = self.db_manager.find_user_emails(user=current_user)
        form = self.AddEmailFormClass()

        # Process valid POST request
        if request.method == "POST" and form.validate():
            # Add a new UserEmail
            new_email = form.email.data
            user_email = self.db_manager.add_user_email(user=current_user, email=new_email)
            # Save new UserEmail
            self.db_manager.save_object(user_email)
            self.db_manager.commit()
            return redirect(url_for('user.manage_emails'))

        # Process GET or invalid POST request
        self.prepare_domain_translations()
        return render_template(self.USER_MANAGE_EMAILS_TEMPLATE,
                      user_emails=user_emails,
                      form=form,
                      )

    @login_required
    def invite_user_view(self):
        """ Allows users to send invitations to register an account """

        invite_user_form = self.InviteUserFormClass(request.form)

        if request.method == 'POST' and invite_user_form.validate():
            # Find User and UserEmail by email
            email = invite_user_form.email.data
            user, user_email = self.db_manager.get_user_and_user_email_by_email(email)
            if user:
                flash("User with that email has already registered", "error")
                return redirect(url_for('user.invite_user'))

            # Add UserInvitation
            user_invitation = self.db_manager.add_user_invitation(
                email=email,
                invited_by_user_id=current_user.id)
            self.db_manager.commit()

            try:
                # Send invite_user email
                self.email_manager.send_invite_user_email(current_user, user_invitation)
            except Exception as e:
                # delete new UserInvitation object if send fails
                self.db_manager.delete_object(user_invitation)
                self.db_manager.commit()
                raise

            # Send sent_invitation signal
            signals \
                .user_sent_invitation \
                .send(current_app._get_current_object(), user_invitation=user_invitation,
                      form=invite_user_form)

            # Flash a system message
            flash(_('Invitation has been sent.'), 'success')

            # Redirect
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_INVITE_ENDPOINT)
            return redirect(safe_next_url)

        self.prepare_domain_translations()
        return render_template(self.USER_INVITE_USER_TEMPLATE, form=invite_user_form)


    def login_view(self):
        """Prepare and process the login form."""

        # Authenticate username/email and login authenticated users.

        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next = self._get_safe_next_url('reg_next', self.USER_AFTER_REGISTER_ENDPOINT)

        # Immediately redirect already logged in users
        if self.call_or_get(current_user.is_authenticated) and self.USER_AUTO_LOGIN_AT_LOGIN:
            return redirect(safe_next_url)

        # Initialize form
        login_form = self.LoginFormClass(request.form)  # for login.html
        register_form = self.RegisterFormClass()  # for login_or_register.html
        if request.method != 'POST':
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next

        # Process valid POST
        if request.method == 'POST' and login_form.validate():
            # Retrieve User
            user = None
            user_email = None
            if self.USER_ENABLE_USERNAME:
                # Find user record by username
                user = self.db_manager.find_user_by_username(login_form.username.data)

                # Find user record by email (with form.username)
                if not user and self.USER_ENABLE_EMAIL:
                    user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.username.data)
            else:
                # Find user by email (with form.email)
                user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.email.data)

            if user:
                # Log user in
                safe_next_url = self.make_safe_url(login_form.next.data)
                return self._do_login_user(user, safe_next_url, login_form.remember_me.data)

        # Render form
        self.prepare_domain_translations()
        template_filename = self.USER_LOGIN_AUTH0_TEMPLATE if self.USER_ENABLE_AUTH0 else self.USER_LOGIN_TEMPLATE
        return render_template(template_filename,
                      form=login_form,
                      login_form=login_form,
                      register_form=register_form)

    def logout_view(self):
        """Process the logout link."""
        """ Sign the user out."""

        # Send user_logged_out signal
        signals.user_logged_out.send(current_app._get_current_object(), user=current_user)

        # Use Flask-Login to sign out user
        logout_user()

        # Flash a system message
        flash(_('You have signed out successfully.'), 'success')

        # Redirect to logout_next endpoint or '/'
        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGOUT_ENDPOINT)
        return redirect(safe_next_url)

    def register_view(self):
        """ Display registration form and create new User."""

        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next_url = self._get_safe_next_url('reg_next', self.USER_AFTER_REGISTER_ENDPOINT)

        # Initialize form
        login_form = self.LoginFormClass()  # for login_or_register.html
        register_form = self.RegisterFormClass(request.form)  # for register.html

        # invite token used to determine validity of registeree
        invite_token = request.values.get("token")

        # require invite without a token should disallow the user from registering
        if self.USER_REQUIRE_INVITATION and not invite_token:
            flash("Registration is invite only", "error")
            return redirect(url_for('user.login'))

        user_invitation = None
        if invite_token and self.db_manager.UserInvitationClass:
            data_items = self.token_manager.verify_token(invite_token, self.USER_INVITE_EXPIRATION)
            if data_items:
                user_invitation_id = data_items[0]
                user_invitation = self.db_manager.get_user_invitation_by_id(user_invitation_id)

            if not user_invitation:
                flash("Invalid invitation token", "error")
                return redirect(url_for('user.login'))

            register_form.invite_token.data = invite_token

        if request.method != 'POST':
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next_url
            if user_invitation:
                register_form.email.data = user_invitation.email

        # Process valid POST
        if request.method == 'POST' and register_form.validate():
            user = self.db_manager.add_user()
            register_form.populate_obj(user)
            user_email = self.db_manager.add_user_email(user=user, is_primary=True)
            register_form.populate_obj(user_email)

            # Store password hash instead of password
            user.password = self.hash_password(user.password)

            # Email confirmation depends on the USER_ENABLE_CONFIRM_EMAIL setting
            request_email_confirmation = self.USER_ENABLE_CONFIRM_EMAIL
            # Users that register through an invitation, can skip this process
            # but only when they register with an email that matches their invitation.
            if user_invitation:
                if user_invitation.email.lower() == register_form.email.data.lower():
                    user_email.email_confirmed_at=datetime.utcnow()
                    request_email_confirmation = False

            self.db_manager.save_user_and_user_email(user, user_email)
            self.db_manager.commit()

            # Send 'registered' email and delete new User object if send fails
            if self.USER_SEND_REGISTERED_EMAIL:
                try:
                    # Send 'confirm email' or 'registered' email
                    self._send_registered_email(user, user_email, request_email_confirmation)
                except Exception as e:
                    # delete new User object if send  fails
                    self.db_manager.delete_object(user)
                    self.db_manager.commit()
                    raise

            # Send user_registered signal
            signals.user_registered.send(current_app._get_current_object(),
                                         user=user,
                                         user_invitation=user_invitation)

            # Redirect if USER_ENABLE_CONFIRM_EMAIL is set
            if self.USER_ENABLE_CONFIRM_EMAIL and request_email_confirmation:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
                return redirect(safe_reg_next_url)

            # Auto-login after register or redirect to login page
            if 'reg_next' in request.args:
                safe_reg_next_url = self.make_safe_url(register_form.reg_next.data)
            else:
                safe_reg_next_url = self._endpoint_url(self.USER_AFTER_CONFIRM_ENDPOINT)
            if self.USER_AUTO_LOGIN_AFTER_REGISTER:
                return self._do_login_user(user, safe_reg_next_url)  # auto-login
            else:
                return redirect(url_for('user.login') + '?next=' + quote(safe_reg_next_url))  # redirect to login page

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_REGISTER_TEMPLATE,
                      form=register_form,
                      login_form=login_form,
                      register_form=register_form)


    def resend_email_confirmation_view(self):
        """Prompt for email and re-send email conformation email."""

        # Initialize form
        form = self.ResendEmailConfirmationFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():

            # Find user by email
            email = form.email.data
            user, user_email = self.db_manager.get_user_and_user_email_by_email(email)

            # Send confirm_email email
            if user:
                self._send_confirm_email_email(user, user_email)

            # Redirect to the login page
            return redirect(self._endpoint_url(self.USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT))

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_RESEND_CONFIRM_EMAIL_TEMPLATE, form=form)


    def reset_password_view(self, token):
        """ Verify the password reset token, Prompt for new password, and set the user's password."""
        # Verify token

        if self.call_or_get(current_user.is_authenticated):
            logout_user()

        data_items = self.token_manager.verify_token(
            token,
            self.USER_RESET_PASSWORD_EXPIRATION)

        user = None
        if data_items:
            # Get User by user ID
            user_id = data_items[0]
            user = self.db_manager.get_user_by_id(user_id)

            # Mark email as confirmed
            user_or_user_email_object = self.db_manager.get_primary_user_email_object(user)
            user_or_user_email_object.email_confirmed_at = datetime.utcnow()
            self.db_manager.save_object(user_or_user_email_object)
            self.db_manager.commit()

        if not user:
            flash(_('Your reset password token is invalid.'), 'error')
            return redirect(self._endpoint_url('user.login'))


        # Initialize form
        form = self.ResetPasswordFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Change password
            password_hash = self.hash_password(form.new_password.data)
            user.password=password_hash
            self.db_manager.save_object(user)
            self.db_manager.commit()

            # Send 'password_changed' email
            if self.USER_ENABLE_EMAIL and self.USER_SEND_PASSWORD_CHANGED_EMAIL:
                self.email_manager.send_password_changed_email(user)

            # Send reset_password signal
            signals.user_reset_password.send(current_app._get_current_object(), user=user)

            # Flash a system message
            flash(_("Your password has been reset successfully."), 'success')

            # Auto-login after reset password or redirect to login page
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_RESET_PASSWORD_ENDPOINT)
            if self.USER_AUTO_LOGIN_AFTER_RESET_PASSWORD:
                return self._do_login_user(user, safe_next_url)  # auto-login
            else:
                return redirect(url_for('user.login') + '?next=' + quote(safe_next_url))  # redirect to login page

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_RESET_PASSWORD_TEMPLATE, form=form)

    def unauthenticated_view(self):
        """ Prepare a Flash message and redirect to USER_UNAUTHENTICATED_ENDPOINT"""
        # Prepare Flash message
        url = request.url
        flash(_("You must be signed in to access '%(url)s'.", url=url), 'error')

        # Redirect to USER_UNAUTHENTICATED_ENDPOINT
        safe_next_url = self.make_safe_url(url)
        return redirect(self._endpoint_url(self.USER_UNAUTHENTICATED_ENDPOINT)+'?next='+quote(safe_next_url))


    def unauthorized_view(self):
        """ Prepare a Flash message and redirect to USER_UNAUTHORIZED_ENDPOINT"""
        # Prepare Flash message
        url = request.script_root + request.path
        flash(_("You do not have permission to access '%(url)s'.", url=url), 'error')

        # Redirect to USER_UNAUTHORIZED_ENDPOINT
        return redirect(self._endpoint_url(self.USER_UNAUTHORIZED_ENDPOINT))

    # def unconfirmed_email_view(self):
    #     """ Prepare a Flash message and redirect to USER_UNCONFIRMED_ENDPOINT"""
    #     # Prepare Flash message
    #     url = request.script_root + request.path
    #     flash(_("You must confirm your email to access '%(url)s'.", url=url), 'error')
    #
    #     # Redirect to USER_UNCONFIRMED_EMAIL_ENDPOINT
    #     return redirect(self._endpoint_url(self.USER_UNCONFIRMED_EMAIL_ENDPOINT))


    def _send_registered_email(self, user, user_email, request_email_confirmation):
        um =  current_app.user_manager

        if self.USER_ENABLE_EMAIL and self.USER_SEND_REGISTERED_EMAIL:

            # Send 'registered' email, with or without a confirmation request
            self.email_manager.send_registered_email(user, user_email, request_email_confirmation)

            # Flash a system message
            if request_email_confirmation:
                email = user_email.email if user_email else user.email
                flash(_('A confirmation email has been sent to %(email)s with instructions to complete your registration.', email=email), 'success')
            else:
                flash(_('You have registered successfully.'), 'success')


    def _send_confirm_email_email(self, user, user_email):

        # Send 'confirm_email' or 'registered' email
        if self.USER_ENABLE_EMAIL and self.USER_ENABLE_CONFIRM_EMAIL:
            # Send email
            self.email_manager.send_confirm_email_email(user, user_email)

            # Flash a system message
            email = user_email.email if user_email else user.email
            flash(_('A confirmation email has been sent to %(email)s with instructions to complete your registration.', email=email), 'success')


    def _do_login_user(self, user, safe_next_url, remember_me=False):
        # User must have been authenticated
        if not user: return self.unauthenticated()

        # Check if user account has been disabled
        if not user.active:
            flash(_('Your account has not been enabled.'), 'error')
            return redirect(url_for('user.login'))

        # Check if user has a confirmed email address
        if self.USER_ENABLE_EMAIL \
                and self.USER_ENABLE_CONFIRM_EMAIL \
                and not current_app.user_manager.USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL \
                and not self.db_manager.user_has_confirmed_email(user):
            url = url_for('user.resend_email_confirmation')
            flash(_('Your email address has not yet been confirmed. Check your email Inbox and Spam folders for the confirmation email or <a href="%(url)s">Re-send confirmation email</a>.', url=url), 'error')
            return redirect(url_for('user.login'))

        # Use Flask-Login to sign in user
        # print('login_user: remember_me=', remember_me)
        login_user(user, remember=remember_me)

        # Send user_logged_in signal
        signals.user_logged_in.send(current_app._get_current_object(), user=user)

        # Flash a system message
        flash(_('You have signed in successfully.'), 'success')

        # Redirect to 'next' URL
        return redirect(safe_next_url)


    # Returns safe URL from query param ``param_name`` if query param exists.
    # Returns url_for(default_endpoint) otherwise.
    def _get_safe_next_url(self, param_name, default_endpoint):

        # Returns safe URL from query param ``param_name`` if query param exists.
        if param_name in request.args:
            safe_next_url = current_app.user_manager.make_safe_url(unquote(request.args[param_name]))

        # Returns url_for(default_endpoint) otherwise.
        else:
            safe_next_url = self._endpoint_url(default_endpoint)

        return safe_next_url


    def _endpoint_url(self, endpoint):
        return url_for(endpoint) if endpoint else '/'

