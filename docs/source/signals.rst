==================
Event Notification
==================

Signals are notifications that Flask extensions send to notify
the application that something happened.

Applications can subscribe to any provided signal.

See the `Flask documentation on signals <http://flask.pocoo.org/docs/signals/>`_

Available Events
----------------
Flask-User provides the following event signals:

| ``flask.ext.user.signals.confirmation_email_sent``
|     Sent just after a confirmation email was sent

| ``flask.ext.user.signals.email_confirmed``
|     Sent just after an email was confirmed

| ``flask.ext.user.signals.user_logged_in``
|     Sent just after a user logged in

| ``flask.ext.user.signals.user_logged_out``
|     Sent just before a user logged out

| ``flask.ext.user.signals.user_registered``
|     Sent just after a user registered

| ``flask.ext.user.signals.password_changed``
|     Sent just after a password was changed

| ``flask.ext.user.signals.password_reset``
|     Sent just after a password was reset

| ``flask.ext.user.signals.reset_password_email_sent``
|     Sent just after a reset password email was sent

| ``flask.ext.user.signals.username_changed``
|     Sent just after a username was changed


Subscribing to Signals
----------------------

An application can receive event notifications by using the event signal's ``connect_via()`` decorator::

    from flask.ext.user.signals import user_logged_in

    @user_logged_in.connect_via(app)
    def track_login(sender, user, **extra):
        sender.logger.info('user logged in')

| For all Flask-User event signals,
| the ``sender`` param points to the app, and
| the ``user`` param points to the user that is associated with this event.

See the `Flask documentation on subscribing to signals <http://flask.pocoo.org/docs/signals/#subscribing-to-signals>`_
