from smtplib import SMTPException

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def try_send_email_add_warning_if_failed(
        request: HttpRequest, email: str, subject: str, message: str):
    if not __send_email(email, subject, message):
        messages.warning(request, _(f'Не вдалося надіслати повідомлення на пошту {email}'))


def __send_email(email: str, subject: str, message: str) -> bool:
    try:
        send_mail(
            subject,
            message,
            # django requires from_email to be explicitly set to None
            # to use settings.DEFAULT_FROM_EMAIL
            from_email=None,
            recipient_list=[email]
        )
    except SMTPException:
        return False
    return True
