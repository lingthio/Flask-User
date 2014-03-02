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

.. include:: includes/signals.txt


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
