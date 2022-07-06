from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from users.models import UserRoleApplication


def _get_message_for_role_application(request_id: int | str):
    return get_object_or_404(UserRoleApplication, id=request_id).message


def _send_registration_review_result_email(email: str, approved: bool, message: str) -> bool:
    subject = _('Ваш запит на реєстрацію ') + _('ухвалено') if approved else _('скасовано')
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
