from smtplib import SMTPException

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def try_send_email_add_warning_if_failed(
        request: HttpRequest, email: str, subject: str, message: str):
    if send_html_email(email, subject, message):
        messages.warning(request, _(f'Не вдалося надіслати повідомлення на пошту {email}'))


def send_html_email(email: str, subject: str, html: str) -> bool:
    msg = EmailMultiAlternatives(
        subject=subject,
        body=html,
        # django requires from_email to be explicitly set to None
        # to use settings.DEFAULT_FROM_EMAIL
        from_email=None,
        to=[email]
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except SMTPException:
        return False
    return True
