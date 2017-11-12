from threading import Thread

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import loader, TemplateDoesNotExist


def render_mail_templates(base_name, context):
    subject = loader.render_to_string(base_name + "_subject.txt", context)
    subject = (" ".join([l.strip() for l in subject.splitlines()])).strip()  # No new lines!
    body_text = loader.render_to_string(base_name + ".txt", context)
    try:
        body_html = loader.render_to_string(base_name + ".html", context)
    except TemplateDoesNotExist:
        body_html = None
    return subject, body_text, body_html


def send_mail(subject, body_text, recipients, body_html=None, from_email=None, sender=None, headers=None,
              connection=None, auth_user=None, auth_password=None, fail_silently=False, async=True):
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not isinstance(recipients, (list, tuple)):
        recipients = [recipients]

    if sender:
        if not isinstance(headers, (list, tuple)):
            headers = {}
        headers["Sender"] = sender
        headers["Return-Path"] = from_email

    if not connection:
        connection = get_connection(username=auth_user, password=auth_password, fail_silently=fail_silently)

    mail = EmailMultiAlternatives(subject, body_text, from_email, recipients, headers=headers, connection=connection)
    if body_html:
        mail.attach_alternative(body_html, "text/html")

    if async:
        # Send email in the background.
        thread = Thread(target=mail.send)
        thread.start()
        return thread

    return mail.send()


def send_template_mail(base_name, recipients, context=None, **kwargs):
    subject, body_text, body_html = render_mail_templates(base_name, context)
    return send_mail(subject, body_text, recipients, body_html=body_html, **kwargs)
