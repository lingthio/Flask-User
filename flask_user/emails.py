"""
    flask_user.emails
    -----------------
    This module contains Flask-User functions that deal with sending emails.

    It uses Jinja2 to render email subject and email message.
    It uses Flask-Mail to send email.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""

import smtplib
import socket

from flask import current_app, render_template, url_for
from flask_mail import Message

def _render_email(email_name, **kwargs):
    filename = 'flask_user/emails/'+email_name

    # Render subject
    subject = render_template(filename+'_subject.txt', **kwargs)
    # Make sure that subject lines do not contain newlines
    subject = subject.replace('\n', ' ')
    subject = subject.replace('\r', ' ')

    # Render HTML message
    html_message = render_template(filename+'_message.html', **kwargs)

    # Render text message
    text_message = render_template(filename+'_message.txt', **kwargs)

    return (subject, html_message, text_message)

def _send_email(recipient, subject, html_message, text_message):
    class SendEmailError(Exception):
        pass

    # Construct Flash-Mail message
    message = Message(subject,
            recipients=[recipient],
            html = html_message,
            body = text_message)

    # Send email using Flash-Mail
    try:
        current_app.mail.send(message)

    # Print helpful error messages on exceptions
    except (socket.gaierror, socket.error) as e:
        raise SendEmailError('SMTP Connection error: Check your MAIL_HOSTNAME or MAIL_PORT settings.')
    except smtplib.SMTPAuthenticationError:
        raise SendEmailError('SMTP Authentication error: Check your MAIL_USERNAME and MAIL_PASSWORD settings.')



def send_confirmation_email(email, user, token):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    assert email
    assert user_manager.enable_confirm_email

    # Generate confirmation link
    confirmation_link = url_for('user.confirm_email', token=token, _external=True)

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email('confirmation',
            user=user, confirmation_link=confirmation_link)

    # Send email message using Flask-Mail
    _send_email(email, subject, html_message, text_message)


def send_reset_password_email(email, user, token):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    assert email
    assert user_manager.enable_forgot_password

    # Generate confirmation link
    reset_password_link = url_for('user.reset_password', token=token, _external=True)

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email('reset_password',
            user=user,
            reset_password_link=reset_password_link)

    # Send email message using Flask-Mail
    _send_email(email, subject, html_message, text_message)
