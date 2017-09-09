.. _EmailMailerInterface:

EmailMailer Interface
=====================

The EmailMailerInterface class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

.. autoclass:: flask_user.email_mailers.email_mailer_interface.EmailMailerInterface
    :special-members: __init__

.. tip::

    ::

        def __init__(self, app):
            self.app = app
            self.sender_name = self.app.user_manager.USER_EMAIL_SENDER_NAME
            self.sender_email = self.app.user_manager.USER_EMAIL_SENDER_EMAIL

        def send_email_message(...):
            # use self.sender_name and self.sender_email here...

Example implementation
----------------------
Here's the `SMTPEmailMailer() implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/email_mailers/smtp_email_mailer.py>`_.

Customizing Flask-User
----------------------
::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the CustomEmailMailer
            self.email_mailer = CustomEmailMailer(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)
