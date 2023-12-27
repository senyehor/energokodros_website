import logging

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from users.forms import NewUserForm, UserRoleApplicationFormForRegistration
from users.models import User
from utils.common.email import send_html_email

logger = logging.getLogger(__name__)


class UserRegistrationController:
    __user_form: NewUserForm
    __role_application_without_user_form: UserRoleApplicationFormForRegistration
    __user: User

    def __init__(self, user_form: NewUserForm,
                 role_application_without_user_form: UserRoleApplicationFormForRegistration):
        self.__user_form = user_form
        self.__role_application_without_user_form = role_application_without_user_form

    def save_user_along_with_registration_request_return_user(self) -> User:
        self.__user = self.__user_form.save(commit=False)
        self.__user.save()
        self.__role_application_without_user_form.set_application_request_user(self.__user)
        self.__role_application_without_user_form.save()
        return self.__user

    def send_email_confirmation_message(self, request: HttpRequest):
        return _EmailConfirmationController.send_email_confirmation_message(
            request, self.__user
        )

    @staticmethod
    def confirm_email_if_user_exists(user_id: int, email: str):
        _EmailConfirmationController.confirm_email_if_user_exists_or_404(user_id, email)


class _EmailConfirmationController:
    @classmethod
    def send_email_confirmation_message(cls, request: HttpRequest, user: User) -> bool:
        ctx = cls.__generate_context(request, user)
        html = render_to_string(
            template_name='email/email_confirmation.html',
            context=ctx
        )
        return send_html_email(user.email, 'Підтвердження реєстрації', html)

    @staticmethod
    def confirm_email_if_user_exists_or_404(user_id: int, email: str):
        user = get_object_or_404(User, pk=user_id, email=email)
        user.is_active = True
        user.save()

    @classmethod
    def __generate_context(cls, request: HttpRequest, user: User) -> dict[str, str]:
        return {
            'link': cls.__generate_link_for_user(user, request),
        }

    @classmethod
    def __generate_link_for_user(cls, user: User, request: HttpRequest) -> str:
        protocol = 'https' if request.is_secure() else 'http'
        link_without_host = cls.__generate_path_for_email_confirmation_for_user(user)
        return protocol + '://' + request.get_host() + link_without_host

    @classmethod
    def __generate_path_for_email_confirmation_for_user(cls, user: User) -> str:
        return reverse(
            'confirm-email',
            kwargs={
                'user_id':    user.pk,
                'user_email': user.email,
            }
        )
