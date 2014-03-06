==================
Event Notification
==================

Flask Applications that want to be kept informed about certain actions that took place
in underlying Flask extensions can do so by registering to receive event notification.

Flask-Util makes use of Flask Signals, which in turn makes use of the Blinker signals.

See the http://flask.pocoo.org/docs/signals/

Installing Blinker
------------------
Since not all applications require notification, Flask-User does not install nor require
the Blinker package.
If your application requires notification please install the Blinker package like so:

::

    pip install blinker

See http://pythonhosted.org/blinker/

Available Events
----------------
Flask-User provides the following event notifications:

.. include:: includes/signals.txt


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
