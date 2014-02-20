from flask import current_app, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user


def register():
    um = current_app.user_manager

    # Initialize form
    form = um.register_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        hashed_password = um.crypt_context.encrypt(form.password.data)
        if um.login_with_username:
            um.db_adapter.add_user(
                username=form.username.data,
                password=hashed_password)
        else:
            um.db_adapter.add_user(
                email=form.email.data,
                password=hashed_password)
        return redirect(um.login_url)

    # Process GET or invalid POST
    return render_template(um.register_template, form=form)

def login():
    um = current_app.user_manager

    # Initialize form
    form = um.login_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Retrieve User
        if um.login_with_username:
            user = um.db_adapter.find_user_by_username(form.username.data)
        else:
            user = um.db_adapter.find_user_by_email(form.email.data)

        if user:
            # Use Flask-Login to sign in user
            login_user(user)

            # Prepare Flash message
            flash(um.flash_signed_in, 'success')

            # Redirect to 'next' URL or '/'
            next = form.next.data
            if not next:
                return redirect('/')
            return redirect(next)

    # Process GET or invalid POST
    return render_template(um.login_template, form=form)

def logout():
    um = current_app.user_manager

    # Use Flask-Login to sign out user
    logout_user()

    # Prepare Flash message
    flash(um.flash_signed_out, 'success')

    # Redirect to logout_next endpoint or '/'
    if um.logout_next:
        return redirect(url_for(um.logout_next))
    else:
        return redirect('/')

@login_required
def change_password():
    um = current_app.user_manager

    # Initialize form
    form = um.change_password_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Change password
        um.db_adapter.set_password(current_user, um.crypt_context.encrypt(form.new_password.data))

        # Prepare Flash message
        flash(um.flash_password_changed, 'success')

        # Redirect to 'next' URL or '/'
        next = form.next.data
        if not next:
            return redirect('/')
        return redirect(next)

    # Process GET or invalid POST
    return render_template(um.change_password_template, form=form)

@login_required
def change_username():
    um = current_app.user_manager

    # Initialize form
    form = um.change_username_form(request.form)

    # Process valid POST
    if request.method=='POST' and form.validate():
        # Change username
        um.db_adapter.set_username(current_user, form.new_username.data)

        # Prepare Flash message
        flash(um.flash_username_changed, 'success')

        # Redirect to 'next' URL or '/'
        next = form.next.data
        if not next:
            return redirect('/')
        return redirect(next)

    # Process GET or invalid POST
    return render_template(um.change_username_template, form=form)

