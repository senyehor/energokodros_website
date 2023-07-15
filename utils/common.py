import logging
from smtplib import SMTPException

from crispy_forms.bootstrap import StrictButton
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def try_send_email_add_warning_if_failed(
        request: HttpRequest, email: str, subject: str, message: str):
    html = render_to_string(
        'email/regular_email.html',
        context={
            'header': subject,
            'text':   message
        }
    )
    if not send_html_email(email, subject, html):
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
    except SMTPException as e:
        logging.error(
            'failed to send email to %s with error: %s',
            email,  # pylint: disable=C0209
            e
        )
        return False
    return True


def generate_submit_type_button(text: str, value: str) -> StrictButton:
    return StrictButton(
        text,
        name='decision',
        value=value,
        css_class='btn btn-primary mt-4',
        type='submit'
    )
