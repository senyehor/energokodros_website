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

logger = logging.getLogger(__name__)


class EmailConfirmationController:
    @classmethod
    def send_email_confirmation_message(cls, request: HttpRequest, user: User) -> bool:
        ctx = cls.__generate_context(request, user)
        html = render_to_string(
            template_name='registration/email_confirmation.html',
            context=ctx
        )
        msg = EmailMultiAlternatives(
            subject=_('Підтвердження реєстрації'),
            body=html,
            # django requires from_email to be explicitly set to None
            # to use settings.DEFAULT_FROM_EMAIL
            from_email=None,
            to=[user.email]
        )
        msg.content_subtype = 'html'
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
    def confirm_email_if_user_exists_or_404(user_id: int, email: str):
        user = get_object_or_404(User, pk=user_id, email=email)
        user.is_active = True
        user.save()

    @staticmethod
    def __generate_context(request: HttpRequest, user: User) -> dict[str, str]:
        link_without_host = reverse_lazy(
            '',
            kwargs={
                'user_id':    user.pk,
                'user_email': user.email,
            }
        )
        return {
            'link': request.get_host() + link_without_host,
        }


def remember_user_for_two_week(request: HttpRequest):
    _remember_user_for_timedelta(request, timedelta(weeks=2))


def _remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)
