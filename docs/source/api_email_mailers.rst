.. _EmailMailerInterface:

EmailMailer interface
=====================

The EmailMailer class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`SMTPEmailMailer`
- :ref:`SendmailEmailMailer`
- :ref:`SendgridEmailMailer`
- :ref:`CustomEmailMailer`

.. autoclass:: flask_user.email_mailers.email_mailer.EmailMailer

--------

.. _SMTPEmailMailer:

SMTPEmailMailer
---------------

.. autoclass:: flask_user.email_mailers.smtp_email_mailer.SMTPEmailMailer

Flask-User ships with ``SMTPEmailMailer``,installs ``Flask-Mail``,
and uses as the default email mailer (no customization required).

--------

.. _SendmailEmailMailer:

SendmailEmailMailer
-------------------

.. autoclass:: flask_user.email_mailers.sendmail_email_mailer.SendmailEmailMailer

Flask-User ships with ``SendmailEmailMailer``, but you will need to install ``Flask-Sendmail`` manually::

    pip install Flask-Sendmail

then customize Flask-User like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure the email mailer
            from flask_user.email_mailers import SendmailEmailMailer
            self.email_mailer = SendmailEmailMailer(
                self.email_sender_email, self.email_sender_name)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. _SendgridEmailMailer:

SendgridEmailMailer
-------------------

.. autoclass:: flask_user.email_mailers.sendgrid_email_mailer.SendgridEmailMailer

Flask-User ships with ``SendgridEmailMailer``, but you will need to install ``sendgrid-python`` manually::

    pip install sendgrid-python

then customize Flask-User like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure the email mailer
            from flask_user.email_mailers import SendgridEmailMailer
            self.email_mailer = SendmailEmailMailer(
                self.email_sender_email, self.email_sender_name)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)


