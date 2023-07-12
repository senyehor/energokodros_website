from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from administrator.forms import UserRoleApplicationRequestsDecisionForm
from users.models import User, UserRole, UserRoleApplication
from utils.common import try_send_email_add_warning_if_failed


class UserRoleApplicationReviewController:
    def __init__(self, application_decision_form: UserRoleApplicationRequestsDecisionForm,
                 application: UserRoleApplication, request: HttpRequest):
        self.application = application
        self.application_decision_form = application_decision_form
        self.request = request

    def process_depending_on_decision(self, is_approved: bool):
        if is_approved:
            self.__fill_missing_user_role_data_from_form_and_save()
            self.__add_successfully_accepted_role_application_message()
        self.__notify_on_role_application_decision(is_approved)
        self.__delete_user_role_application()

    def __delete_user_role_application(self):
        self.application.delete()

    def __add_successfully_accepted_role_application_message(self):
        messages.success(
            self.request,
            _('Успішно додано роль для користувача')
        )

    def __fill_missing_user_role_data_from_form_and_save(self):
        form = self.application_decision_form
        obj: UserRole = form.save(commit=False)
        obj.user = form.application_user
        obj.institution = form.application_institution
        obj.save()

    def __notify_on_role_application_decision(self, is_approved: bool):
        if is_approved:
            subject = 'Ваш запит на роль підтверджено'
            message = 'Нова роль на energokodros вже доступна вам на сайті ' \
                      'і ви можете починати використовувати її.'
        else:
            subject = 'Ваш запит на роль відхилено'
            message = 'На жаль, адміністратор не схвалив важ запит.'
        message_from_admin = self.application_decision_form.message_for_user
        if self.application_decision_form.message_for_user:
            message += f'\nПовідомлення від адміністратора:\n{message_from_admin}'

        try_send_email_add_warning_if_failed(
            self.request,
            self.application_decision_form.application_user.email,
            subject,
            message
        )

    @staticmethod
    def get_application_decision_form_for_application(application: UserRoleApplication) \
            -> UserRoleApplicationRequestsDecisionForm:
        return UserRoleApplicationRequestsDecisionForm.create_from_application_request(
            application
        )


def _get_message_for_role_application(application_id: int) -> UserRoleApplication:
    # as we use SecureModelChoiceField we get request_id hashed,
    # so converting it to int back
    return get_object_or_404(UserRoleApplication, pk=application_id)


def _check_user_has_no_roles(user: User) -> bool:
    return bool(user.roles)


def _get_applications_from_users_who_confirmed_email_ordered() -> QuerySet:
    return UserRoleApplication.objects.all().filter(user__is_active=True).order_by('-pk')


def _is_admin(request: HttpRequest):
    return request.user.is_authenticated and request.user.is_admin  # noqa
