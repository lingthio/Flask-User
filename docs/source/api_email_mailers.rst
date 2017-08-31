.. _EmailMailers:

EmailMailer interface
=====================

The EmailMailer class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

Included implementations:

- :ref:`EmailMailerForSMTP`
- :ref:`EmailMailerForSendmail`
- :ref:`EmailMailerForSendgrid`
- :ref:`CustomEmailMailer`

Other email mailers can be supported by adding additional interface implementation classes.

.. autoclass:: flask_user.email_mailers.email_mailer.EmailMailer

--------

.. _EmailMailerForSMTP:

EmailMailerForSMTP
-----------------------

.. autoclass:: flask_user.email_mailers.email_mailer_for_smtp.EmailMailerForSMTP

Flask-User ships with ``EmailMailerForSMTP``,installs ``Flask-Mail``,
and uses as the default email mailer (no customization required).

--------

.. _EmailMailerForSendmail:

EmailMailerForSendmail
---------------------------

.. autoclass:: flask_user.email_mailers.email_mailer_for_sendmail.EmailMailerForSendmail

Flask-User ships with ``EmailMailerForSendmail``, but you will need to install ``Flask-Sendmail`` manually::

    pip install Flask-Sendmail

then customize Flask-User like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure the email mailer
            from flask_user.email_mailers import EmailMailerForSendMail
            self.email_mailer = EmailMailerForSendmail(
                self.email_sender_email, self.email_sender_name)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. _EmailMailerForSendgrid:

EmailMailerForSendgrid
----------------------

.. autoclass:: flask_user.email_mailers.email_mailer_for_sendgrid.EmailMailerForSendgrid

Flask-User ships with ``EmailMailerForSendgrid``, but you will need to install ``sendgrid-python`` manually::

    pip install sendgrid-python

then customize Flask-User like so::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure the email mailer
            from flask_user.email_mailers import EmailMailerForSendgrid
            self.email_mailer = EmailMailerForSendmail(
                self.email_sender_email, self.email_sender_name)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

--------

.. _CustomEmailMailer:

EmailMailerForSendgrid
----------------------

.. autoclass:: flask_user.email_mailers.email_mailer_for_sendgrid.EmailMailerForSendgrid

You can configure Flask-User to use a custom email mailer like so:

    # Write your own custom email mailer
    class CustomEmailMailer(object):
        ...

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize():

            # Configure the email mailer
            self.email_mailer = CustomEmailMailer(
                self.email_sender_email, self.email_sender_name)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)
