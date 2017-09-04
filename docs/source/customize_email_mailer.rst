.. _CustomizeEmailMailer:

Customizing the EmailMailer
===========================

Flask-User uses EmailMailers to send email via various methods.

Flask-User ships with the following EmailMailers:

- :ref:`CustomizeSMTPEmailMailer` for sending email via SMTP.
- :ref:`CustomizeSendmailEmailMailer` for sending email via ``sendmail``.
- :ref:`CustomizeSendgridEmailMailer` for sending email via SendGrid.

and developers can define their own:

- :ref:`CustomEmailMailer`.

--------

.. _CustomizeSMTPEmailMailer:

SMTPEmailMailer
---------------
Flask-User uses the SMTPEmailMailer and install Flask-Mail by default.
No customization is required to use SMTPEmailMailer to send emails via SMTP.

Configure the ``MAIL_...`` settings in your app config to point to the desired SMTP server and account.

--------

.. _CustomizeSendmailEmailMailer:

SendmailEmailMailer
-------------------
Flask-User ships with a SendmailEmailMailer, but Flask-Sendmail must be installed manually::

    pip install Flask-Sendmail

and minor customization is required use to SendmailEmailMailer to send emails via ``sendmail``.::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Use the provided SendmailEmailMailer
            from flask_user.email_mailers import SendmailEmailMailer
            self.email_mailer = SendmailEmailMailer()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

No configuration is required (other than setting up sendmail on your system).

---------

.. _CustomizeSendgridEmailMailer:

SendgridEmailMailer
-------------------
Flask-User ships with a SendgridEmailMailer, but sendgrid-python needs to be installed manually::

    pip install sendgrid-python

and minor customization is required to use SendgridEmailMailer to send emais via SendGrid::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Use the provided SendgridEmailMailer
            from flask_user.email_mailers import SendgridEmailMailer
            self.email_mailer = SendgridEmailMailer()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

Configuration: TBD.

--------

.. _CustomEmailMailer:

Implement a custom EmailMailer
------------------------------

Flask-User allows developers to implement a custom EmailMailer that
conforms to the :ref:`DbAdapterInterface`::

    # Define a custom EmailMailer
    from flask_user.email_mailers import EmailMailer
    class CustomEmailMailer(EmailMailer):
        pass

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self):
            # Use the CustomEmailMailer
            self.email_mailer = CustomEmailMailer()

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)

