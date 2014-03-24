Customize Two
=============

Level Two customizations require editing a non-Python file such as a template file
or a Babel translation file. Mistakes in these files are visible to customers
but it's unlikely that they will endanger the stability of your website.

* `Customizing Emails`_
* `Customizing Field labels`_
* `Customizing Flash messages`_
* `Customizing Form templates`_
* `Customizing Form template filenames`_
* `Customizing Validation messages`_

Customizing Emails
------------------
Emails can be customized by copying the built-in email template files
from the flask_user templates directory to your application's templates directory.

The flask_user directory depends on Python, virtualenv and pip
and can be determined with the following command::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

Let's assume that:

* This command returned: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/``
* Your app directory is: ``~/path/to/YOURAPP/``

Emails can be customized by copying the email template files like so::

    mkdir -p ~/path/to/YOURAPP/templates/flask_user/emails
    cp ~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/emails/* ~/path/to/YOURAPP/templates/flask_user/emails/.

and by editing the copies to your liking.

Flask-User currently offers the following email types::

    registered       # Sent to users after they submitted a registration form
    forgot_password  # Sent to users after they submitted a forgot password form

Each email type has three email template files.
The 'registered' email for example has the following files::

    templates/flask_user/emails/registered_subject.txt   # The email subject line
    templates/flask_user/emails/registered_message.html  # The email message in HTML format
    templates/flask_user/emails/registered_message.txt   # The email message in Text format

Each file is extended from the base template file::

    templates/flask_user/emails/base_subject.txt
    templates/flask_user/emails/base_message.html
    templates/flask_user/emails/base_message.txt

The base template files are used to define email elements that are similar in all types of email messages.

| If, for example, for every email you want to:
| - Set the background color and padding,
| - Start with a logo and salutation, and
| - End with a signature,
| you can define ``templates/flask_user/emails/base_message.html`` like so

::

    <div style="background-color: #f4f2dd; padding: 10px;">
        <p><img src="http://example.com/static/images/email-logo.png"></p>
        <p>Dear Customer,</p>
        {% block message %}{% endblock %}
        <p>Sincerely,<br/>
        The Flask-User Team</p>
    </div>

and define the confirmation specific messages in ``templates/flask_user/emails/confirm_email_message.html`` like so::

    {% extends "flask_user/emails/base_message.html" %}

    {% block message %}
    <p>Thank you for registering with Flask-User.</p>
    <p>Visit the link below to complete your registration:</p>
    <p><a href="{{ confirm_email_link }}">Confirm your email address</a>.</p>
    <p>If you did not initiate this registration, you may safely ignore this email.</p>
    {% endblock %}

The email template files, along with available template variables listed below:

* Template variables available in any email template
    * ``user_manager`` - For example: ``{% if user_manager.enable_confirm_email %}``
    * ``user`` - For example: ``{{ user.email }}``
* templates/flask_user/registered_[subject.txt|message.html|message.txt]
    * ``confirm_email_link`` - For example: ``{{ confirm_email_link }}``
* templates/flask_user/forgot_password_[subject.txt|message.html|message.txt]
    * ``reset_password_link`` - For example: ``{{ reset_password_link }}``

If you need other email notifications, please enter a feature request to our Github issue tracker. Thank you.

Customizing Field Labels
------------------------
The built-in Form field labels can be customized by editing the 'en' Babel translation file.

See :doc:`internationalization`

Customizing Flash messages
--------------------------
Flash messages are those one-time system messages that appear on the next page.
The built-in Flash messages can be customized by editing the 'en' Babel translation file.

See :doc:`internationalization`

.. _customizingformtemplates:

Customizing Form Templates
--------------------------
Forms can be customized by copying the built-in form template files
from the flask_user templates directory to your application's templates directory.

The flask_user directory depends on Python, virtualenv and pip
and can be determined with the following command::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

Let's assume that:

* This command returned: ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/``
* Your app directory is: ``~/path/to/YOURAPP/``

Forms can be customized by copying the form template files like so::

    mkdir -p ~/path/to/YOURAPP/templates/flask_user
    cp ~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/*.html ~/path/to/YOURAPP/templates/flask_user/.

and by editing the copies to your liking.

The following form template files resides in the ``templates`` directory and can be customized::

    base.html                         # root template

    flask_user/member_base.html       # extends base.html
    flask_user/change_password.html   # extends flask_user/member_base.html
    flask_user/change_username.html   # extends flask_user/member_base.html

    flask_user/public_base.html       # extends base.html
    flask_user/forgot_password.html   # extends flask_user/public_base.html
    flask_user/login.html             # extends flask_user/public_base.html
    flask_user/register.html          # extends flask_user/public_base.html
    flask_user/reset_password.html    # extends flask_user/public_base.html


Customizing Form Template filenames
-----------------------------------
In addition to customizing the Form Template file,
the path and filename of each form template file can be customized individually
through the application's config

.. include:: includes/config_form_templates.txt

These path settings are relative to the application's ``templates`` directory.

Form templates can make full use of Jinja2.

Customizing Validation messages
-------------------------------
The built-in Form validation messages be customized by editing the 'en' Babel translation file.

See :doc:`internationalization`

