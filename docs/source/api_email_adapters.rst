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

.. _CustomEmailAdapters:

Implementing a CustomEmailAdapter
---------------------------------
You can write you own EmailAdapter implementation by defining a CustomEmailAdapter class
and configure Flask-User to use this class like so::

    # Define a CustomEmailAdapter
    from flask_user.email_adapters import EmailAdapterInterface
    class CustomEmailAdapter(EmailAdapterInterface):
        ...

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    # Customize Flask-User
    user_manager.email_adapter = CustomDbAdapter(app)

For an example, see `the SMTPEmailAdapter() implementation <https://github.com/lingthio/Flask-User/blob/master/flask_user/email_adapters/smtp_email_adapter.py>`_.
