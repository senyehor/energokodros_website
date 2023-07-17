from django.contrib import messages
from django.db.transaction import atomic
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from users.forms import UserRoleApplicationRequestsDecisionForm
from users.models import UserRole, UserRoleApplication
from utils.common.email import try_send_email_add_warning_if_failed


class UserRoleApplicationReviewController:
    def __init__(self, application_decision_form: UserRoleApplicationRequestsDecisionForm,
                 application: UserRoleApplication, request: HttpRequest, is_approved: bool):
        self.application = application
        self.application_decision_form = application_decision_form
        self.request = request
        self.is_approved = is_approved

    @method_decorator(atomic)
    def process_depending_on_decision(self):
        if self.is_approved:
            self.__create_user_role()
        self.__delete_user_role_application()
        self.__notify_on_role_application_decision()
        self.__add_message_for_decision()

    def __delete_user_role_application(self):
        self.application.delete()

    def __add_message_for_decision(self):
        if self.is_approved:
            message = _('Успішно додано роль для користувача')
        else:
            message = _('Запит користувача було успішно відхилено')
        messages.success(self.request, message)

    def __create_user_role(self):
        user_role_without_user: UserRole = self.application_decision_form.instance
        user_role_without_user.user = self.application.user
        user_role_without_user.save()

    def __notify_on_role_application_decision(self):
        if self.is_approved:
            subject = 'Ваш запит на роль підтверджено'
            message = 'Нова роль на energokodros вже доступна вам на сайті ' \
                      'і ви можете починати використовувати її.'
        else:
            subject = 'Ваш запит на роль відхилено'
            message = 'На жаль, адміністратор не схвалив ваш запит.'
        if message_from_admin := self.application_decision_form.get_message_for_user():
            message += mark_safe(f'<br>Повідомлення від адміністратора:<br> {message_from_admin}')

        try_send_email_add_warning_if_failed(
            self.request,
            self.application.user.email,
            subject,
            message
        )
