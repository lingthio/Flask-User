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


def send_confirmation_email(email, user, token):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    assert email
    assert user_manager.require_email_confirmation

    # For debug only
    email = 'ling.thio@gmail.com'

    # Generate confirmation link
    confirmation_link = url_for('user.confirm_email', token=token, _external=True)

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email('confirmation',
            user=user, confirmation_link=confirmation_link)

    # Construct Flash-Mail message
    message = Message(subject,
            recipients=[email],
            body = text_message,
            html = html_message)

    # Send message
    current_app.mail.send(message)


def send_reset_password_email(email, user, token):
    # Verify certain conditions
    user_manager =  current_app.user_manager
    assert email
    assert user_manager.enable_forgot_password

    # For debug only
    email = 'ling.thio@gmail.com'

    # Generate confirmation link
    reset_password_link = url_for('user.reset_password', token=token, _external=True)

    # Render subject, html message and text message
    subject, html_message, text_message = _render_email('reset_password',
            user=user,
            reset_password_link=reset_password_link)

    # Construct Flash-Mail message
    message = Message(subject,
            recipients=[email],
            body = text_message,
            html = html_message)

    # Send message
    current_app.mail.send(message)
