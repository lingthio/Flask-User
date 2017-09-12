.. _EmailAdapterInterface:

EmailAdapter Interface
======================

The EmailAdapterInterface class defines an interface to send email messages
while shielding the Flask-User code from the underlying implementation.

.. autoclass:: flask_user.email_adapters.email_adapter_interface.EmailAdapterInterface
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
Here's the `SMTPEmailAdapter() implementation on github <https://github.com/lingthio/Flask-User/blob/master/flask_user/email_adapters/smtp_email_adapter.py>`_.

Customizing Flask-User
----------------------
::

    # Customize Flask-User
    class CustomUserManager(UserManager):

        def customize(self, app):
            # Use the CustomEmailAdapter
            self.email_adapter = CustomEmailAdapter(app)

    # Setup Flask-User
    user_manager = CustomUserManager(app, db, User)
