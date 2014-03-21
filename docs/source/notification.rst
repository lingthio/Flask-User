==================
Event Notification
==================

Flask Applications that want to be kept informed about certain actions that took place
in underlying Flask extensions can do so by registering to receive event notification.

Flask-User defines the following events:

.. include:: includes/signals.txt

Flask-Util makes use of Flask Signals, which in turn makes use of the Blinker signals.

See the http://flask.pocoo.org/docs/signals/

Installing Blinker
------------------
The ``blinker`` package is required to receive event notifications.

::

    pip install blinker

See http://pythonhosted.org/blinker/

Subscribing to Signals
----------------------

An application can receive event notifications by using the event signal's ``connect_via()`` decorator::

    from flask.ext.user.signals import user_logged_in

    @user_logged_in.connect_via(app)
    def track_login(sender, user, **extra):
        sender.logger.info('user logged in')

| For all Flask-User event signals:
| - ``sender``  points to the app, and
| - ``user``  points to the user that is associated with this event.

See the `Subscribing to signals <http://flask.pocoo.org/docs/signals/#subscribing-to-signals>`_
