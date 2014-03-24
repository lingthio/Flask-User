""" This file contains email sending functions for Flask-User.
    It uses Jinja2 to render email subject and email message. It uses Flask-Mail to send email.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""

import smtplib
import socket
from flask import current_app, render_template

def _render_email(filename, **kwargs):
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

def send_email(recipient, subject, html_message, text_message):
    """ Send email from default sender to 'recipient' """

    class SendEmailError(Exception):
        pass

    try:
        from flask_mail import Message
    except:
        raise SendEmailError("Flask-Mail is missing. Please install Flask-Mail ('pip install Flask-Mail').")

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

def send_registered_email(email, user, confirm_email_link):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    if not user_manager.enable_email: return
    if not user_manager.send_registered_email and not user_manager.enable_confirm_email: return
    assert(email)

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email(
            user_manager.registered_email_template,
            user=user, confirm_email_link=confirm_email_link)

    # Send email message using Flask-Mail
    user_manager.send_email_function(email, subject, html_message, text_message)

def send_forgot_password_email(email, user, reset_password_link):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    if not user_manager.enable_email: return
    assert user_manager.enable_forgot_password
    assert email

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email(
            user_manager.forgot_password_email_template,
            user=user,
            reset_password_link=reset_password_link)

    # Send email message using Flask-Mail
    user_manager.send_email_function(email, subject, html_message, text_message)
