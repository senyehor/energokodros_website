import logging
from datetime import timedelta
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.crypto import hide_int, hide_str

logger = logging.getLogger(__name__)


class EmailConfirmationController:
    @classmethod
    def send_email_confirmation_message(cls, user: User) -> bool:
        ctx = cls.__generate_context_for_user(user)
        text_message_content = cls.__generate_text_content(
            confirmation_link=reverse_lazy('confirm_email', kwargs=ctx)
        )
        html = render_to_string('registration/email_confirmation.html', ctx)
        msg = EmailMultiAlternatives(
            subject=_('Підтвердження реєстрації'),
            body=text_message_content,
            # django requires from_email to be explicitly set to None
            # to use settings.DEFAULT_FROM_EMAIL
            from_email=None,
            to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except SMTPException as e:
            logger.error(
                msg='something went wrong during sending confirmation email',
                exc_info=e
            )
            return False
        return True

    @staticmethod
    def confirm_email_if_exists_or_404(user_id: int, email: str):
        user = get_object_or_404(User, pk=user_id, email=email)
        user.is_active = True
        user.save()

    @staticmethod
    def __generate_context_for_user(user: User) -> dict[str, str]:
        return {
            'user_id':    hide_int(user.id),
            'user_email': hide_str(user.email),
        }

    @staticmethod
    def __generate_text_content(confirmation_link: str) -> str:
        return _(
            f'Для підтвердження пошти перейдіть по наступному посиланню {confirmation_link}'
        )


def remember_user_for_two_week(request: HttpRequest):
    _remember_user_for_timedelta(request, timedelta(weeks=2))


def _remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)
