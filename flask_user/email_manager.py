from flask import current_app, render_template, url_for
from flask_mail import Message

def _render_confirmation_email(user, confirmation_link):
    # Render subject
    subject = render_template('flask_user/emails/confirmation_subject.txt',
            user=user,
            confirmation_link=confirmation_link)
    # Make sure that subject lines do not contain newlines
    subject = subject.replace('\n', ' ')
    subject = subject.replace('\r', ' ')

    # Render HTML message
    html_message = render_template('flask_user/emails/confirmation_message.html',
            user=user,
            confirmation_link=confirmation_link)

    # Render text message
    text_message = render_template('flask_user/emails/confirmation_message.txt',
            user=user,
            confirmation_link=confirmation_link)

    return (subject, html_message, text_message)


def send_confirmation_email(email, user):
    # Only send emails if USER_REGISTER_WITH_EMAIL is True
    user_manager =  current_app.user_manager
    if user_manager.register_with_email:

        # For debug only
        email = 'ling.thio@gmail.com'

        # Generate token and confirmation link
        token = user_manager.token_manager.generate_token(user.id)
        confirmation_link = url_for('user.confirm_email', token=token, _external=True)

        # Render subject, html message and text message
        subject, html_message, text_message = _render_confirmation_email(user, confirmation_link)

        # Construct Flash-Mail message
        message = Message(subject,
                recipients=[email],
                body = text_message,
                html = html_message)

        # Send message
        current_app.mail.send(message)

