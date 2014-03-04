Customizing Two
===============

Level Two customizations require editing a non-Python file such as a template file
or a Babel translation file. Mistakes in these files are visible to customers
but it's unlikely that they will endanger the stability of your website.

* `Customizing Emails`_
* `Customizing Field labels`_
* `Customizing Flash messages`_
* `Customizing Form templates`_
* `Customizing Validation messages`_

Customizing Emails
------------------
All user management Emails can be customized by copying the Flask-User email template files
into the application's ``templates`` dir.

To find out where flask_user got installed, type the following::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

If the command returned something like ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages``,
the email template files will be in
``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/emails/``,
and you should copy them to something like: ``~/path/to/YOURAPP/templates/flask_user/emails/``

Emails are sent as multipart messages with a subject, HTML message body and a Text message body. HTML capable
email clients will display the HTML message body while Text-only email clients will display the Text message body.

Each part has a corresponding base template::

    templates/flask_user/emails/base_subject.txt
    templates/flask_user/emails/base_message.html
    templates/flask_user/emails/base_message.txt

The base templates are used to define email elements that are similar in all types of email messages.

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

and define the confirmation specific messages in ``templates/flask_user/emails/confirmation_message.html`` like so::

    {% extends "flask_user/emails/base_message.html" %}

    {% block message %}
    <p>Thank you for registering with Flask-User.</p>
    <p>Visit the link below to complete your registration:</p>
    <p><a href="{{ confirmation_link }}">Confirm your email address</a>.</p>
    <p>If you did not initiate this registration, you may safely ignore this email.</p>
    {% endblock %}

The email template files, along with available template variables listed below:

* templates/flask_user/confirmation_[subject.txt|message.html|message.txt]
    * ``user`` - For example: ``{{ user.email }}``
    * ``confirmation_link`` - For example: ``{{ confirmation_link }}``
* templates/flask_user/reset_password_[subject.txt|message.html|message.txt]
    * ``user`` - For example: ``{{ user.email }}``
    * ``reset_password_link`` - For example: ``{{ reset_password_link }}``

Customizing Field Labels
------------------------
The built-in Form field labels can be customized by editing the 'en' Babel translation file.

[To be documented]

Customizing Flash messages
--------------------------
Flash messages are those one-time system messages that appear on the next page.

Customizing Form Templates
--------------------------
Forms can be customized by copying the Flask-User form template files into the the application's ``templates`` directory.

To find out where flask_user got installed, type the following::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib();"

If the command returned something like ``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages``,
the form template files will be in
``~/.virtualenvs/ENVNAME/lib/python2.7/site-packages/flask_user/templates/flask_user/``,
and you should copy them to something like: ``~/path/to/YOURAPP/templates/flask_user/``

In addition, the path and name of each form template file can be customized individually
through the application's config

.. include:: includes/config_templates.txt

The path is relative to the application's ``templates`` directory.

Form templates can make full use of Jinja2.

Customizing Validation messages
-------------------------------
The built-in Form validation messages be customized by editing the 'en' Babel translation file.

[To be documented]

