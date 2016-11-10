=======================
Signals (event hooking)
=======================

Flask Applications that want to be kept informed about certain actions that took place
in the underlying Flask-User extensions can do so by subscribing 'signals' to receive
event notification.

Flask-User defines the following signals:

.. include:: includes/signals.txt


See the http://flask.pocoo.org/docs/signals/

Installing Blinker -- REQUIRED!
-------------------------------
NB: Flask-User relies on Flask signals, which relies on the 'blinker' package.
Event notification WILL NOT WORK without first installing the 'blinker' package.

::

    pip install blinker

See http://pythonhosted.org/blinker/


Subscribing to Signals
----------------------

AFTER BLINKER HAS BEEN INSTALLED, An application can receive event notifications
by using the event signal's ``connect_via()`` decorator::

    from flask_user import user_logged_in

    @user_logged_in.connect_via(app)
    def _after_login_hook(sender, user, **extra):
        sender.logger.info('user logged in')

| For all Flask-User event signals:
| - ``sender``  points to the app, and
| - ``user``  points to the user that is associated with this event.

See `Subscribing to signals <http://flask.pocoo.org/docs/signals/#subscribing-to-signals>`_

Troubleshooting
---------------
If the code looks right, but the tracking functions are not called, make sure to check
to see if the 'blinker' package has been installed (analyze the output of ``pip freeze``).
