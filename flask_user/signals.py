"""
    flask_user.signals
    ------------------
    Signals send notifications to subscribed listeners (like your app)

    Flask-User.signals is based on Flask.signals which is based on the blinker module.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

from flask.signals import Namespace

# Place Flask-User signals in our own namespace
_signals = Namespace()

# Signal sent just after a user registered
user_registered = _signals.signal('user.user_registered')

# Signal sent just after a confirmation email was sent
confirmation_email_sent = _signals.signal('user.confirmation_email_sent')

# Signal sent just after an email was confirmed
email_confirmed = _signals.signal('user.email_confirmed')

# Signal sent just after a user logged in
user_logged_in = _signals.signal('user.user_logged_in')

# Signal sent just before a user logged out
user_logged_out = _signals.signal('user.user_logged_out')

# Signal sent just after a username was changed
username_changed = _signals.signal('user.username_changed')

# Signal sent just after a password was changed
password_changed = _signals.signal('user.password_changed')

# Signal sent just after a reset password email was sent
reset_password_email_sent = _signals.signal('user.reset_password_email_sent')

# Signal sent just after a password was reset
password_reset = _signals.signal('user.password_reset')

