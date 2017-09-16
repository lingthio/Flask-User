Customizing Emails
==================

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst

--------

.. _CustomizingEmailAdapters:

Customizing EmailAdapters
-------------------------
Flask-User ships with the following EmailAdapters:
- SendgridEmailAdapter to send email messages via Sendgrid
- SendmailEmailAdapter to send email messages via Sendmail
- SMTPEmailAdapter to send email messages via SMTP

Flask-User works with the SMTPEmailAdapter by default, but another EmailAdapter can be configured like so::

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Customize Flask-User
    from flask_user.email_adapters import SendgridEmailAdapter
    user_manager.email_adapter = SendgridEmailAdapter(app)


--------

Customizing Email messages
--------------------------

Flask-User currently offers the following types of email messages::

    confirm_email     # Sent after a user submitted a registration form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CONFIRM_EMAIL = True

    forgot_password   # Sent after a user submitted a forgot password form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_FORGOT_PASSWORD = True

    password_changed  # Sent after a user submitted a change password or reset password form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CHANGE_PASSWORD = True
                      # - Requires USER_SEND_PASSWORD_CHANGED_EMAIL = True

    registered        # Sent to users after they submitted a registration form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CONFIRM_EMAIL = False
                      # - Requires USER_SEND_REGISTERED_EMAIL = True

    username_changed  # Sent after a user submitted a change username form
                      # - Requires USER_ENABLE_EMAIL = True
                      # - Requires USER_ENABLE_CHANGE_USERNAME = True
                      # - Requires USER_SEND_USERNAME_CHANGED_EMAIL = True

Emails are constructed using three email template files, using the Jinja2 templating engine.
The 'registered' email, for example, makes use of the following template files::

    registered_subject.txt   # Subject line
    registered_message.html  # Message in HTML format
    registered_message.txt   # Message in Text format

Which, in turn, depend on the common base template files::

    base_subject.txt
    base_message.html
    base_message.txt

The base templates are shared across all message types.
Typically the base templates define the message design (the look-and-feel)
while the message templates define the message content.

--------

.. _CustomizingEmailTemplates:

Customizing Email templates
---------------------------

Before we can customize any of the email templates, we'll need to copy them
from the Flask-User install directory to your application's template directory.

Copying Email template files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Determine the location of where the Flask-User package is installed::

    # In a python shell, type the following:
    import os
    import flask_user
    print(os.path.dirname(flask_user.__file__))

    # Prints something like:
    # ~/.envs/my_app/lib/python3.6/site-packages/flask_user

2) The examples below assume the following::

    flask_user dir: ~/.envs/my_app/lib/python3.6/site-packages/flask_user
    app dir:        ~/dev/my_app

Adjust the examples below to your specific environment.

3) Copy the template files, substituting your flask_user and your template directory accordingly::

    # IMPORTANT:
    # If you've already worked on customizing form templates, you can (and must) skip this step,
    # since you've already copied the email templates along with the form templates.

    cp ~/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user ~/dev/my_app/app/templates/.
    cp ~/.envs/my_app/lib/python2.7/site-packages/flask_user/templates/flask_user_base.html ~/dev/my_app/app/templates/.

You should now have an app/template/flask_user directory::

    ls -1 ~/dev/my_app/app/templates/flask_user/emails

Expected output::

    base_message.html
    base_message.txt
    base_subject.txt
    confirm_email_message.html
    confirm_email_message.txt
    confirm_email_subject.txt
        ...

Steps 1) through 3) only need to be performed once.

Editing Email template files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After you've `copied the Email template files <CopyEmailTemplateFiles>`,
you can edit any HTML or TXT template file in your ``app/templates/flask_user/emails/`` directory,
and change it to your liking.

Flask-User makes the following template variables available to all email templates::

    app_name      # The value of the USER_APP_NAME app config setting
    email         # The user's email
    user          # The user's User object
    user_manager  # The UserManager object

The following email templates also receive the following template variables::

    # confirm_email templates
    confirm_email_link     # Confirm email link with confirm email token

    # forgot_password templates
    reset_password_link    # Reset password link with reset password token

    # invite_user templates
    accept_invitation_link # Accept invitation like with register token
    invited_by_user        # The user that created this invitation

Here's the default `base_message.html implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/templates/flask_user/emails/base_message.html>`_.

Here's the default `confirm_email_message.html implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/templates/flask_user/emails/confirm_email_message.html>`_.

--------

.. include:: includes/submenu_defs.rst
.. include:: includes/customizing_submenu.rst
